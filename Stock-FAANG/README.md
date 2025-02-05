# Stock Price Prediction with LSTM

## Introduction
This project aims to create a web application that predicts stock prices using an LSTM (Long Short-Term Memory) model trained on historical stock data. The application allows users to visualize stock data and see predictions made by the model.

## Technologies Used
- Python
- Streamlit
- TensorFlow
- Keras
- Yahoo Finance API
- Matplotlib
- NumPy
- Pandas



## Model Training
The LSTM model is trained on historical stock price data. The model is saved as `keras.model.h5` after training, which is then loaded in the application for making predictions.

## Visualizations
The application provides the following visualizations:
- Raw stock price data
- Closing price charts
- Moving averages (100-day and 200-day)
- Predictions vs. original prices

## Conclusion
This project demonstrates the use of LSTM models for stock price prediction and provides a user-friendly interface for visualizing stock data. Future improvements could include adding more features, such as additional stock indicators or enhancing the model's accuracy.
