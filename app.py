import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

graph_plots = np.zeros(shape=1)

df = pd.read_csv('transaction.csv')

def total_amount():
    total = df['transaction'].sum() 
    return total

def getPlots():
    graph_plots = np.zeros(shape=1)
    curr_amt = 0
    for i in range(0, len(df)):
        curr_amt += df.loc[i, "transaction"]
        graph_plots = np.append(graph_plots,curr_amt)

    graph_plots = np.delete(graph_plots, 0)
    return graph_plots

def getMonthPlot():
    month_plots = np.zeros(shape=1)
    for i in range(0, 7):
        month_plots = np.append(month_plots, date.today() - relativedelta(days = (5*i)))

    month_plots = np.delete(month_plots , 0)
    month_plots =  [date.strftime('%m-%d') for date in month_plots]
    month_plots = np.flip(month_plots)
    return month_plots

def getTransactionRange():
    maxVal = df['transaction'].max()+100
    transactionRange = np.zeros(shape=1)
    maxval = maxVal//7
    amt = 0
    for i in range(1,7):
        amt += i*maxval
        transactionRange = np.append(transactionRange, amt)

    return transactionRange

with st.sidebar:
    st.title('NoMoney')
    choice = st.radio('Navigation',['Dashboard :chart_with_upwards_trend:', 'Update Finance :lower_left_ballpoint_pen:', 'Detailed View :computer:', 'Transactions :clipboard:'])

if choice == 'Dashboard :chart_with_upwards_trend:':
    st.title('Dashboard :chart_with_upwards_trend:')
    fig = plt.figure()
    plt.plot(getMonthPlot(), getTransactionRange())
    st.pyplot(plt)
    

elif choice == 'Update Finance :lower_left_ballpoint_pen:':
    st.title('Update Finance :lower_left_ballpoint_pen:')
    df_name = st.text_input('Name: ', placeholder='Transaction')
    
    toggle = st.toggle('Money is added')
    if toggle:
        df_price = st.number_input('How Muchis added: ', min_value=0)
    else:
        df_price = st.slider('How much Money did you spent: ', 0, total_amount())
        df_price = df_price - df_price - df_price
    

    df_date = st.date_input('When Did transaction take place', value=None,  max_value=date.today(), min_value=date.today() - relativedelta(years=100))
    df_category = st.selectbox('Category: ', ('-','Fees', 'Stationary', 'Addictions', 'Food & Drinks', 'Travel', 'Subcriptions', 'Other'))

    if st.button('Add'): 
        if df_name == '' or df_price == 0 or df_date == None or df_category == '-':
            st.divider()
            st.write(':red[You might have Missed something!]')
        else: 
            st.divider()
            st.write(':green[Inputs are verified!]')
            new_data = {'transaction_name': df_name, 'transaction': df_price, 'date': df_date, 'category': df_category}
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv('transaction.csv', index=False)


elif choice == 'Detailed View :computer:':
    st.title('Detailed View :computer:')

elif choice == 'Transactions :clipboard:':
    st.title('Transactions :clipboard:')
    st.data_editor(df, use_container_width=True,num_rows= "dynamic")



