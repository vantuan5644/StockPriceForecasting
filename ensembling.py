from sktime.forecasting.compose import EnsembleForecaster
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from statsmodels.tsa.stattools import acf

forecaster = EnsembleForecaster([("ses", ExponentialSmoothing(seasonal="multiplicative", sp=12)),
                                 ("holt", ExponentialSmoothing(trend="add", damped_trend=False, seasonal="multiplicative", sp=12),),
                                 ("damped", ExponentialSmoothing(trend="add", damped_trend=True, seasonal="multiplicative", sp=12),),
                                 ])
