import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

graph_plots = np.zeros(shape=1)

df = pd.read_csv('transaction.csv')

total_investment = round(float(df['transaction'].sum()), 2)
mean_investment = round(float(df['transaction'].mean()), 2)
mode_investment = round(float(df['transaction'].mode().iloc[0]), 2)
median_investment = round(float(df['transaction'].median()), 2)



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
    # st.image('Resource/MIT-WPU-logo-419026232.png', use_column_width=True)
    st.title('Transaction Application')
    choice = st.radio('Navigation',['Dashboard :chart_with_upwards_trend:', 'Update Finance :lower_left_ballpoint_pen:', 'Transactions :clipboard:'])

if choice == 'Dashboard :chart_with_upwards_trend:':
    st.title('Dashboard :chart_with_upwards_trend:')
    
    total1, total2, total3, total4 = st.columns(4, gap='medium')

    with total1:
        st.info("Total Investment", icon="📌")
        if total_investment>=0: 
            st.header(f':green[{total_investment}]')
        else:
            st.header(f':red[{total_investment}]')

    with total2:
        st.info("Most Frequent", icon="📌")
        if mode_investment>=0: 
            st.header(f':green[{mode_investment}]')
        else:
            st.header(f':red[{mode_investment}]')

    with total3:
        st.info("Average Spending", icon="📌")
        if mean_investment>=0: 
            st.header(f':green[{mean_investment}]')
        else:
            st.header(f':red[{mean_investment}]')

    with total4:
        st.info("Central Earnings", icon="📌")
        if median_investment>=0: 
            st.header(f':green[{median_investment}]')
        else:
            st.header(f':red[{median_investment}]')
    
    st.markdown("---")
    
    # Simple Bar Graph
    df['date'] = pd.to_datetime(df['date'])

# Group transactions by date and category, and sum them up
    df_grouped = df.groupby(['date', 'category'])['transaction'].sum().unstack(fill_value=0)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot each category as a separate line
    for category in df_grouped.columns:
        plt.plot(df_grouped.index, df_grouped[category], marker='o', linestyle='-', label=category)

    plt.title('Transaction Trend by Category')
    plt.xlabel('Date')
    plt.ylabel('Transaction Amount')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
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

elif choice == 'Transactions :clipboard:':
    st.title('Transactions :clipboard:')

    with st.expander("Tabular"):
        selected_categories = st.multiselect(
        "Select Transaction Category",
        options=df["category"].unique())
        filtered_df = df[df["category"].isin(selected_categories)]
        showData=st.multiselect('Filter : ',filtered_df.columns,default=[])

    if selected_categories==[]:
        st.data_editor(df, use_container_width=True,num_rows= "dynamic")
    else: 
        if showData==[]:
            st.dataframe(filtered_df)
        else:
            st.dataframe(filtered_df[showData])

