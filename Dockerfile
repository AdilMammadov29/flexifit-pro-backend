# Python'un hafif bir versiyonunu kullanıyoruz
FROM python:3.9-slim

# Konteyner içindeki çalışma dizinini belirliyoruz
WORKDIR /app

# Önce requirements.txt dosyasını kopyalayıp kütüphaneleri kuruyoruz (Cache avantajı için)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Şimdi tüm proje dosyalarını kopyalıyoruz
COPY . .

# Flask uygulamasının çalışacağı portu açıyoruz (Render genelde portu otomatik ayarlar ama standart 5000'dir)
EXPOSE 5000

# Uygulamayı başlatma komutu (app.py dosyanı çalıştırır)
CMD ["python", "app.py"]