import pandas as pd
from pprint import pprint
import functions_calc as fc
import streamlit as st

CURRENCY = '$'

st.set_page_config(page_title='Cost_Ave_Calc', 
                   layout='centered', initial_sidebar_state='auto')
st.title('Basic Cost Averaging Calculator')
st.text('This calculator aims to help determine the average share price that you paid for a stock and determine the target share price in your next purchase based on your preferred percentage gain(%).')

def on_change_user_prompt():
    st.session_state['selectbox']

options = ['add', 'view', 'edit', 'calculate', 'remove', 'exit']

#user_prompt = input("Type 'add', 'view', 'edit', 'calculate', 'remove' or 'exit': ")
user_prompt = st.selectbox('How would like to proceed? ', options, index=None, 
                           key='selectbox',on_change=on_change_user_prompt,
                           placeholder='Select an action here...')
while user_prompt:
    try: 
        st.write('You selected: ', user_prompt )

        if user_prompt == 'add':
            #event = fc.add_transaction()
            #print(event)
            event = fc.transaction_form()
            print(event)
            all_events = fc.get_event() # Get the existing transactions
            all_events.append(event) # Append the new event
            fc.write_event(all_events) # Write all events to the CSV file
            st.write('The updated transactions: ')
            st.table(all_events)
            break

        elif user_prompt == 'view':
            event = fc.get_event()
            #pprint(event)
            st.table(event)
            break

        elif user_prompt == 'calculate':
            all_events = fc.get_event() # Get the existing transactions
            df = pd.DataFrame(all_events)
            df.set_index('Transaction_ID')
            st.table(all_events)
            
            ### CALCULATOR FORMULA ###
            # Total owned stocks
            total_shares_bought = pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum()

            # Convert 'Price' column to numeric, handling errors
            net_amount = pd.to_numeric(df['Num_of_Stocks'], errors='coerce') * pd.to_numeric(df['Price'], errors='coerce')
            cost_ave_result = round(net_amount.sum() / pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum(), 2)

            # Gross purchase price ((#shares * purchase price) + commissions)
            gross_amount = round(pd.to_numeric(df['Cost_of_Transaction'], errors='coerce').sum(), 2)

            # Total commission / spread / fees:
            fees = gross_amount - net_amount.sum()
            fees_percentage = round((fees / gross_amount)*100, 4)
            
            #SUMMARY:
            # st.write(f'SUMMARY:')
            # st.write(f'You have invested: {total_shares_bought} shares at {cost_ave_result} = $ {net_amount.sum()}')
            # st.write(f'Breakdown:')
            # st.write(f'\tTotal shares bought: {total_shares_bought} units')
            # st.write(f'\tAverage share price: {CURRENCY} {cost_ave_result}')
            # st.write(f'\tGross amount (including commission, spread, ...) : {CURRENCY} {gross_amount}')
            # st.write(f'\tNet amount of your investment: {CURRENCY} {net_amount.sum()}')
            # st.write(f'\tTotal commission/spread/fees: {CURRENCY} {fees} ({fees_percentage}%) ')
            
            st.subheader('Summary of Investment: ')

            col11, col12, = st.columns(2)
            col11.metric(label="Total shares bought", 
                         value=f"{total_shares_bought:,} unit(s)", 
                         border=True, 
                         help="The number of stocks bought, \
                         calculated after deduction of fees from the gross amount.")
            col12.metric(label="Average share price", 
                         value=f"{cost_ave_result:,}", 
                         border=True, 
                         help="Average price paid per stock in multiple purchases.")
            
            col21, col22, = st.columns(2)
            col21.metric(label="Gross amount invested", 
                         value=f"{CURRENCY} {gross_amount:,}", 
                         border=True, 
                         help="Total purchase price including broker commission, spread, and other fees.")
            col22.metric(label="Net amount invested", 
                         value=f"{CURRENCY} {net_amount.sum():,}", 
                         border=True, 
                         help="Total amount paid solely for the stocks.")

            col31, col32, = st.columns(2)
            col31.metric(label="Total commission/spread/fees", 
                         value=f"{CURRENCY} {fees:,}", 
                         border=True, 
                         help="Total fees due to broker commission, spread, ...")
            col32.metric(label="Total commission/spread/fees in percentage", 
                         value=f"{fees_percentage} %", 
                         border=True, 
                         help="Total amount paid solely for the stocks.")


            st.write('What do you want to do next? ')
            #st.write('  A: Calculate the gain/loss percentage based on the current price ')
            #st.write('  B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment. ')
            #st.write('  C: Determine the target selling price of all your current stocks based on your preferred gain percentage. ')

            expander_A = st.expander('A: Calculate the gain/loss percentage based on the current price')
            current_stock_price = float(expander_A.text_input(f'How much is the stock price now? (You may check in YahooFinance or MarketWatch)  {CURRENCY} '))
            current_invest_value = pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum() * current_stock_price
            expander_A.write(f"Current investment's value: {CURRENCY} {round(current_invest_value,2):,}")
        
