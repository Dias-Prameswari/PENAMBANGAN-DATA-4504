# PENAMBANGAN-DATA-4504
#### Tugas tentang mata kuliah penambangan data kelompok A11.4504.
#### Nama : Najma Aura Dias Prameswari.
#### NIM : A11.2022.14532.

# Apa itu Forex ? 
#### Forex (Foreign Exchange) adalah pasar global untuk perdagangan mata uang. Dalam Forex, trader memperjualbelikan pasangan mata uang seperti (EUR/USD) dengan tujuan mendapatkan keuntungan dari perubahan nilai tukar. Pasar Forex merupakan pasar keuangan terbesar di dunia dengan volume perdagangan harian mencapai triliunan dolar.

# Konsep Dasar Forex : 
- Pasangan Mata Uang : Contoh EUR/USD (Euro terhadap Dolas AS). Harga menunjukkan berapa dolar yang diperlukan untuk membeli satu Euro.
- Pergerakan Harga : Dipengarauhi oleh berbagai faktor seperti berita ekonomi, kebijakan bank sentral dan kondisi geopolitik.
- Leverage : Fitur unik di Forex yang memungkinkan trader mengelola posisi besar dengan model kecil, tetapi memiliki risiko tinggi
- Pip : Satuan terkecil dalam perubahan harga mata uang.
#### Forex digunakan oleh investor, perusahaan dan institusi untuk berbagai tujuan seperti investasi, hedging atau spekulasi.

# Keterangan nama file 
#### Prediksi Forex - Axcel : 
- Dataset : Menggunakan dataset lebih dari 8.000 data historis
- Model : Menggunakan Long Short Term Memory untuk prediksi
- Keunggulan : Model ini memiliki kemampuan prediksi yang sangat baik, karena data yang digunakan lebih lengkap
- Output : Memberikan hasil prediksi yang akurat untuk harga emas XAUUSD
- Link Deployment : https://penambangan-data-4504-xuvmlhdfrqf8jrtheldpty.streamlit.app/

#### Prediksi Forex - Mama RF : 
- Dataset : Menggunakan dataset lebih kecil, sekitar 260 data historis
- Model : Menggunakan Random Forest untuk prediksi dengan tambahan analisis teknikal (SMA,RSI,BB/Bollinger Bands)
- Hasil : Test Set MAE = 4.15, menunjukkan rata - rata kesalahan prediksi yang kecil. Visualisasi hasil prediksi sangat mendekati nilai aktual, mengindikasikan model bekerja dengan baik untuk dataset yang kecil. Tetapi meski menunjukkan hasil visual dan statistik yang baik, ukuran dataset yang kecil membatasi kemampuan model untuk digunakan pada deployment skala besar.

#### Prediksi Forex - Mama Des : 
- Dataset : Menggunakan dataset lebih kecil, sekitar 260 data historis
- Model : Menggunakan Random Forest, Logistic Regression, Decision Tree untuk menghasilkan statistik trading seperti total profit, average profit per trade dan lain sebagainya
- Hasil : Fokus pada analisis performa trading secara keseluruhan, bukan hanya prediksi harga
