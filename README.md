# Bike Sharing Dataset: Dicoding Submission

## Live Dashboard
https://submission-bike-sharing-analysis-dicoding-patricia-ho.streamlit.app

## Overview Projek
Proyek ini dikerjakan sebagai syarat penyelesaian kursus "Belajar Analisis Data dengan Python" dari Dicoding. Disini saya menganalisis Bike Sharing Dataset dimana fokus saya adalah melihat tren, pola, serta korelasi antar variabel. 

## Penjelasan General
Proyek ini mencermati tren persewaan sepeda dan berbagai faktor yang mungkin mempengaruhinya. Disini akan melihat bagaimana hari libur, musim, cuaca, dan suhu berperan dalam seberapa sering orang menyewa sepeda. Disini juga akan melacak bagaimana tren ini berubah seiring waktu dan mengidentifikasi kapan persewaan sepeda paling populer dan paling tidak populer. Pengaruh kecepatan angin terhadap jumlah sewa juga akan dipertimbangkan. Selain itu, akan ada juga membandingkan penggunaan antara pengendara biasa dan anggota terdaftar, dan mencari tahu waktu tersibuk untuk persewaan sepeda. Studi ini akan memberi gambaran yang lebih jelas tentang apa yang mempengaruhi kebiasaan penyewaan sepeda, yang dapat membantu program bike-sharing memenuhi kebutuhan penggunanya dengan lebih baik.

## Sumber Data
Sumber data yang digunakan berasal dari Dicoding, ada didalam folder Data dengan 2 file (day.csv dan hour.csv)

## Library yang digunakan
- Streamlit
- Pandas
- Numpy
- Matplotlib
- Seaborn
- Ipython

## 
- Penyewaan sepeda naik dan turun seiring musim, menjadi lebih sibuk di beberapa musim dan lebih tenang di musim lain.
- Cuaca yang baik berarti lebih banyak persewaan sepeda, terutama saat cuaca tidak terlalu panas atau terlalu dingin.
- Orang-orang lebih banyak menyewa sepeda pada suhu yang hangat, dan toleransi suhu yang dirasakan oleh manusia juga termasuk variabel yang penting.
- Aspek kecepatan angin tidak menghentikan orang untuk menyewa sepeda.
- Pengendara biasa dan pengguna yang terdaftar dalam menggunakan sepeda secara berbeda, dan melihat kapan masing-masing kelompok suka bersepeda.
- Menemukan waktu tersibuk dalam sehari untuk menyewa sepeda, yang biasanya terjadi pada saat orang berangkat kerja atau pulang.
- Dan lainnya!

## Cara menjalankan Dashboard dengan Streamlit

Untuk menjalankan dashboard Bike Sharing, ikuti langkah berikut:

### Setup Environment

1. **Buat dan aktifkan Python Environment**:
   - Jika menggunakan Conda (pastikan [Conda](https://docs.conda.io/en/latest/) telah diinstal):
     ```
     conda create --name bike-sharing python=3.12
     conda activate bike-sharing
     ```
   - Jika menggunakan venv (standar tool dari Python environment):
     ```
     python -m venv bike-sharing
     source bike-sharing/bin/activate  # Di windows gunakan `bike-sharing\Scripts\activate`
     ```

2. **Install library atau package yang diperlukan**:
   - Library atau package berikut diperlukan untuk menjalankan analisis dan dashboard:
     ```
     pip install pandas numpy matplotlib seaborn streamlit ipython
     ```

     atau bisa dengan
     ```
     pip install -r requirements.txt
     ```
### Menjalankan Streamlit

1. **Arahkan ke Direktori Proyek** tempat `dashboard.py` berada.

2. **Jalankan Aplikasi Streamlit**:
    ```
    streamlit run dashboard.py
    ```

### Catatan:

- Python notebook (`notebook.ipynb`) yang berisi keseluruhan analisis sudah ada dalam repo ini, Silahkan dicek:D

---

## Tentang Saya
- **Nama:** :  Patricia Ho
- **Email:** :  patricia.ho@student.pradita.ac.id
- **ID Dicoding** : [patricia_ho_rKsF](https://www.dicoding.com/users/patricia_ho_rksf)

