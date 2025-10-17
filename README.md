# ☁️ Serverless API - AWS Lambda + API Gateway (Python)

## 🎯 Proje Amacı
Bu projenin amacı, **serverless mimariyi** kavramak ve **AWS Lambda** üzerinde çalışan, API Gateway aracılığıyla HTTP üzerinden erişilebilen bir bulut fonksiyonu geliştirmektir.  
Bu proje kapsamında oluşturulan API, kullanıcıdan `name` ve opsiyonel olarak `number` parametrelerini alır, kullanıcının adını içeren bir mesaj döner ve eğer sayı parametresi gönderildiyse karesini hesaplayarak yanıtlar.

---

## ⚙️ Kullanılan AWS Servisleri ve Mimari

### 🧩 Mimari Bileşenler
| Servis | Açıklama |
|--------|-----------|
| **AWS Lambda** | Sunucusuz fonksiyon çalıştırma hizmeti. Kodun çalıştığı ortamdır. |
| **Amazon API Gateway** | HTTP isteklerini Lambda fonksiyonuna yönlendiren API katmanıdır. |
| **Amazon CloudWatch** | Lambda fonksiyonuna ait logları ve metrikleri otomatik olarak kaydeder. |
| **IAM (Identity & Access Management)** | Lambda'nın yalnızca gerekli izinlerle çalışmasını sağlar (least privilege). |

### 🏗️ Mimari Akış
1. Kullanıcı, tarayıcı veya Postman üzerinden bir HTTP isteği yapar:  
   `https://{api-id}.execute-api.{region}.amazonaws.com/hello?name=Ali&number=5`
2. **API Gateway** isteği alır ve **Lambda fonksiyonuna** yönlendirir.
3. **Lambda**, parametreleri işler:  
   - “Merhaba {name}” mesajı oluşturur.  
   - Eğer `number` verilmişse, karesini hesaplar.  
4. **Lambda**, sonuç mesajını JSON formatında döner.  
5. **CloudWatch Logs**, fonksiyonun çalışmasıyla ilgili detayları otomatik olarak kaydeder.  

Bu yapı tamamen **serverless** olduğu için herhangi bir sunucu yönetimi gerekmez ve maliyet yalnızca fonksiyonun çağrıldığı süreyle sınırlıdır.

---

## 🧠 Lambda Fonksiyonu Kodu (Python 3.9)

```python
import json

def lambda_handler(event, context):
    params = event.get("queryStringParameters", {}) or {}
    name = params.get("name", "Ziyaretçi")
    number_str = params.get("number")

    message = f"Merhaba {name}, bu fonksiyon bulutta çalışıyor!"

    if number_str:
        try:
            number = float(number_str)
            square = number ** 2
            message += f" {number} sayısının karesi {square}’tir."
        except ValueError:
            message += " Ancak geçerli bir sayı girmedin."

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message})
    }

``` 

🚀 AWS Üzerinde Kurulum ve Deploy Adımları
------------------------------------------

### 1️⃣ AWS Hesabına Giriş

-   https://aws.amazon.com/ adresine gidip AWS hesabına giriş yap.

-   AWS Management Console üzerinden işlem yapacağız.

* * * * *

### 2️⃣ Lambda Fonksiyonunu Oluşturma

1.  Console arama çubuğuna **Lambda** yaz → **AWS Lambda** servisini aç.

2.  "**Create function**" butonuna tıkla.

3.  "**Author from scratch**" seçeneğini seç.

4.  Aşağıdaki ayarları gir:

    -   **Function name:** `helloFunction`

    -   **Runtime:** `Python 3.9`

    -   **Permissions:** "Create a new role with basic Lambda permissions"\
        (CloudWatch loglarını otomatik olarak etkinleştirir.)

5.  "**Create function**" butonuna bas.

* * * * *

### 3️⃣ Kodun Eklenmesi

1.  Fonksiyon oluşturulduktan sonra **Code** sekmesine git.

2.  Yukarıdaki Python kodunu editöre yapıştır.

3.  Sağ üstteki **Deploy** butonuna tıkla.

* * * * *

### 4️⃣ API Gateway Tetikleyicisini Ekleme

1.  Fonksiyon sayfasında "**Add trigger**" butonuna tıkla.

2.  **API Gateway** seçeneğini seç.

3.  "**Create an API → HTTP API**" seç.

4.  Güvenlik: "**Open**" (herkese açık erişim).

5.  "**Add**" butonuna tıkla.

6.  AWS otomatik olarak bir **Invoke URL** oluşturur:

    `https://abcd1234.execute-api.eu-central-1.amazonaws.com/hello`

* * * * *

### 5️⃣ API'yi Test Etme

Tarayıcıda veya Postman'da aşağıdaki örnek URL'leri test edebilirsin:

| Test | URL | Beklenen Sonuç |
| --- | --- | --- |
| Basit test | `/hello?name=Ali` | `{"message": "Merhaba Ali, bu fonksiyon bulutta çalışıyor!"}` |
| Sayı parametresiyle | `/hello?name=Ayşe&number=5` | `{"message": "Merhaba Ayşe, bu fonksiyon bulutta çalışıyor! 5 sayısının karesi 25'tir."}` |
| Hatalı sayı | `/hello?name=Ali&number=abc` | `{"message": "Merhaba Ali, bu fonksiyon bulutta çalışıyor! Ancak geçerli bir sayı girmedin."}` |







