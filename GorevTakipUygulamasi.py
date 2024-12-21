import json
import os
from datetime import datetime

class Gorev:
       def __init__(self, baslik, aciklama, oncelik, tarih=None, tamamlandi=False):
              self.baslik = baslik
              self.aciklama = aciklama
              self.oncelik = oncelik
              self.tarih = tarih or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              self.tamamlandi = tamamlandi

       def to_dict(self):
              return {
                     "baslik": self.baslik,
                     "aciklama": self.aciklama,
                     "oncelik": self.oncelik,
                     "tarih": self.tarih,
                     "tamamlandi": self.tamamlandi
              }
       
       @staticmethod
       def from_dict(data):
              return Gorev(
            baslik=data["baslik"],
            aciklama=data["aciklama"],
            oncelik=data["oncelik"],
            tarih=data["tarih"],
            tamamlandi=data["tamamlandi"]
        )
       
class GorevTakipUygulamasi:
       def __init__(self, dosya_adi="gorevler.json"):
              self.dosya_adi = dosya_adi
              self.gorevler = self.verileri_yukle()

       def verileri_yukle(self):
              if os.path.exists(self.dosya_adi):
                     with open(self.dosya_adi, "r", encoding="utf-8") as dosya:
                            return [Gorev.from_dict(gorev) for gorev in json.load(dosya)]
                     return []
              
       def verileri_kaydet(self):
              with open(self.dosya_adi, "w", encoding="utf-8") as dosya:
                     json.dump([gorev.to_dict() for gorev in self.gorevler], dosya, indent=4, ensure_ascii=False)

       def gorev_ekle(self, baslik, aciklama, oncelik):
              yeni_gorev = Gorev(baslik, aciklama, oncelik)
              self.gorevler.append(yeni_gorev)
              self.verileri_kaydet()
              print("Görev başarı ile eklendi\n")

       def gorevleri_listele(self):
              if not self.gorevler:
                     print("Henüz bir görev eklemediniz!\n")
                     return
              
              print("\nMevcut Görevler:\n")
              for i, gorev in enumerate(self.gorevler, start=1):
                     durum = "Tamamlandı" if gorev.tamamlandi else "Devam Ediyor"
                     print(f"{i}. {gorev.baslik} - {gorev.oncelik} - {gorev.tarih} - Durum: {durum}")
              print()

       def gorevi_duzenle(self, indeks, yeni_baslik=None, yeni_aciklama=None, yeni_oncelik=None):
              if 0 <= indeks < len(self.gorevler):
                     if yeni_baslik:
                            self.gorevler[indeks].baslik = yeni_baslik
                     if yeni_aciklama:
                            self.gorevler[indeks].aciklama = yeni_aciklama
                     if yeni_oncelik:
                            self.gorevler[indeks].oncelik = yeni_oncelik
                     self.verileri_kaydet()
                     print("Görev başarı ile güncellendi!\n")
              else:
                     print("Geçersiz görev seçimi\n")
              
       def gorevi_tamamla(self, indeks):
              if 0 <= indeks < len(self.gorevler):
                     self.gorevler[indeks].tamamlandi = True
                     self.verileri_kaydet()
                     print("Görev başarı ile tamamlandı!\n")
              else:
                     print("Geçersiz görev seçimi!\n")

       def gorevi_sil(self, indeks):
              if 0 <= indeks < len(self.gorevler):
                     silinen = self.gorevler.pop(indeks)
                     self.verileri_kaydet()
                     print(f"'{silinen.baslik}' başlıklı görev silindi!\n")
              else:
                     print("Geçersiz görev seçimi!\n")

       def gorev_ara(self, kelime):
              bulunanlar = [gorev for gorev in self.gorevler if kelime.lower() in gorev.baslik.lower() or kelime.lower() in gorev.aciklama.lower()]
              if not bulunanlar:
                     print("Aradığınız kriterlere uygun bir görev bulunamadı!\n")
                     return
              
              print("\nArama Sonuçları:\n")
              for i, gorev in enumerate(bulunanlar, start=1):
                     durum = "Tamamlandı" if gorev.tamamlandi else "Devam Ediyor"
                     print(f"{i}. {gorev.baslik} - {gorev.oncelik} - {gorev.tarih} - Durum: {durum}")
              print()
       
       def calistir(self):
              while True:
                     print("\n--- Görev Takip Uygulaması ---")
                     print("1. Yeni Görev Ekle")
                     print("2. Görevleri Listele")
                     print("3. Görevi Düzenle")
                     print("4. Görevi Tamamla")
                     print("5. Görevi Sil")
                     print("6. Görev Ara")
                     print("7. Çıkış")

                     secim = input("Yapmal istediğiniz işlemi seçiniz: ")

                     if secim == "1":
                            baslik = input("Görev Başlığı: ")
                            aciklama = input("Görev Açıklaması: ")
                            oncelik = input("Görev Önceliği (Düşük-Orta_Yüksek): ")
                            self.gorev_ekle(baslik, aciklama, oncelik)
                     
                     elif secim == "2":
                            self.gorevleri_listele()

                     elif secim == "3":
                            self.gorevleri_listele()
                            try:
                                   indeks = int(input("Düzenlemek istediğiniz görev numarası: ")) - 1
                                   yeni_baslik = input("Yeni Başlık (boş bırakabilirsiniz): ")
                                   yeni_aciklama = input("Yeni Açıklama (boş bırakabilirsiniz): ")
                                   yeni_oncelik = input("Yeni Öncelik (boş bırakabilirsiniz): ")
                                   self.gorevi_duzenle(indeks, yeni_baslik, yeni_aciklama, yeni_oncelik)
                            except ValueError:
                                   print("Geçersiz giriş!\n")

                     elif secim == "4":
                            self.gorevleri_listele()
                            try:
                                   indeks = int(input("Tamamlamak istediğiniz görev numarası: ")) - 1
                                   self.gorevi_tamamla(indeks)
                            except ValueError:
                                   print("Geçersiz Giriş!\n")

                     elif secim == "5":
                            self.gorevleri_listele()
                            try:
                                   indeks = int(input("Silmek istediğiniz görev numarası: ")) - 1
                                   self.gorevi_sil(indeks)
                            except ValueError:
                                   print("Geçersiz İşlem!\n")
                            
                     elif secim == "6":
                            kelime = input("Aramak istediğiniz kelime: ")
                            self.gorev_ara(kelime)

                     elif secim == "7":
                            print("Görev Takip Uygulamasından Çıkış Yapılıyor...\n")
                            print("Görüşmek Üzere!\n")
                            break

                     else:
                            print("Geçersiz seçim! Lütfen tekrar deneyiniz!\n")

uygulama = GorevTakipUygulamasi()
uygulama.calistir()