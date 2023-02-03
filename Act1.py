# Precio histórico de una acción
import pandas as pd
import yfinance as yf
import numpy_financial as nfp

ticker = "IBM"
df = yf.download(ticker, start="2020-02-02", end="2023-02-02")


# %% Quick Report
def dqr(data):
    cols = pd.DataFrame(list(data.columns.values),
                        columns=['Name'],
                        index=list(data.columns.values))
    dtyp = pd.DataFrame(data.dtypes, columns=['Type'])
    misval = pd.DataFrame(data.isnull().sum(),
                          columns=['N/A value'])
    presval = pd.DataFrame(data.count(),
                           columns=['Count values'])
    unival = pd.DataFrame(columns=['Unique values'])
    minval = pd.DataFrame(columns=['Min'])
    maxval = pd.DataFrame(columns=['Max'])
    mean = pd.DataFrame(data.mean(), columns=['Mean'])
    Std = pd.DataFrame(data.std(), columns=['Std'])
    Var = pd.DataFrame(data.var(), columns=['Var'])
    median = pd.DataFrame(data.median(), columns=['Median'])

    skewness = pd.DataFrame(data.skew(), columns=['Skewness'])
    kurtosis = pd.DataFrame(data.kurtosis(), columns=['Kurtosis'])

    for col in list(data.columns.values):
        unival.loc[col] = [data[col].nunique()]
        try:
            minval.loc[col] = [data[col].min()]
            maxval.loc[col] = [data[col].max()]
        except:
            pass

    # Juntar todas las tablas
    return cols.join(dtyp).join(misval).join(presval).join(unival).join(minval).join(maxval).join(mean).join(Std).join(
        Var).join(median).join(skewness).join(kurtosis)


print(dqr(df['Adj Close'].to_frame()))

df['Adj Close'].to_frame().plot()


