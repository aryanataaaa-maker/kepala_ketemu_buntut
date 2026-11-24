# Name : Nataarya 
# Desc : Simple snake game for experiment and self learn


# Modul 1 : Konstanta, dipisah untuk memudahkan mengubah ukuran dari tiap variabel seperti size layar.
import sys      # digunakan untuk berinteraksi dengan sistem operasi, seperti untuk menutup game dengan bersih.
import random   # digunakan untuk menghasilkan angka atau pilihan acak semisak kemunculan buah di game snake.
import pygame   # library khusus untuk membuat game seperti menangkap perintah keyboard ; mouse, menggambar karakter/objek, dll.

# ukuran layar (pixel)
LEBAR = 600
TINGGI = 400 
UKURAN = 20     # ini berarti ukuran ular satu kotaknya adalah 20 x 20 
FPS = 10        # semakin besar nilai semakin cepat gerakan game(terutama ular disini)

# warna dalam format (merah, hijau, biru)
HITAM = (0, 0, 0)
PUTIH = (255, 255, 255)
HIJAU = (0, 200, 0)
MERAH = (220, 0, 0)

# Arah gerak, dalam bentuk perpindahan (x,y)
KIRI  = (-UKURAN,0)     
KANAN = (UKURAN,0)
ATAS  = (0,-UKURAN) # kartesian terbalik, semakin minus semakin ke atas
BAWAH = (0,UKURAN)

# Modul 2 : Ular dan Makanan
def buat_makanan(ular):  #membuat sebuah fungsi buat_makanan dengan masukan atau parameter ulat (pixel badan ular) sebagai bahan pengecekan
    """Cari posisi acak untuk makanan yang tidak menimpa badan ular."""
    while True: # melakukan perulangan tanpa henti untuk mencari tempat baru (tidak berpotongan atau tertimpa dengan pixel ular)
        x = random.randrange(0, LEBAR, UKURAN) # muncul secara acak di bidang horizontal dengan batasan LEBAR(tempat main kita) dan sebesar UKURAN (satuan kotak yang disepakati[20])
        y = random.randrange(0, TINGGI, UKURAN) # muncul secara acak di bidang vertikal dengan batasan LEBAR(tempat main kita) dan sebesar UKURAN (satuan kotak yang disepakati[20])
        if (x,y) not in ular :  # cek apakah petak itu sudah ada badan ular atau tidak
            return (x,y)        # kalau tidak tertimpa badan ular, fungsi mengembalikan nilai koordinat untuk menaruh buah, jika tidak, kembali ke perulangan untuk mencari petak kosong

def mulai_ulang(): 
    """Menyiapkan kondisi awal game : digunakan saat game baru mulai dan restart"""
    ular = [(300, 200), (280, 200), (260, 200)] # ular merupakan list of coordinates, isinya merupakan koordinat dimana ular berpijak di tempat main, disini ular menghadap kanan karena index 0 kepala
    arah = KANAN    # Menyimpan status arah gerak pertama ular ke dalam variabel arah(mengambil [20,0]) 
    makanan = buat_makanan(ular) # panggil fungsi buat_makanan dengan posisi ular sekarang
    skor = 0    # Inisialisasi variabel skor 
    return ular, arah, makanan, skor    # Mengembalikan variabel ular, arah, makanan, dan skor

# Loop untuk Modul 5 agar ular tidak langsung bergerak ke arah yang berlawanan


# Modul 4 : Mengatur visual seluruh game

def gambar(layar, ular, makanan, skor, font):
    layar.fill(HITAM) # bersihkan layar terlebih dahulu 

    # Gambar setiap kotak ular 
    for x, y in ular: 
        pygame.draw.rect(layar, HIJAU, (x, y, UKURAN, UKURAN))

    # Gambar maknan 
    x, y = makanan
    pygame.draw.rect(layar, MERAH, (x, y, UKURAN, UKURAN))

    # Tulis skor di pojok kiri atas 
    teks = font.render(f"Skor: {skor}", True, PUTIH)
    layar.blit(teks, (10, 10))

    pygame.display.flip() # Tampilkan hasil gambar ke layar

    
    
    
def main () :
        pygame.init()
        layar = pygame.display.set_mode((LEBAR, TINGGI))
        pygame.display.set_caption("Snake")
        jam = pygame.time.Clock()
        font = pygame.font.SysFont(None, 30)

        ular, arah, makanan, skor = mulai_ulang()
        selesai = False # True kalau game over 

        while True: 
            # 1. BACA INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:    # cek apakah ada tombol keyboard yang baru ditekan pemain 
                    if event.key == pygame.K_UP and arah != BAWAH:
                        arah = ATAS 
                    elif event.key == pygame.K_DOWN and arah != ATAS:
                        arah = BAWAH
                    elif event.key == pygame.K_LEFT and arah != KANAN:
                        arah = KIRI
                    elif event.key == pygame.K_RIGHT and arah != KIRI:
                        arah = KANAN
                    elif event.key == pygame.K_r and selesai:
                        ular, arah, makanan, skor = mulai_ulang()
                        selesai = False

            # 2. UPDATE LOGIKA (hanya kalau belum game over)
            if not selesai: 
                dx, dy = arah 
                kepala_x, kepala_y = ular[0]
                kepala_baru = (kepala_x + dx, kepala_y + dy)

                # Cek tabrakan 
                di_luar_layar = not (0 <= kepala_baru[0] < LEBAR and 
                                     0 <= kepala_baru[1] < TINGGI)
                kena_badan = kepala_baru in ular

                if di_luar_layar or kena_badan:
                    selesai = True
                else:
                    ular.insert(0, kepala_baru) # kepala maju 
                    if kepala_baru == makanan:
                        skor += 1
                        makanan = buat_makanan(ular)  # makanan baru, ekor tidak dibuang
                    else: 
                        ular.pop() # tidak makan = ukuran tetap, ekor dibuang supaya panjangnya tetap

            # 3. GAMBAR
            gambar (layar, ular, makanan, skor, font)

            if selesai: 
                teks = font.render("Game over! Tekan R untuk main lagi", True, PUTIH)
                layar.blit(teks, (LEBAR // 2 - teks.get_width() // 2, TINGGI // 2))
                pygame.display.flip()

            # TUNGGU
            jam.tick(FPS)

if __name__ == "__main__":
    main()

            