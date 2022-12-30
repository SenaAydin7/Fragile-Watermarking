import sys
import math
import itertools
import random
from PIL import Image
import time

items = list(range(0, 40))
def resize(inputpath):
    image = Image.open(inputpath)
    new_image = image.resize((256, 256))
    resize_path = "picture/human_256.png"
    new_image.save(resize_path)
    return resize_path
def resize2(inputpath):
    image = Image.open(inputpath)
    new_image = image.resize((256, 256))
    resize_path = "picture/cengmark.jpg"
    new_image.save(resize_path)
    return resize_path

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    total = len(iterable)
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    printProgressBar(0)

    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    print()

HEIGHT = 256
WIDTH = 256
size = HEIGHT*WIDTH
order = []
for i in range(size):    #[0-65536]
    order.append(i)



def encrypt(plain, key):
    matris = []
    for i in range(len(plain)):
        matris.append((plain[i] + ord(key[i % len(key)])) % 256)
    #print(matris)
    return matris


def takelsb(image, width, order,mode=1):
    lsb_list = []
    px = image.load()
    k = 0
    cur = 0
    for pos in order:
        i = pos / width
        j = pos % width
        if (mode == 1):
            cur |= (px[i % image.width, j % image.height] & 1) << k
        else:
            cur |= (px[i % image.width, j % image.height][0] & 1) << k
        k += 1
        if (k >= 8):
            lsb_list.append(cur)
            k = 0
            cur = 0
    if (k > 0):
        lsb_list.append(cur)
    return lsb_list



def in_lsb(inputpath, watermarkpath, outputpath):
    photo = Image.open(resize(inputpath))
    watermark = Image.open(resize2(watermarkpath)).convert("1")
    output = Image.new(photo.mode, photo.size)
    px_photo = photo.load()
    px_output = output.load()
    plain_photo = takelsb(watermark, photo.width, order,1)
    #print(len(plain_photo))
    key = input("Parola Giriniz: ")
    if(key=="1234"):
        cipher = encrypt(plain_photo, key)
        k = 0
        mod = watermark.width * watermark.height
        for pos in order:
            i = pos / photo.width
            j = pos % photo.width
            p = list(px_photo[i, j])
            p[0] = (p[0] & 0b11111110) | ((cipher[int(k / 8)] >> (k % 8)) & 1)
            k = (k + 1) % mod
            px_output[i, j] = tuple(p)
        for item in progressBar(items, prefix='DAMGALANIYOR:', suffix='', length=50):
            time.sleep(0.1)
        print("DAMGALAMA BAŞARILI!")
        output.save(outputpath)
        output.show()
    else:
        error = "parola yanlış"
        return error



def psnr(watermarkedpath, plainpath):

    watermarked = Image.open(watermarkedpath)
    plain = Image.open(plainpath)
    imwat= watermarked.load()
    impla=plain.load()
    PIXEL_MAX = 225.0
    wat_mean_sum = 0
    pla_mean_sum = 0
    for i in range(watermarked.width):
        for j in range(watermarked.height):
            wat = imwat[i, j]
            pla = impla[i, j]

            p_a_mean = (wat[0] + wat[1] + wat[2]) / 3
            wat_mean_sum += p_a_mean

            p_b_mean = (pla[0] + pla[1] + pla[2]) / 3
            pla_mean_sum += p_b_mean

    final_sum =math.pow((pla_mean_sum-wat_mean_sum), 2)
    # print(p_a_mean_sum)
    # print(final_sum)
    rms = (math.sqrt(final_sum / (watermarked.width * watermarked.height) / 3))
    PSNR = 20 * math.log10(PIXEL_MAX / rms)
    print("PSNR: " + str(PSNR))
    return PSNR




def decrypt(matris, key):
    plain = []
    for i in range(len(matris)):
        plain.append((matris[i] + 256 - ord(key[i % len(key)])) % 256)
    return plain


def out_lsb(inputpath, outputpath):
    photo = Image.open(inputpath)
    lsb = Image.new("1", photo.size);
    px_lsb = lsb.load()

    key = str(input("Parola Giriniz: "))
    cipher = takelsb(photo, photo.width, order,0)
    plain = decrypt(cipher, key)

    k = 0
    for pos in order:
        i = pos / photo.width
        j = pos % photo.width
        px_lsb[i, j] = ((plain[int(k / 8)] >> (k % 8)) & 1)
        k = (k + 1)
    lsb.save(outputpath);
    lsb.show();




def main():
    cmd = input("Damgalamak için (d) / Çıkarmak için (ç)")
    if cmd == 'd':
        in_lsb(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
        print(sys.argv[1]," ögesi " ,sys.argv[2] ," ile damgalandı.")
        print("Oluşan damgalı görsel", sys.argv[3]," olarak kaydedildi.")



        for i in range(3):
            print(" ")
        for item in progressBar(items, prefix='PSNR hesaplanıyor:', suffix='', length=50):
            time.sleep(0.1)
        psnr(str(resize(sys.argv[1])), str(sys.argv[3]))


    else:
        print("Damgalanmış görsel:", sys.argv[1])
        out_lsb(str(sys.argv[1]),"out_lsb_" + str(sys.argv[2]))

if __name__ == '__main__':
    main()
