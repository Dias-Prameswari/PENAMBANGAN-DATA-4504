import streamlit as st
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os

# Title and Description
st.title("Forex Price Prediction (XAUUSD)")
st.write("""
    Prediksi harga emas (XAUUSD) menggunakan LSTM dengan dataset lokal.
    Pilih langkah prediksi (4 jam, 1 hari, dll.) untuk melihat hasilnya.
""")

# Load pre-trained model
@st.cache_resource
def load_model_cached():
    return load_model('my_model.keras')

model = load_model_cached()

# Load local dataset
@st.cache_data
def load_local_data():
    file_path = r"C:\Users\HP\Documents\data mining\XAUUSD H1.csv"  # Path ke dataset lokal Anda
    if not os.path.exists(file_path):
        st.error(f"File tidak ditemukan di lokasi: {file_path}")
        return pd.DataFrame()
    
    try:
        data = pd.read_csv(file_path)
        data.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        data = data[['Datetime', 'Close']]
        data.set_index('Datetime', inplace=True)
        return data
    except Exception as e:
        st.error(f"Error saat membaca dataset: {e}")
        return pd.DataFrame()

# Load data
data = load_local_data()

if not data.empty:
    st.write("Data Terbaru:")
    st.write(data.head())

    # Preprocess data
    scaler = MinMaxScaler()
    prices = data["Close"].values.reshape(-1, 1)
    data_scaled = scaler.fit_transform(prices)
    sequence_length = 50

    # Test model on data
    x_test = data_scaled[-sequence_length:].reshape(1, sequence_length, 1)
    y_test = prices[-sequence_length:]
    y_pred = model.predict(x_test)
    y_pred_rescaled = scaler.inverse_transform(y_pred)

    st.write("Perbandingan pada Data Uji:")
    st.line_chart({
        "Harga Asli": y_test.flatten(),
        "Prediksi": y_pred_rescaled.flatten()
    })

    # Prediction
    steps_ahead = st.slider("Pilih langkah prediksi (misalnya 4, 24, atau 720):", 1, 720, 4)
    last_sequence = data_scaled[-sequence_length:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    future_predictions = []

    for _ in range(steps_ahead):
        pred = model.predict(last_sequence)
        future_predictions.append(pred[0, 0])
        new_input = np.append(last_sequence[:, 1:, :], [[[pred[0, 0]]]], axis=1)
        last_sequence = new_input

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Display predictions
    st.write(f"Prediksi Harga {steps_ahead} Langkah ke Depan:")
    st.line_chart(future_predictions)

    # Option to show original vs predicted
    if st.checkbox("Tampilkan Grafik Harga Asli vs Prediksi"):
        if len(prices) >= steps_ahead:
            st.line_chart({
                "Harga Asli": prices[-steps_ahead:].flatten(),
                "Prediksi": future_predictions.flatten()
            })
        else:
            st.warning("Data harga asli tidak cukup untuk dibandingkan dengan prediksi.")
else:
    st.warning("Data tidak tersedia. Periksa path atau format dataset Anda.")
