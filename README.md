# Fragile-Watermarking

Kırılgan damgalama ile orijinal görüntüye damga yerleştirip, damglanmış görüntüden tekrar damganın kendisinin elde edilmesi.

## Gerekli Kütüphaneler ve Modüller
- sys
- math
- itertools
- random
- PIL (pillow) for Image
- time

## Kullanılan Görseller
- ![Orijinal Görüntü] ()
- ![Damga] ()

## Nasıl Çalışır
### Damgalama
```
python3 main.py picture\child.png picture\cengmark.jpg merked_child.png
```
### Damga Çıkartma
```
python3 main.py marked_child.png mark_out.jpg
```
![Elde Edilen Damga](out_lsb_mark_out)
### Görüntüdeki Bozulmayı Elde Etme
```
python3 main.py marked_child:painted.png paint_out.jpg
```
![Bozulmuş Görüntü](https://github.com/SenaAydin7/Fragile-Watermarking/blob/main/marked_child_painted.png)

![Bozulma](out_lsb_paint_out)


Görseller telif hakkı göz önünde bulundurularak [thispersondoesnotexist.com](https://thispersondoesnotexist.com/) üzerinden alınmış gerçek insanlara ait olmayan görsellerdir.
