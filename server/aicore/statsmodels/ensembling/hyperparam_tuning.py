from sktime.forecasting.theta import ThetaForecaster
import pandas as pd
import numpy as np

from utils import MAPE


def find_best_sp(train_ts, valid_ts):
    print(train_ts.shape, valid_ts.shape)
    fh = list(np.arange(len(valid_ts)) + 1)

    def gridsearch(sps):
        best_param = (None, 100)

        for sp in sps:
            forecaster = ThetaForecaster(sp=sp)
            forecaster.fit(train_ts.reset_index(drop=True))
            y_pred = forecaster.predict(fh)
            y_pred = pd.Series(y_pred.values, index=valid_ts.index[:len(fh)])
            mape = MAPE(valid_ts, y_pred)
            if mape < best_param[1]:
                best_param = (sp, mape)

    #         print(f'sp = {sp}, MAPE = {mape}')
#         print(best_param)
        return best_param

    sps = [1, 5, 20, 250, 300, 365, int(len(train_ts)/2)]
    new_sp = gridsearch(sps)[0]
#     print(new_sp)
    new_sps = range(max(new_sp - 25, 1), min(new_sp + 25, int(len(train_ts)/2)))
    best_param = gridsearch(new_sps)
    sp = best_param[0]
    print(best_param)
    return sp


def find_best_params(train_ts, valid_ts):
    fh = list(np.arange(len(valid_ts)) + 1)

    def gridsearch(sps, lengths):
        best_param = {'mape': 100}
        for length in lengths:
            for sp in sps:
                length = max(2 * sp, length)
                truncated_train_ts = train_ts[-length:]
                forecaster = ThetaForecaster(sp=sp)
                forecaster.fit(truncated_train_ts.reset_index(drop=True))
                y_pred = forecaster.predict(fh)
                y_pred = pd.Series(y_pred.values, index=valid_ts.index[:len(fh)])
                mape = MAPE(valid_ts, y_pred)
                #                 print(f'length = {length}, sp = {sp}, mape = {mape}')
                if mape < best_param['mape']:
                    best_param = {'length': length, 'sp': sp, 'mape': mape}
        return best_param

    sps = [1, 5, 25, 50, 100, 250]
    lengths = [500, 750, 1000, 1250]

    results = gridsearch(sps, lengths)
    coarse_sp = results['sp']
    coarse_length = results['length']
    new_sps = range(max(coarse_sp - 25, 1), min(coarse_sp + 25, int(len(train_ts) / 2)))
    new_lengths = range(coarse_length - 50, coarse_length + 50, 5)
    best_params = gridsearch(new_sps, new_lengths)

    print(best_params)
    return best_params