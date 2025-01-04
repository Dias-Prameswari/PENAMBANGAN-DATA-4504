import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import gdown

# Judul aplikasi
st.title("Prediksi Harga Emas (XAUUSD)")
st.write("""
    Aplikasi ini memprediksi harga emas menggunakan model LSTM dan data historis.
    Anda dapat memilih langkah prediksi untuk 4 jam, 1 hari, atau 1 bulan ke depan.
""")

# Fungsi untuk mengunduh file dari Google Drive
@st.cache_resource
def download_file_from_gdrive(file_id, output_name):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_name, quiet=False)

# Unduh dataset dari Google Drive
dataset_id = "17GEo3L16A7KUsPPLmW-za60L40l20Ne3"  # ID dataset
model_id = "1TTRIgUOcRFJffD_TLrM1lL6LVd91qqla"  # ID model

download_file_from_gdrive(dataset_id, "XAUUSD_H1.csv")
download_file_from_gdrive(model_id, "my_model.keras")

# Load model
@st.cache_resource
def load_model_cached():
    return load_model("my_model.keras")

model = load_model_cached()

# Baca dataset
file_path = "XAUUSD_H1.csv"
try:
    data = pd.read_csv(file_path)
    data.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
    data.set_index('Datetime', inplace=True)
    data.dropna(inplace=True)

    st.write("Dataset yang Dimuat:")
    st.dataframe(data.head())

    # Preprocessing
    scaler = MinMaxScaler()
    prices = data[['Close']].values  # Hanya menggunakan kolom Close
    data_scaled = scaler.fit_transform(prices)
    sequence_length = 50  # Panjang input timesteps

    # Prediksi Data Uji
    x_test = data_scaled[-sequence_length:]
    x_test = np.expand_dims(x_test, axis=0)
    y_test = prices[-sequence_length:]
    y_pred = model.predict(x_test)
    y_pred_rescaled = scaler.inverse_transform(y_pred)

    # Menampilkan grafik actual vs prediksi
    st.write("Perbandingan Harga Aktual vs Prediksi:")
    fig, ax = plt.subplots()
    ax.plot(y_test, label="Harga Aktual", color="blue")
    ax.plot(y_pred_rescaled, label="Prediksi", color="red")
    ax.legend()
    st.pyplot(fig)

    # Prediksi harga ke depan
    steps_mapping = {
        "4 Jam ke Depan": 4,
        "1 Hari ke Depan": 24,
        "1 Bulan ke Depan": 720
    }

    pred_choice = st.selectbox(
        "Pilih Langkah Prediksi:",
        list(steps_mapping.keys())
    )
    steps_ahead = steps_mapping[pred_choice]

    if st.button("Proses Prediksi"):
        last_sequence = data_scaled[-sequence_length:]
        last_sequence = np.expand_dims(last_sequence, axis=0)
        future_predictions = []

        for _ in range(steps_ahead):
            pred = model.predict(last_sequence)
            future_predictions.append(pred[0, 0])
            new_input = np.append(last_sequence[:, 1:, :], [[[pred[0, 0]]]], axis=1)
            last_sequence = new_input

        future_predictions_rescaled = scaler.inverse_transform(
            np.array(future_predictions).reshape(-1, 1)
        )

        st.write(f"Prediksi Harga untuk {pred_choice}:")
        fig, ax = plt.subplots()
        ax.plot(future_predictions_rescaled, label=f"Prediksi Harga ({pred_choice})", color="green")
        ax.set_title(f"Prediksi Harga ({pred_choice})")
        ax.set_xlabel("Steps Ahead")
        ax.set_ylabel("Price")
        ax.legend()
        st.pyplot(fig)

except FileNotFoundError:
    st.error(f"File tidak ditemukan di lokasi: {file_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
