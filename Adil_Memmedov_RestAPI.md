# Adil Memmedov - FlexiFit REST API Dokümantasyonu

**REST API Canlı Domain Adresi:** https://flexifit-api.onrender.com

**YouTube API Test Videosu:** [Video Linki Buraya Gelecek]

## Üzerime Düşen Gereksinimler (Auth & User Management)
Grup dağılımına göre kullanıcı kayıt, giriş ve listeleme (şahitlik) API uçları tarafımca geliştirilmiştir.

### 1. Kullanıcı Kaydı (Register)
* **Metot:** POST
* **Yol (Endpoint):** `/auth/register`
* **Açıklama:** Yeni bir kullanıcının sisteme kayıt olmasını sağlar. Şifreler veritabanına hash'lenerek kaydedilir.
* **Request Body (JSON):**
    ```json
    {
      "fullName": "Adil Mammadov",
      "email": "adil@sdu.edu.tr",
      "password": "UltraGuvenli123!",
      "height": 186,
      "weight": 98
    }
    ```

### 2. Kullanıcı Girişi (Login)
* **Metot:** POST
* **Yol (Endpoint):** `/auth/login`
* **Açıklama:** Kayıtlı kullanıcının e-posta ve şifresiyle sisteme giriş yapmasını (doğrulama) sağlar.
* **Request Body (JSON):**
    ```json
    {
      "email": "adil@sdu.edu.tr",
      "password": "UltraGuvenli123!"
    }
    ```

### 3. Kullanıcıları Listeleme (Debug/Şahitlik)
* **Metot:** GET
* **Yol (Endpoint):** `/debug/users`
* **Açıklama:** Veritabanına kayıtlı kullanıcıların temel bilgilerini listeler. (Veritabanı kontrolü için).
* **Request Body:** Bulunmuyor.