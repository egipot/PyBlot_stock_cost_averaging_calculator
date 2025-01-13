import csv
import os
from pprint import pprint
import pandas as pd
import numpy as np
import functions_calc as fc


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


# def get_event(filepath_r = 'entries.csv'):
#     """
#     Gets the existing transaction from the entries.csv file
#     If the file is not found, creates the file and returns an empty list
#     """
#     try:
#         with open(filepath_r, 'r') as readfile_local:
#             reader = csv.DictReader(readfile_local)
#             return list(reader) # Return as a list of dictionaries
#     except FileNotFoundError:
#         # If file not found, create it with headers
#         with open(filepath_r, 'w', newline='') as writefile_local:
#             writer = csv.writer(writefile_local)
#             writer.writerow(['Transaction', 'Stock_Name', 'Date', 'Num_of_Stocks', 'Price', 'Cost_of_Transaction', 'Transaction_ID'])  # Add header
#             return [] # Return an empty list if file was not found initially


# def write_event(all_events, filepath_w='entries.csv'):
#     """
#     Write the new/updated transactions
#     into the existing CSV file.
#     """
#     # Get the fieldnames from the first transaction if available
#     fieldnames = all_events[0].keys() if all_events else ['Transaction', 'Stock_Name', 'Date', 'Num_of_Stocks', 'Price', 'Cost_of_Transaction', 'Transaction_ID']

#     with open(filepath_w, 'w', newline='') as writefile_local:
#         writer = csv.DictWriter(writefile_local, fieldnames=fieldnames)
#         writer.writeheader()  # Write header row
#         writer.writerows(all_events)  # Write all the transaction data



user_prompt = input("Type 'add', 'view', 'edit', 'calculate', or 'remove': ")
user_prompt  = user_prompt.strip()
user_prompt  = user_prompt.lower()

if user_prompt == 'add':
   event = fc.add_transaction()
   print(event)
   all_events = fc.get_event() # Get the existing transactions
   all_events.append(event) # Append the new event
   fc.write_event(all_events) # Write all events to the CSV file

elif user_prompt == 'view':
   event = fc.get_event()
   pprint(event)

elif user_prompt == 'calculate':
    all_events = fc.get_event() # Get the existing transactions
    df = pd.DataFrame(all_events)
    df.set_index('Transaction_ID')
    # Convert 'Price' column to numeric, handling errors
    cost = pd.to_numeric(df['Num_of_Stocks'], errors='coerce') * pd.to_numeric(df['Price'], errors='coerce')
    cost_ave_result = round(cost.sum() / pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum(), 2)
    print(cost_ave_result)

elif user_prompt == 'remove':
    all_events = fc.get_event() # Get the existing transactions
    #pprint(all_events)
    entry_to_remove = int(input('Enter the transaction_ID to remove: '))
    entry_to_remove = entry_to_remove-1
    if entry_to_remove not in range (len(all_events)):
        print('Provided Transaction_ID does not exist. Exiting...')
    else:
        all_events.pop(entry_to_remove)
        pprint(all_events)
        fc.write_event(all_events) # Write all events to the CSV file

elif user_prompt == 'edit':
    all_events = fc.get_event() # Get the existing transactions
    entry_to_edit = int(input('Enter the transaction_ID to edit: '))
    entry_to_edit = entry_to_edit-1
    if entry_to_edit not in range (len(all_events)):
        print('Provided Transaction_ID does not exist. Exiting...')
    else:
        edited = fc.edit_transaction()
        all_events[entry_to_edit] = edited 
        pprint(all_events)
        fc.write_event(all_events) # Write all events to the CSV file

else:
   print('exiting...')