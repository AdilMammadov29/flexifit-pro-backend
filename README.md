# FlexiFit Pro Backend API 🚀🏋️‍♂️

FlexiFit platformunun gelişmiş sürümü için tasarlanmış, ölçeklenebilir ve yüksek performanslı RESTful Web API projesi. Bu sürüm, standart uygulamaya kıyasla daha karmaşık veri ilişkilerini ve optimize edilmiş önbellek yönetimini içerir.

## 🌟 Öne Çıkan Özellikler
* **Gelişmiş Önbellekleme Mimarisi:** Sık erişilen antrenman programları ve kullanıcı istatistikleri **Redis** üzerinde tutularak milisaniye seviyesinde yanıt süreleri elde edilir.
* **Güvenli Veri Yönetimi:** Kullanıcı hesapları, şifreleme algoritmaları ve seans (session) kontrolleri **SQLite** tabanlı yapı üzerinde güvenle işlenir.
* **Genişletilebilir Uç Noktalar (Endpoints):** Antrenman verilerini, diyet listelerini ve kullanıcı gelişimini takip etmek için modüler Flask rotaları (routes) oluşturulmuştur.

## 🛠️ Teknoloji Yığını
* **Backend:** Python, Flask
* **Veritabanı:** SQLite
* **Cache & Performans:** Redis
* **Test & Geliştirme:** Postman (API Testleri)

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda test etmek için aşağıdaki adımları izleyin:

1. **Depoyu Klonlayın:**
   ```bash
   git clone [https://github.com/AdilMammadov29/flexifit-pro-backend.git](https://github.com/AdilMammadov29/flexifit-pro-backend.git)
   cd flexifit-pro-backend
