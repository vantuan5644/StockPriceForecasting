import pandas as pd 
import numpy as np 
import datetime

def get_datetime_value_from_df(dataframe: pd.DataFrame):
    # preprocessing dataframe
    df = dataframe[["date", "close"]]
    df.rename(columns={"date": "time", "close": "price"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d", errors="coerce")
    df.sort_values(by="time", inplace=True, ascending=True)
    df.reset_index(inplace=True, drop=True)

    # extract time and stock price
    results = []
    for i in range(len(df)):
        results.append({"time": df.loc[i, "time"].strftime("%d/%m/%Y %H:%M:%S"), "price": df.loc[i, "price"]})

    return results


def get_timestamp_from_filename_model(filename_model):
    filename_model = filename_model.replace(".csv", "")
    temp = filename_model.split("-")
    ddmmyyyy = temp[1].replace("m","/")
    hhmmss = temp[2].replace("m",":")
    return f"{ddmmyyyy} {hhmmss}"