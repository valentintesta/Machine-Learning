import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import date
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model 
from sklearn.preprocessing import MinMaxScaler


# Configurar fechas
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Función optimizada para cargar datos
@st.cache_data
def load_data(ticker):
    return yf.download(ticker, start=START, end=TODAY)

# Interfaz de usuario
st.title('📈 Stock FAANG Data App')

stocks = ['GOOG', 'AAPL', 'MSFT', 'GME']
selected_stock = st.selectbox('Select a stock:', stocks)

# Cargar datos
data = load_data(selected_stock)

# Mostrar datos recientes
st.subheader(f'Raw data from {selected_stock}')
st.write(data.tail())


# visualistion
st.subheader('Closing Price vs Time Chart')
fig =plt.figure(figsize=(12,6))
plt.plot(data.Close)
st.pyplot(fig)


st.subheader('Closing Price vs Time Chart with 100MA')
ma100 =data.Close.rolling(100).mean()
fig =plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(data.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 200MA')
ma100 =data.Close.rolling(100).mean()
ma200 =data.Close.rolling(200).mean()
fig =plt.figure(figsize=(12,6))
plt.plot(ma100,'r')
plt.plot(ma200,'g')
plt.plot(data.Close,'b')
st.pyplot(fig)



# Load Data
data_training = pd.DataFrame(data['Close'][0:int(len(data) * 0.70)])
data_testing = pd.DataFrame(data['Close'][int(len(data) * 0.70):])

# Scaling Data
scaler = MinMaxScaler(feature_range=(0, 1))
data_training_array = scaler.fit_transform(data_training)

# Load Model
model = load_model('keras.model.h5')

# Preparing Testing Data
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)

# Apply same scaling (use transform, not fit_transform)
input_data = scaler.transform(final_df)

# Creating Test Data
x_test, y_test = [], []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i - 100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

# Model Prediction
y_predicted = model.predict(x_test)

# Correct Scaling Back
scale_factor = 1 / scaler.scale_[0]  # Extract scale factor correctly
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Plot Predictions vs Original
st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)