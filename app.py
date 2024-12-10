from pandas.io.html import read_html
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import time
import os

st.image('./image.png', width=700)


def color_negative_red(value):
    if value.startswith('-'):
        color = 'red'
    else:
        color = 'green'

    return 'color: %s' % color


website = "https://munafasutra.com/"
ex_date = datetime.now().strftime('%Y-%m-%d')

st.subheader("Gainers/Losers")
col1, col2, col3, col4 = st.columns(4)
exch = col1.selectbox("Exchange", ["nse", "bse"])
stype = col2.selectbox("Type", ["GAINERS", "LOSERS"])
value = col3.selectbox("Value", [1, 2, 3, 4, 5, 6])
duration = col4.selectbox("Time", ["WEEKLY", "MONTHLY"])
price_list = [20, 100, 300, 500, 100000]

c1, c2 = st.columns(2)
check_20 = c1.selectbox("Stocks under", price_list,
                        index=price_list.index(100000))
search = c2.text_input('Find Ticker')
if value == 0:
    url = website+"%s/top/%s/%s" % (exch, stype, duration)
else:
    url = website+"%s/top/%s/%s/%s" % (exch, stype, duration, str(value))


def get_stocks(url):
    df = pd.read_html(url)[1]
    df.dropna(axis=0, inplace=True)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    df['Ticker'] = df['Company'].apply(lambda x: str(x).split(' ')[0])
    df['Change Percent'] = df['Change Percent'].apply(
        lambda x: x.split(' ')[0])
    df['Company'] = df['Company'].apply(
        lambda x: x.split(' ', 1)[1:][0].strip())
    df = df[df['Current Price'].apply(lambda x: float(x)) < check_20]
    df = df[df['Ticker'].apply(lambda x: search.lower() in x.lower())]
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.rename(columns={'Change Percent': 'Change %',
                       'Current Price': 'Curr. Price'}, inplace=True)
    return df

my_bar = st.progress(0)
data_df = get_stocks(url)
for complete in range(100):
    my_bar.progress(complete + 1)
    time.sleep(0.001)
st.dataframe(data_df.style.set_properties(**{
    'background-color': 'white',
    'font-size': '10pt',
    'font': 'monaco'
}))


@st.cache_data()
def get_data(type):
    url = f"https://www.5paisa.com/share-market-today/{type}"
    df = pd.read_html(url)[0]
    return df


st.markdown(''' --- ''')
bonus = st.checkbox("Bonus Details")
if bonus:
    my_bar = st.progress(0)
    bonusDF = get_data('bonus')
    if not bonusDF.empty:
        for complete in range(100):
            my_bar.progress(complete + 1)
            time.sleep(0.001)
        st.subheader("Upcoming Bonus Decleared")
        st.write(bonusDF)
        st.markdown(
            '**Note:** One should have stocks in their account on `Ex-Bonus` date to get Bonus.')
    else:
        st.write("There are no upcoming bonus :(")

st.markdown(''' --- ''')
split = st.checkbox("Splits Details")
if split:
    my_bar = st.progress(0)
    splitDF = get_data('splits')
    if not splitDF.empty:
        for complete in range(100):
            my_bar.progress(complete + 1)
            time.sleep(0.001)
        st.subheader("Splits Declared")
        st.write(splitDF)
        st.markdown(
            '**Note:** One should have stocks in their account on `Split Date` date to get Splits.')
    else:
        st.write("There are no upcoming splits :(")

st.markdown(''' --- ''')
right = st.checkbox("Rights Details")
if right:
    my_bar = st.progress(0)
    rightsDF = get_data('rights')
    if not rightsDF.empty:
        for complete in range(100):
            my_bar.progress(complete + 1)
            time.sleep(0.001)
        st.subheader("Rights Issues")
        st.write(rightsDF)
        st.markdown(
            '**Note:** One should have stocks in their account on `Ex-Rights` date to get Rights.')
    else:
        st.write("There are no upcoming Rights Issue :(")

st.markdown(''' --- ''')
dividend = st.checkbox("Dividend Details")
if dividend:
    my_bar = st.progress(0)
    dvdf = get_data('dividends')
    if not dvdf.empty:
        for complete in range(100):
            my_bar.progress(complete + 1)
            time.sleep(0.001)
        st.subheader("Dividends Declared")
        st.write(dvdf)
        st.markdown(
            '**Note:** One should have stocks in their account on `Ex-Dividend` date to get dividend.')
    else:
        st.write("There are no upcoming Dividends :(")


st.sidebar.markdown('''
** STOCK FILTER **

This webapp is for finding stocks performance from 1 week to last 6 months, you can
select from the filter given. if you want to look for stocks which are consistantly growing from
last 3 months, select the filter Type: `GAINER` Value: `3` Time: `Monthly`

Similarly you can also get the stocks who are giving bonus, right , dividend and getting split with record and ex-record date.

This is getting updated on near realtime.


*** This is just a small application for those who want to get all the information on one page.***
 ''')


st.markdown('''
            ###
            ---
            \n \n \n \n \n \n
             Made by **Vikas Srivastava**
            ''')