#
            set_tax = float(expander_A.text_input('Enter the Tax (%) required in your country: '))
            gain_loss_if_selling_in_current_price = round((((current_stock_price * total_shares_bought)*(1+(set_tax/100))) - (gross_amount)) ,2)
            expander_A.write(f'If you sell all {total_shares_bought:,} shares at this current price, then deducting the tax, your profit(or loss) is: {CURRENCY} {round(gain_loss_if_selling_in_current_price):,}')
    
            if (current_invest_value *(1+(set_tax/100))) > gross_amount: 
                #expander_A.write(f'({round(current_invest_value*(1+(set_tax/100)),2)}-{gross_amount})*100/{gross_amount}')
                expander_A.write(f'That is {round(((current_invest_value*(1+(set_tax/100)))-gross_amount)*100/gross_amount,2):,}% gain!')
                expander_A.write(f'The whole amount that you will receive after selling is: {CURRENCY}{round(current_invest_value*(1+(set_tax/100))):,}! ') 
                expander_A.write(f'Congratulations! Keep on investing and learning!')
            elif current_invest_value == gross_amount:
                expander_A.write('Breakeven. You just paid your taxes without income. Congratulations on being a good citizen :D')
            else: 
                expander_A.write(f'{CURRENCY} {gain_loss_if_selling_in_current_price:,}')
                expander_A.write(f'{((gain_loss_if_selling_in_current_price - gross_amount)/gross_amount):,} %')
                expander_A.write("Loss.. Don't worry, this is just a paperloss if you average down. Just make sure that the company is still worth investing in...")
   

#

            break

        elif user_prompt == 'remove':
            all_events = fc.get_event() # Get the existing transactions
            #pprint(all_events)
            entry_to_remove = int(st.text_input('Enter the transaction_ID to remove: '))
            entry_to_remove = entry_to_remove-1
            if entry_to_remove not in range (len(all_events)):
                print('Provided Transaction_ID does not exist. Exiting...')
            else:
                all_events.pop(entry_to_remove)
                #pprint(all_events)
                st.info(f'Transaction_ID {entry_to_remove+1} has been removed.')
                st.write('The updated transactions: ')
                st.table(all_events)
                fc.write_event(all_events) # Write all events to the CSV file
            break

        elif user_prompt == 'edit':
            all_events = fc.get_event() # Get the existing transactions
            st.table(all_events)
            entry_to_edit = int(st.text_input('Enter the transaction_ID to edit: '))
            entry_to_edit = entry_to_edit-1
            if entry_to_edit not in range (len(all_events)):
                print('Provided Transaction_ID does not exist. Exiting...')
            else:
                edited = fc.transaction_form()
                all_events[entry_to_edit] = edited 
                #pprint(all_events)
                if True:
                    st.write(f'With the updated Transaction_ID {entry_to_edit + 1}: ')
                    st.table(all_events)
                    fc.write_event(all_events) # Write all events to the CSV file
            break

        elif user_prompt == 'exit':
            print('exiting...')
            break

        else:
            break

    except:
        #print('exiting...')
        break


#print('Hello')
#st.session_state