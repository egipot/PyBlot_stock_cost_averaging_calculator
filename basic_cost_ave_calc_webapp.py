import pandas as pd
import numpy as np
from pprint import pprint
import functions_calc as fc
import streamlit as st

st.title('Basic Cost Averaging Calculator')
st.text('This calculator aims to help determine the average share price that you paid for a stock and determine the target share price in your next purchase based on your preferred percentage gain(%).')
#user_prompt = input("Type 'add', 'view', 'edit', 'calculate', 'remove' or 'exit': ")
user_prompt = st.selectbox('How would like to proceed? ', 
                           ('add', 'view', 'edit', 'calculate', 'remove', 'exit'), 
                           index=None, on_change= ,placeholder='Select an action here...')
while user_prompt:
    try: 
        user_prompt  = user_prompt.strip()
        user_prompt  = user_prompt.lower()
        st.write('You selected: ', user_prompt )


        if user_prompt == 'add':
            event = fc.add_transaction()
            print(event)
            all_events = fc.get_event() # Get the existing transactions
            all_events.append(event) # Append the new event
            fc.write_event(all_events) # Write all events to the CSV file

        elif user_prompt == 'view':
            event = fc.get_event()
            #pprint(event)
            st.table(event)
            break

        elif user_prompt == 'calculate':
            all_events = fc.get_event() # Get the existing transactions
            df = pd.DataFrame(all_events)
            df.set_index('Transaction_ID')
            # Convert 'Price' column to numeric, handling errors
            cost = pd.to_numeric(df['Num_of_Stocks'], errors='coerce') * pd.to_numeric(df['Price'], errors='coerce')
            cost_ave_result = round(cost.sum() / pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum(), 2)
            #print(cost_ave_result)
            st.write(f'The average share cost: {cost_ave_result}')
            break

        elif user_prompt == 'remove':
            all_events = fc.get_event() # Get the existing transactions
            #pprint(all_events)
            entry_to_remove = int(input('Enter the transaction_ID to remove: '))
            entry_to_remove = entry_to_remove-1
            if entry_to_remove not in range (len(all_events)):
                print('Provided Transaction_ID does not exist. Exiting...')
            else:
                all_events.pop(entry_to_remove)
                #pprint(all_events)
                st.table(all_events)
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
                #pprint(all_events)
                st.table(all_events)
                fc.write_event(all_events) # Write all events to the CSV file

        elif user_prompt == 'exit':
            print('exiting...')
            break

        else:
            break

    except:
        print('exiting...')
        break