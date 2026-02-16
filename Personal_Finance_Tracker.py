import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

# title of the web app
st.title("💰 Personal Finance Tracker")
st.write('Welcome to the app!')

# Initialize session state
if "transactions" not in st.session_state:
    try:
        df = pd.read_csv("transactions.csv")
        st.session_state.transactions = df.to_dict("records")
    except:
        st.session_state.transactions = []

# Sidebar to add transactions
st.sidebar.header("Add transactions")

transactions_type = st.sidebar.selectbox('Type',['Income','Expense'])
amount = st.sidebar.number_input('Amount',min_value = 0.0)
category = st.sidebar.selectbox('Category',['Rent','Food','Others'])
transaction_date = st.sidebar.date_input('date',date.today())

if st.sidebar.button('Add'):
    transactions = {
        "type" : transactions_type,
        "amount" : amount,
        "category" : category,
        "date" : transaction_date
        
    }
    st.session_state.transactions.append(transactions)
    pd.DataFrame(st.session_state.transactions).to_csv('transactions.csv',index=False)

    st.sidebar.success('Transactions Added!')


# Convert to dataframe

if st.session_state.transactions:
    df= pd.DataFrame(st.session_state.transactions)

    # Convert date to datetime column
    df['date']= pd.to_datetime(df['date'])
    
    # Month selector
    selected_month = st.selectbox(
        'Select_Month',
        sorted(df['date'].dt.to_period('M').astype(str).unique())
    )

    # Filtered data based on selected month

    filtered_df = df[df['date'].dt.to_period('M').astype(str)== selected_month]
    
    # Calculations

    total_income = filtered_df[filtered_df['type']=='Income']['amount'].sum()
    total_expense = filtered_df[filtered_df['type']=='Expense']['amount'].sum()
    savings = total_income - total_expense
    
    # Budgeting
    st.subheader('Monthly Budget')

    budget = st.number_input('Set Monthly Budget',min_value = 0.0)

    if budget > 0:
        remaining = budget - total_expense
        st.write('Remaining Balance is', f'${remaining:.2f}')

        progress = total_expense / budget

        if progress < 0:
            progress = 0
        elif progress > 0:
            progress = 1

        st.progress(progress)

    else:
        st.info('Please enter the budget to see if progress.')

        
    if total_income>0:
        savings_rate = (savings/total_income)*100
    else:
        savings_rate = 0.0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total_Income',f'${total_income:.2f}')
    col2.metric('Total_Expense',f'${total_expense:.2f}')
    col3.metric('Total_Savings',f'${savings:.2f}')
    col4.metric('Savinds_Rate',f'{savings_rate:.2f}%')

    st.subheader('All Transactions')
    st.dataframe(filtered_df)

    # Delete transactions
    st.subheader('Delete Transactions')

    if not filtered_df.empty:
        delete_index = st.number_input(
            'Enter index to delete',
            min_value=0,
            max_value=len(st.session_state.transactions)-1,
            step=1
        )

    if st.button('Delete Transaction'):

        st.session_state.transactions.pop(delete_index)

        # Update CSV
        pd.DataFrame(st.session_state.transactions).to_csv(
            'transactions.csv',
            index=False
        )

        st.success('Deleted Successfully!')
        st.rerun()


    st.subheader('Expense Breakdown')
    expense_df = df[df['type']=='Expense']

    if not expense_df.empty:
        category_totals = expense_df.groupby('category')['amount'].sum()

        fig, ax = plt.subplots()
        ax.pie(category_totals, labels= category_totals.index, autopct= "%1.1f%%")
        ax.set_title('Expense by category')

        st.pyplot(fig)
        
    # Download button

    st.subheader('Download button')

    csv_data = pd.DataFrame(st.session_state.transactions).to_csv(index=False)

    st.download_button(
        label = 'Download Transactions CSV',
        data = csv_data,
        file_name = 'transactions.csv',
        mime = 'text/csv'
    )
    




    

















    
