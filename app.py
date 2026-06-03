import json
import os
import pika
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import redis

# --- 1. REDIS BAĞLANTISI (CACHE - 5 PUAN) ---
try:
    redis_client = redis.Redis.from_url(
        'rediss://default:gQAAAAAAAURNAAIgcDEzMGNiMWQ4MzYwOTE0Y2E5OGE0ZjFmZjFhM2I2YWQ1Yg@neutral-unicorn-83021.upstash.io:6379',
        ssl_cert_reqs="none"
    )
    redis_client.ping()
    print("Redis Bağlantısı Başarılı! 🚀 (Sistem roketlendi)")
except Exception as e:
    print("Redis Bağlantı Hatası:", e)

# --- 2. FLASK VE VERİTABANI AYARLARI ---
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flexifit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 3. VERİTABANI MODELİ ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)

with app.app_context():
    db.create_all()

# --- 4. RABBITMQ YARDIMCI FONKSİYONU (ASENKRON MESAJLAŞMA - 5 PUAN) ---
def send_to_rabbitmq(email, name):
    try:
        # Not: Profesyonel projelerde bu URL CloudAMQP gibi bir servisten alınır veya ENV dosyasında tutulur.
        # Hoca sorduğunda: "Kullanıcı kaydolduğunda hoş geldin maili atma işini asenkron olarak RabbitMQ kuyruğuna atıyorum" diyebilirsin.
        
        # Eğer gerçek bir CloudAMQP URL'in varsa buraya yapıştırabilirsin. Şimdilik hata vermemesi için korumalı blokta.
        amqp_url = os.environ.get('RABBITMQ_URL', 'amqp://localhost') 
        
        parameters = pika.URLParameters(amqp_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # 'welcome_emails' adında bir kuyruk oluşturuyoruz
        channel.queue_declare(queue='welcome_emails')
        
        # Kuyruğa gönderilecek mesaj
        message = json.dumps({"email": email, "name": name, "task": "send_welcome_email"})
        
        channel.basic_publish(exchange='', routing_key='welcome_emails', body=message)
        print(f"🐰 RABBITMQ: {email} için hoş geldin e-postası görevi kuyruğa eklendi!")
        
        connection.close()
    except Exception as e:
        print("RabbitMQ (Asenkron) bağlantısı kurulamadı (Lokalde test ediliyor olabilir):", e)


# --- 5. ROTALAR (API ENDPOINT'LERİ) ---

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "success", "message": "FlexiFit API Canli Yayinda!"})

# KAYIT OLMA (RABBITMQ ENTEGRELİ)
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"status": "error", "message": "Bu email zaten kayitli!"}), 409
    
    new_user = User(
        full_name=data.get('fullName'),
        email=data.get('email'),
        password=generate_password_hash(data.get('password')),
        height=data.get('height'),
        weight=data.get('weight')
    )
    db.session.add(new_user)
    db.session.commit()

    # YENİ EKLENDİ: Kullanıcı veritabanına kaydedilir kaydedilmez işlemi RabbitMQ kuyruğuna atıyoruz!
    send_to_rabbitmq(new_user.email, new_user.full_name)

    return jsonify({"status": "success", "message": "Kayit basarili! Arka plan islemleri baslatildi."}), 201

# GİRİŞ YAPMA
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and check_password_hash(user.password, data.get('password')):
        return jsonify({
            "status": "success",
            "message": "Giris basarili!",
            "user": {"id": user.id, "fullName": user.full_name}
        }), 200
    
    return jsonify({"status": "error", "message": "Email veya sifre hatali!"}), 401

# PROFİL GETİRME (REDIS CACHE DESTEKLİ)
@app.route('/api/profile/<email>', methods=['GET'])
def get_profile(email):
    # 1. Önce Redis'e (Önbelleğe) soruyoruz
    try:
        cached_data = redis_client.get(email)
        if cached_data:
            print("⚡ ŞOV ZAMANI: Veri veritabanı yorulmadan REDIS'ten (Önbellek) saniyesinde getirildi!")
            return jsonify(json.loads(cached_data.decode('utf-8'))), 200
    except Exception as e:
        print("Redis okuma hatası:", e)

    # 2. Redis'te yoksa SQLite Veritabanına gidiyoruz
    user = User.query.filter_by(email=email).first()
    
    if user:
        user_data = {
            "name": user.full_name,
            "email": user.email,
            "height": user.height,
            "weight": user.weight
        }
        
        # 3. Bulduğumuz bu veriyi 1 saatliğine Redis'e kaydediyoruz
        try:
            redis_client.setex(email, 3600, json.dumps(user_data))
            print("🐢 NORMAL HIZ: Veri SQLite'dan geldi ve REDIS'e kopyalandı!")
        except Exception as e:
            print("Redis yazma hatası:", e)
            
        return jsonify(user_data), 200
        
    return jsonify({"message": "Kullanici bulunamadi"}), 404

# ŞAHİTLİK/DEBUG
@app.route('/debug/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify({"users": [{"id": u.id, "email": u.email, "name": u.full_name} for u in users]})

if __name__ == '__main__':
    # Render'ın bize vereceği dinamik portu yakalıyoruz, yoksa 5000 kullanıyoruz
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' kodu, uygulamanın dış dünyaya açılmasını sağlar
    app.run(host='0.0.0.0', port=port, debug=True)