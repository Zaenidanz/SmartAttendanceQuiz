import os
import csv
import random
from datetime import datetime

DATA_FILE = "data_siswa.csv"
CSV_FILE = "data_siswa.csv"
GURU_PASSWORD = "Guru@12345"

# === Fungsi Mode Guru ===
def mode_guru():
    print("\n=== MODE GURU ===")
    password = input("Masukkan Password Guru: ")

    if password != GURU_PASSWORD:
        print("❌ Password salah! Akses ditolak.")
        return

    print("\n✔ Login berhasil! Menampilkan nilai siswa :\n")
    tampilkan_data_guru()


# === Tampilkan Data Lengkap ===
def tampilkan_data_guru():
    try:
        with open(CSV_FILE, "r") as file:
            lines = file.readlines()

        # langsung tampilkan isi file apa adanya (karena sudah ASCII table)
        for line in lines:
            print(line.rstrip())

    except FileNotFoundError:
        print("❌ File CSV tidak ditemukan (belum ada data).")

# === Inisialisasi file utama ===
def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama", "Tanggal", "Mapel", "Waktu Mulai", "Waktu Selesai", "Nilai"])

# === Fungsi Absensi (catat waktu mulai) ===
def absen():
    nama = input("Masukkan nama Anda: ").strip().title()
    tanggal = datetime.now().strftime("%Y-%m-%d")
    waktu_mulai = datetime.now().strftime("%H:%M:%S")

    # Pilih mapel
    if not os.path.exists("quizzes"):
        print("Folder quizzes tidak ditemukan.")
        return None, None, None, None
    files = os.listdir("quizzes")
    if not files:
        print("Belum ada file kuis di folder quizzes.")
        return None, None, None, None

    print("\nPilih Mata Pelajaran:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {os.path.splitext(f)[0].capitalize()}")

    try:
        pilih = int(input("Pilih nomor mapel: "))
        if 1 <= pilih <= len(files):
            mapel = os.path.splitext(files[pilih - 1])[0].capitalize()
        else:
            print("Pilihan tidak valid.")
            return None, None, None, None
    except ValueError:
        print("Pilihan tidak valid.")
        return None, None, None, None

    # === CEK DUPLIKAT di file ASCII ===
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.startswith("|") and not line.startswith("| Nama")]
            for l in lines:
                parts = [p.strip() for p in l.strip("|").split("|")]
                if len(parts) == 6:
                    n, tgl, mp, _, _, _ = parts
                    if n.lower() == nama.lower() and tgl == tanggal and mp.lower() == mapel.lower():
                        print(f"\n[•] {nama} sudah absen hari ini di mapel {mapel}.")
                        return None, None, None, None

    # Jika belum ada duplikat
    print(f"\n[✔] Kehadiran {nama} dicatat ({tanggal}, {mapel}, {waktu_mulai})")
    return nama, tanggal, waktu_mulai, mapel

# === Pilih Mapel ===
def pilih_mapel():
    if not os.path.exists("quizzes"):
        print("Folder quizzes tidak ditemukan.")
        return None
    files = os.listdir("quizzes")
    if not files:
        print("Belum ada file kuis di folder quizzes.")
        return None

    print("\nPilih Mata Pelajaran:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {os.path.splitext(f)[0].capitalize()}")

    try:
        pilih = int(input("Pilih nomor mapel: "))
        if 1 <= pilih <= len(files):
            return os.path.join("quizzes", files[pilih - 1])
    except ValueError:
        pass
    print("Pilihan tidak valid.")
    return None

