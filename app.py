from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Mengimpor dataset dari file Excel
file_path = 'Kasus Komstat.xlsx'
df = pd.read_excel(file_path)

# Fungsi cek_syarat_lulus untuk mengevaluasi syarat kelulusan mahasiswa
def cek_syarat_lulus(mahasiswa):
    mata_kuliah_semester_5 = [
        'Data Mining', 'Komputasi Statistik', 'Teori Optimasi',
        'Visualisasi Data dan Informasi', 'Pembelajaran Mesin', 'Kecerdasan Buatan'
    ]

    result = []

    for mata_kuliah in mata_kuliah_semester_5:
        if mata_kuliah == 'Data Mining' and mahasiswa['Struktur Data'] not in ['C', 'BC', 'B', 'AB', 'A']:
            result.append(f"{mata_kuliah} tidak dapat diambil. Disarankan untuk mengulang Struktur Data.")
        elif mata_kuliah == 'Komputasi Statistik' and mahasiswa['ADS'] not in ['C', 'BC', 'B', 'AB', 'A']:
            result.append(f"{mata_kuliah} tidak dapat diambil. Disarankan untuk mengulang Analisis Data Statistika.")
        elif mata_kuliah == 'Teori Optimasi' and mahasiswa['Metnum'] not in ['C', 'BC', 'B', 'AB', 'A']:
            result.append(f"{mata_kuliah} tidak dapat diambil. Disarankan untuk mengulang Metode Numerik.")
        # Tambahkan pengecekan untuk mata kuliah lainnya di sini sesuai logika yang sama

        else:
            result.append(f"Dapat mengambil mata kuliah {mata_kuliah}.")

    return result

# Route untuk halaman utama
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama_mahasiswa = request.form['mahasiswa']
        nilai_mahasiswa = df[df['NAMA'] == nama_mahasiswa][['Struktur Data', 'ADS', 'Metnum', 'Alpro', 'SSD', 'Alstrat']].iloc[0]
        hasil = cek_syarat_lulus(nilai_mahasiswa)
        return render_template('result.html', nama_mahasiswa=nama_mahasiswa, hasil=hasil)
    else:
        unique_mahasiswa = df['NAMA'].unique().tolist()
        return render_template('index.html', unique_mahasiswa=unique_mahasiswa)

if __name__ == '__main__':
    app.run(debug=True)