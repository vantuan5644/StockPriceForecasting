# Stock Price Forecasting

The project aims to use time-series machine learning forecasting models to predict stock prices.

## Problem Statement

The project aims to solve the problem of predicting stock prices using time-series machine learning models. The goal is to develop models that can accurately forecast the future price of a stock based on its historical price data. 

## Dataset

The dataset used for the project consists of historical stock price data for various companies. The data includes features such as opening price, closing price, volume, and other financial indicators.

## Methodology

The project uses time-series forecasting models such as Theta model, Exponential Moving Average, ARIMA, Prophet, and LSTM to predict the future price of a stock based on its historical price data. 
The models are trained and tested using a time series split and evaluated using mean absolute percentage error (MAPE) as the metric.

## Results

The project has achieved promising results in predicting stock prices using the developed time-series forecasting models.

| Model           | Performance (MAPE) (%) |
|-----------------|------------------------|
| ARIMA           | 3.7088                 |
| Ensemble model  | 1.3429                 |
| Prophet         | 2.4516                 |
| LSTM            | 8.747                  |

## Future Work

Future work includes exploring the use of other time-series forecasting models and improving the accuracy of the current models.

## Requirements

The project is implemented in Python and requires the following libraries:
- pandas
- numpy
- scikit-learn
- statsmodels
- fbprophet
- tensorflow
- pytorch

## Deployment

This application is also deployed to a web app written in Flask. To run the web app, follow these steps:

1. Install the required libraries by running `pip sync requirements.txt`.
2. Run the Flask app by executing `python server/app.py`.
3. Navigate to `http://localhost:5000` in your web browser to access the web app.

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request. We welcome all contributions!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
