#This file contains all the functions used in the basic_cost_ave_calc.py
import csv
import streamlit as st

################################################################
# FUNCTIONS outside the streamlit app
def add_transaction():
    transaction_dict = {}
    #transaction_dict['Transaction'] = input("Transaction ['buy', 'sell']: ")  
    #if transaction_dict['Transaction'].lower() not in ('buy', 'sell'):
    #    return "Invalid Input"
    #transaction_dict['Stock_Name'] = input("Stock_Name (abbreviation): ")  
    transaction_dict['Date'] = input("Date YYYY-MM-DD: ")  
    transaction_dict['Num_of_Shares'] = input("Number of Shares: ")  
    transaction_dict['Price'] = input("Price per Share: ")
    transaction_dict['Cost_of_Transaction'] = input("Cost of Transaction: ")
    #transaction_dict['Transaction_ID'] = int(input("Transaction ID: "))
    return transaction_dict

def edit_transaction():
    edit_transaction_dict = {}
    # edit_transaction_dict['Transaction'] = input("Transaction ['buy', 'sell']: ")  
    # if edit_transaction_dict['Transaction'].lower() not in ('buy', 'sell'):
    #     return "Invalid Input"
    #edit_transaction_dict['Stock_Name'] = input("Stock_Name (abbreviation): ")  
    edit_transaction_dict['Date'] = input("Date YYYY-MM-DD: ")  
    edit_transaction_dict['Num_of_Shares'] = input("Number of Share: ")  
    edit_transaction_dict['Price'] = input("Price per Share: ")
    edit_transaction_dict['Cost_of_Transaction'] = input("Cost of Transaction: ")
    #edit_transaction_dict['Transaction_ID'] = int(input("Transaction ID: "))
    return edit_transaction_dict
################################################################

def transaction_form():
    transaction_dict = {}
    with st.form("my_form"):
        #st.slider("Inside the form")
        #transaction_dict['Transaction'] = st.pills('action', ['buy', 'sell'], selection_mode='single')
        #transaction_dict['Stock_Name'] = st.text_input("Stock_Name (abbreviation): ", placeholder='Enter the Stock Abbreviated Name (do not press enter yet)') 
        transaction_dict['Date'] = st.date_input("Date of Purchase [YYYY-MM-DD]: ", format="YYYY.MM.DD")  
        transaction_dict['Num_of_Shares'] = st.number_input("Number of Shares: ")  
        transaction_dict['Price_per_share'] = st.number_input("Price per Share: ", format="%0.2f")
        transaction_dict['Cost_of_Transaction'] = st.number_input("Cost of Transaction: ", format="%0.2f")
        #transaction_dict['Transaction_ID'] = st.number_input("Transaction ID: ", placeholder='Enter the data. Do not press enter yet, please use the Submit button')
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


def get_sample(filepath_r = 'sample.csv'):
    """
    Gets the existing transaction from the entries.csv file
    If the file is not found, creates the file and returns an empty list
    """
    with open(filepath_r, 'r') as readfile_local:
        reader = csv.DictReader(readfile_local)
        return list(reader) # Return as a list of dictionaries


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
            writer.writerow(['Date', 'Num_of_Shares', 'Price_per_share', 'Cost_of_Transaction'])  # Add header
            return [] # Return an empty list if file was not found initially


def write_event(all_events, filepath_w='entries.csv'):
    """
    Write the new/updated transactions
    into the existing CSV file.
    """
    # Get the fieldnames from the first transaction if available
    fieldnames = all_events[0].keys() if all_events else ['Date', 'Num_of_Shares', 'Price_per_share', 'Cost_of_Transaction']

    with open(filepath_w, 'w', newline='') as writefile_local:
        writer = csv.DictWriter(writefile_local, fieldnames=fieldnames)
        writer.writeheader()  # Write header row
        writer.writerows(all_events)  # Write all the transaction data


if __name__ == '__main__':
    print('Hello')
    