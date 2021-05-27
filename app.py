from pandas.io.html import read_html
import streamlit as st
import pandas as pd
from datetime import datetime
import time


st.image('./image.png', width=700)


def color_negative_red(value):
    if value.startswith('-'):
        color = 'red'
    else:
        color = 'green'

    return 'color: %s' % color


website = "https://munafasutra.com/"

st.subheader("Gainers/Losers")
col1, col2, col3, col4 = st.beta_columns(4)
exch = col1.selectbox("Exchange", ["nse", "bse"])
stype = col2.selectbox("Type", ["GAINERS", "LOSERS"])
value = col3.selectbox("Value", [1, 2, 3, 4, 5, 6])
duration = col4.selectbox("Time", ["WEEKLY", "MONTHLY"])

if value == 0:
    url = website+"%s/top/%s/%s" % (exch, stype, duration)
else:
    url = website+"%s/top/%s/%s/%s" % (exch, stype, duration, str(value))

df = st.cache(pd.read_html)(url)[1]
df = df.rename(columns=df.iloc[0]).drop(df.index[0])
my_bar = st.progress(0)
for complete in range(100):
    my_bar.progress(complete + 1)
    time.sleep(0.001)
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


st.markdown(''' --- ''')
bonus = st.checkbox("Bonus Details")
if bonus:
    my_bar = st.progress(0)
    bonusDF = get_data('bonus')
    for complete in range(100):
        my_bar.progress(complete + 1)
        time.sleep(0.001)
    st.subheader("Bonus Decleared")
    st.write(bonusDF)

st.markdown(''' --- ''')
split = st.checkbox("Splits Details")
if split:
    my_bar = st.progress(0)
    splitDF = get_data('splits')
    for complete in range(100):
        my_bar.progress(complete + 1)
        time.sleep(0.001)
    st.subheader("Splits Declared")
    st.write(splitDF)

st.markdown(''' --- ''')
right = st.checkbox("Rights Details")
if right:
    my_bar = st.progress(0)
    rightsDF = get_data('rights')
    for complete in range(100):
        my_bar.progress(complete + 1)
        time.sleep(0.001)
    st.subheader("Rights Issues")
    st.write(rightsDF)

st.markdown(''' --- ''')
dividend = st.checkbox("Dividend Details")
if dividend:
    my_bar = st.progress(0)
    dvdf = get_data('dividends_declared')
    for complete in range(100):
        my_bar.progress(complete + 1)
        time.sleep(0.001)

    st.subheader("Dividends Declared")
    st.write(dvdf)


st.markdown('''
            ### 
            ---
            \n \n \n \n \n \n 
             Made by ** Vikas Srivastava **
            ''')
