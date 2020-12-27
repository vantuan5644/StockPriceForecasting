import csv
import os
from datetime import datetime
import vnquant.DataLoader as web
from util.setup import STOCK_CODES
import vnquant.DataLoader as web
from aicore.Prophet.Prophet import ProphetModel

#scrawl data from webpage
current_date = datetime.now().strftime("%Y-%m-%d")
# for code in STOCK_CODES:
#     # filepath = os.getcwd() + r"\dataset\\" + str(code) + datetime.now().strftime("-%dm%mm%Y-%Hm%Mm%S") + ".csv"
#     filepath = os.getcwd() + r"\dataset\\" + str(code) + ".csv"
#     loader = web.DataLoader(code, '2016-1-1', current_date)
#     data = loader.download()
#     data.columns = ["high", "low", "open", "close", "adjust", "volume"]
#     data.reset_index(drop=False, inplace=True)
#     data.to_csv(filepath, date_format='%Y%m%d')

# re-train model
ProphetModel.re_train_model()