# === Jalankan kuis pilihan ganda ===
def jalankan_kuis(nama, tanggal, waktu_mulai, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Baca semua soal dari file
    soal_data = []
    i = 0
    while i < len(lines):
        soal = lines[i]
        opsi = lines[i + 1:i + 5]
        jawaban = lines[i + 5].strip().upper() if i + 5 < len(lines) else ""
        soal_data.append((soal, opsi, jawaban))
        i += 6

    # Ambil 15 soal secara acak tanpa menampilkan info jumlahnya
    total_soal = len(soal_data)
    jumlah_dipilih = min(15, total_soal)
    soal_terpilih = random.sample(soal_data, jumlah_dipilih)

    print("\n🧩 Mulai Kuis\n")

    benar = 0
    for idx, (soal, opsi, jawaban) in enumerate(soal_terpilih, start=1):
        print(f"{idx}. {soal}")
        for o in opsi:
            print(o)
        jawab = input("Jawaban kamu (A/B/C/D): ").strip().upper()
        if jawab == jawaban:
            print("✅ Benar!\n")
            benar += 1
        else:
            print(f"❌ Salah! Jawaban benar: {jawaban}\n")

    total = len(soal_terpilih)
    nilai = round((benar / total) * 100, 2)
    waktu_selesai = datetime.now().strftime("%H:%M:%S")

    print(f"🎯 Kuis selesai. Nilai tersimpan otomatis.\n")

    mapel = os.path.splitext(os.path.basename(file_path))[0].capitalize()

    # === Simpan hasil ke tabel ASCII seperti sebelumnya ===
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file if line.strip()]
            for l in lines:
                if l.startswith("| ") and not l.startswith("| Nama"):
                    parts = [p.strip() for p in l.strip("|").split("|")]
                    if len(parts) == 6:
                        data.append(parts)

    data.append([nama, tanggal, mapel, waktu_mulai, waktu_selesai, str(nilai)])

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        file.write("📋 Data Kehadiran dan Nilai Siswa\n")
        file.write("=" * 85 + "\n")
        file.write(f"| {'Nama':<12} | {'Tanggal':<10} | {'Mapel':<12} | {'Mulai':<10} | {'Selesai':<10} | {'Nilai':<7} |\n")
        file.write("-" * 85 + "\n")
        for d in data:
            file.write(f"| {d[0]:<12} | {d[1]:<10} | {d[2]:<12} | {d[3]:<10} | {d[4]:<10} | {d[5]:<7} |\n")
        file.write("=" * 85 + "\n")

# === Lihat semua data ===
def lihat_data():
    if not os.path.exists(DATA_FILE):
        print("\n[!] Belum ada data yang tersimpan.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        lines = [line.rstrip("\n") for line in file]

    if not lines or len(lines) < 5:
        print("\n[!] Belum ada data tersimpan.")
        return

    print("\n📋 Data Kehadiran Siswa")
    print("=" * 72)
    print(f"| {'Nama':<12} | {'Tanggal':<10} | {'Mapel':<12} | {'Mulai':<10} | {'Selesai':<10} |")
    print("-" * 72)

    for line in lines:
        # cari baris yang berisi data siswa (dimulai dengan '| Nama' dilewati)
        if line.startswith("| ") and not line.startswith("| Nama"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) == 6:
                nama, tanggal, mapel, mulai, selesai, nilai = parts
                # tampilkan tanpa kolom nilai
                print(f"| {nama:<12} | {tanggal:<10} | {mapel:<12} | {mulai:<10} | {selesai:<10} |")

    print("=" * 72)

# === Menu utama ===
def main():
    init_file()
    while True:
        print("\n=== SMART ATTENDANCE QUIZ CLI ===")
        print("1. Absen & Mulai Kuis")
        print("2. Lihat Data Semua Siswa")
        print("3. Lihat Nilai Siswa (Khusus Guru)")
        print("4. Keluar")

        pilihan = input("Pilih menu (1/2/3): ").strip()

        if pilihan == "1":
            # Ambil data dari fungsi absen()
            nama, tanggal, waktu_mulai, mapel = absen()

            # Kalau hasilnya valid (bukan None)
            if nama and mapel:
                file_kuis = f"quizzes/{mapel.lower()}.txt"
                if os.path.exists(file_kuis):
                    jalankan_kuis(nama, tanggal, waktu_mulai, file_kuis)
                else:
                    print(f"\n[!] File kuis untuk mapel '{mapel}' tidak ditemukan.")
            else:
                print("\n[!] Proses absen dibatalkan atau tidak valid.")

        elif pilihan == "2":
            lihat_data()
        
        elif pilihan == "3":
            mode_guru()

        elif pilihan == "4":
            print("\nTerima kasih! Program selesai.")
            break

        else:
            print("\n[!] Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()

