# AI Senior Posture Master v20

Bu proje, bilgisayar başında uzun süre vakit geçiren kullanıcılar için geliştirilmiş, yapay zeka tabanlı bir **Gerçek Zamanlı Postür Takip ve Analiz** sistemidir. MediaPipe ve OpenCV kullanarak vücut mekaniğini analiz eder ve hatalı duruşlarda kullanıcıyı hem görsel hem de sesli olarak uyarır.

## Öne Çıkan Özellikler
* **Çok Boyutlu Analiz:** Sadece vücut eğilmesini değil; boyun düşmesini (Neck Drop) ve omuz kapanmasını (Shoulder Rounding) takip eder.
* **Akıllı Sabır Mekanizması:** Anlık hareketlerde uyarmaz; sadece 2 saniye ve üzeri hatalı duruşlarda devreye girer.
* **Sesli & Görsel Uyarı:** Windows `winsound` entegrasyonu ile sesli, dinamik HUD arayüzü ile görsel bildirim sağlar.
* **Seans Karnesi:** Program kapatıldığında toplam çalışma süresi ve "Sağlık Puanı" raporu sunar.
* **Responsive Arayüz:** Her pencere boyutuna uyumlu, dinamik veri paneli (Telemetri).

## Kurulum ve Çalıştırma

Bu projenin çalışabilmesi için sisteminizde Python 3.10+ yüklü olmalıdır.

### 1. Gerekli Kütüphaneler
Kütüphaneler arasında versiyon çatışması yaşanmaması için aşağıdaki komutu terminale yapıştırarak en stabil sürümleri yükleyin:

```bash
pip install mediapipe opencv-python numpy

# Önemli Not: Eğer hata alırsanız, sisteminizde Microsoft Visual C++ Redistributable paketinin yüklü olduğundan emin olun.