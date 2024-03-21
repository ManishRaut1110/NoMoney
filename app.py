import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

graph_plots = np.zeros(shape=1)

df = pd.read_csv('transaction.csv')

total_investment = float(df['transaction'].sum())
mean_investment = float(df['transaction'].mean())
mode_investment = float(df['transaction'].mode().iloc[0])
median_investment = float(df['transaction'].median())

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
    st.image('Resource/MIT-WPU-logo-419026232.png', use_column_width=True)
    st.title('Transaction Application')
    choice = st.radio('Navigation',['Dashboard :chart_with_upwards_trend:', 'Update Finance :lower_left_ballpoint_pen:', 'Detailed View :computer:', 'Transactions :clipboard:'])

if choice == 'Dashboard :chart_with_upwards_trend:':
    st.title('Dashboard :chart_with_upwards_trend:')
    
    total1, total2, total3, total4 = st.columns(4, gap='medium')

    with total1:
        st.info("Total Investment", icon="📌")
        st.metric(label="Sum ₹", value=f"{total_investment:,.0f}")

    with total2:
        st.info("Most Frequent", icon="📌")
        st.metric(label="Mode ₹", value=f"{mode_investment:,.0f}")

    with total3:
        st.info("Average", icon="📌")
        st.metric(label="Average ₹", value=f"{mean_investment:,.0f}")

    with total4:
        st.info("Central Earnings", icon="📌")
        st.metric(label="Median ₹", value=f"{median_investment:,.0f}")
    
    st.markdown("---")
    
    # Simple Bar Graph
    st.subheader("Simple Bar Graph")
    plt.bar(['Mode', 'Mean', 'Median'], [mode_investment, mean_investment, median_investment])
    st.pyplot(plt)

    # Line chart divided by category
    st.subheader("Line Chart by Category")
    fig, ax = plt.subplots()
    for category, group in df.groupby('category'):
        group = group.set_index('date')  # Set date as index for each category
        group = group.reindex(pd.date_range(group.index.min(), group.index.max(), freq='D'), fill_value=0)  # Fill missing dates with zeros
        ax.plot(group.index, group['transaction'], label=category)
    ax.set_title('Line Chart by Category')
    ax.legend()
    st.pyplot(fig)

    # Pie Chart by Category
    st.subheader("Pie Chart by Category")
    category_sum = df.groupby('category')['transaction'].sum()
    category_sum = category_sum[category_sum >= 0]  # Exclude negative values
    plt.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
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
    st.sidebar.header("Filter Transaction")
    selected_categories = st.sidebar.multiselect(
    "Select Transaction Category",
    options=df["category"].unique()
    )
    filtered_df = df[df["category"].isin(selected_categories)]
    
    def filter():
        with st.expander("Tabular"):
            showData=st.multiselect('Filter : ',filtered_df.columns,default=[])
            st.write(filtered_df[showData])
    filter()
    st.data_editor(df, use_container_width=True,num_rows= "dynamic")
