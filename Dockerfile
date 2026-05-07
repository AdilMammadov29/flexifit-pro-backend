# 1. İşletim sistemi ve Python sürümünü seçiyoruz
FROM python:3.10-slim

# 2. Konteyner içinde çalışacağımız klasörü belirliyoruz
WORKDIR /app

# 3. Kütüphane listemizi kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Geri kalan tüm kodlarımızı (app.py vb.) kopyalıyoruz
COPY . .

# 5. Dışarıya açacağımız portu (Flask'ın çalıştığı port) belirtiyoruz
EXPOSE 5000

# 6. Konteyner çalıştırıldığında verilecek komut
CMD ["python", "app.py"]