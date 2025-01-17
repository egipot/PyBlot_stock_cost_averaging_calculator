#This file contains all the functions used in the basic_cost_ave_calc.py
import csv
import os
import streamlit as st

################################################################
# FUNCTIONS outside the streamlit app
# def add_transaction():
#     transaction_dict = {}
#     transaction_dict['Transaction'] = input("Transaction ['buy', 'sell']: ")  
#     if transaction_dict['Transaction'].lower() not in ('buy', 'sell'):
#         return "Invalid Input"
#     transaction_dict['Stock_Name'] = input("Stock_Name (abbreviation): ")  
#     transaction_dict['Date'] = input("Date YYYY-MM-DD: ")  
#     transaction_dict['Num_of_Stocks'] = input("Number of Stocks: ")  
#     transaction_dict['Price'] = input("Price per Stock: ")
#     transaction_dict['Cost_of_Transaction'] = input("Cost of Transaction: ")
#     transaction_dict['Transaction_ID'] = int(input("Transaction ID: "))
#     return transaction_dict

# def edit_transaction():
#     edit_transaction_dict = {}
#     edit_transaction_dict['Transaction'] = input("Transaction ['buy', 'sell']: ")  
#     if edit_transaction_dict['Transaction'].lower() not in ('buy', 'sell'):
#         return "Invalid Input"
#     edit_transaction_dict['Stock_Name'] = input("Stock_Name (abbreviation): ")  
#     edit_transaction_dict['Date'] = input("Date YYYY-MM-DD: ")  
#     edit_transaction_dict['Num_of_Stocks'] = input("Number of Stocks: ")  
#     edit_transaction_dict['Price'] = input("Price per Stock: ")
#     edit_transaction_dict['Cost_of_Transaction'] = input("Cost of Transaction: ")
#     edit_transaction_dict['Transaction_ID'] = int(input("Transaction ID: "))
#     return edit_transaction_dict
################################################################

def transaction_form():
    transaction_dict = {}
    with st.form("my_form"):
        #st.slider("Inside the form")
        transaction_dict['Transaction'] = st.pills('action', ['buy', 'sell'], selection_mode='single')
        transaction_dict['Stock_Name'] = st.text_input("Stock_Name (abbreviation): ", placeholder='Enter the Stock Abbreviated Name (do not press enter yet)') 
        transaction_dict['Date'] = st.text_input("Date YYYY-MM-DD: ", placeholder='Enter the data. Do not press enter yet, please use the Submit button')  
        transaction_dict['Num_of_Stocks'] = st.text_input("Number of Stocks: ", placeholder='Enter the data. Do not press enter yet, please use the Submit button')  
        transaction_dict['Price'] = st.text_input("Price per Stock: ", placeholder='Enter the data. Do not press enter yet, please use the Submit button')
        transaction_dict['Cost_of_Transaction'] = st.text_input("Cost of Transaction: ", placeholder='Enter the data. Do not press enter yet, please use the Submit button')
        transaction_dict['Transaction_ID'] = st.text_input("Transaction ID: ", placeholder='Enter the data. Do not press enter yet, please use the Submit button')
        submitted = st.form_submit_button("Submit")
        if submitted:
            print(transaction_dict)
            print(list(transaction_dict.values()))
            exists = False
            values_to_check = ['', ' ', None]
            for check in values_to_check: 
                if check in transaction_dict.values():
                    exists = True
            print(exists)
            if exists == True:
                print('Incomplete input')
            else: 
                print('OK')
                return transaction_dict


def get_event(filepath_r = 'entries.csv'):
    """
    Gets the existing transaction from the entries.csv file
    If the file is not found, creates the file and returns an empty list
    """
    try:
        with open(filepath_r, 'r') as readfile_local:
            reader = csv.DictReader(readfile_local)
            return list(reader) # Return as a list of dictionaries
    except FileNotFoundError:
        # If file not found, create it with headers
        with open(filepath_r, 'w', newline='') as writefile_local:
            writer = csv.writer(writefile_local)
            writer.writerow(['Transaction', 'Stock_Name', 'Date', 'Num_of_Stocks', 'Price', 'Cost_of_Transaction', 'Transaction_ID'])  # Add header
            return [] # Return an empty list if file was not found initially


def write_event(all_events, filepath_w='entries.csv'):
    """
    Write the new/updated transactions
    into the existing CSV file.
    """
    # Get the fieldnames from the first transaction if available
    fieldnames = all_events[0].keys() if all_events else ['Transaction', 'Stock_Name', 'Date', 'Num_of_Stocks', 'Price', 'Cost_of_Transaction', 'Transaction_ID']

    with open(filepath_w, 'w', newline='') as writefile_local:
        writer = csv.DictWriter(writefile_local, fieldnames=fieldnames)
        writer.writeheader()  # Write header row
        writer.writerows(all_events)  # Write all the transaction data

