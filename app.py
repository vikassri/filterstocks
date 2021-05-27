from pandas.io.html import read_html
import streamlit as st
import pandas as pd
from datetime import datetime


def color_negative_red(value):
    if value.startswith('-'):
        color = 'red'
    else:
        color = 'green'

    return 'color: %s' % color


website = "https://munafasutra.com/"

st.header("Stocks Details")
st.subheader("Gainers/Losers")
col1, col2, col3, col4 = st.beta_columns(4)
exch = col1.selectbox("Exchange", ["nse", "bse"])
stype = col2.selectbox("Type", ["GAINERS", "LOSERS"])
value = col3.selectbox("Value", [1, 2, 3, 4, 5, 6])
time = col4.selectbox("Time", ["WEEKLY", "MONTHLY"])

if value == 0:
    url = website+"%s/top/%s/%s" % (exch, stype, time)
else:
    url = website+"%s/top/%s/%s/%s" % (exch, stype, time, str(value))

df = st.cache(pd.read_html)(url)[1]
df = df.rename(columns=df.iloc[0]).drop(df.index[0])
st.dataframe(df.style.applymap(color_negative_red, subset=[
    'Change Percent']))


def get_data(type):
    year = datetime.now().year
    url = f"https://www.moneycontrol.com/stocks/marketinfo/{type}/index.php?sel_year={year}"
    tables = pd.read_html(url)
    df = tables[1]
    df[0] = df[0].apply(lambda x: x.split("Add")[0])
    if type != "splits":
        df = df.rename(columns=df.iloc[1]).drop(df.index[0]).drop(df.index[1])
    else:
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


bonus = st.checkbox("Bonus Details")
if bonus:
    st.subheader("Bonus Decleared")
    st.write(get_data('bonus'))

split = st.checkbox("Splits Details")
if split:
    st.subheader("Splits Declared")
    st.write(get_data('splits'))

right = st.checkbox("Rights Details")
if right:
    st.subheader("Rights Issues")
    st.write(get_data('rights'))

dividend = st.checkbox("Dividend Details")
if dividend:
    st.subheader("Dividends Declared")
    st.write(get_data('dividends_declared'))
