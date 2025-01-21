import pandas as pd
#import numpy as np
from pprint import pprint
import functions_calc as fc

CURRENCY = '$'

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

    ### CALCULATOR FORMULA ###
    # Total owned stocks
    total_shares_bought = pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum()

    # Convert 'Price' column to numeric, handling errors
    net_amount = pd.to_numeric(df['Num_of_Stocks'], errors='coerce') * pd.to_numeric(df['Price'], errors='coerce')
    cost_ave_result = round(net_amount.sum() / pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum(), 2)

    # Gross purchase price ((#shares * purchase price) + commissions)
    gross_amount = round(pd.to_numeric(df['Cost_of_Transaction'], errors='coerce').sum(), 2)

    # Net sell price = (# shares × sell price) – commission 
    # ^This is equivalent to the variable 'cost' above

    # Total commission / spread / fees:
    fees = gross_amount - net_amount.sum()
    fees_percentage = round((fees / gross_amount)*100, 2)
    
    #SUMMARY:
    print(f'SUMMARY:')
    print(f'You have invested: {total_shares_bought} shares at {cost_ave_result} = $ {net_amount.sum()}')
    print(f'Breakdown:')
    print(f'\tTotal shares bought: {total_shares_bought} units')
    print(f'\tAverage share price: {CURRENCY} {cost_ave_result}')
    print(f'\tGross amount (including commission, spread, ...) : {CURRENCY} {gross_amount}')
    print(f'\tNet amount of your investment: {CURRENCY} {net_amount.sum()}')
    print(f'\tTotal commission/spread/fees: {CURRENCY} {fees} ({fees_percentage}%) ')

    print('What do you want to do next? ')
    print('  A: Calculate the gain/loss percentage based on the current price ')
    print('  B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment. ')
    print('  C: Determine the target selling price of all your current stocks based on your preferred gain percentage. ')
    #print('  D: Perform B and C in sequence - to average down once and determine the target selling price based on target gain. ')
    #print('  E: Show me a demo (sample calculation). ')

    more_functions = input('Choose from the provided options: ')
    
    if more_functions.upper() == 'A':
        current_stock_price = float(input(f'How much is the stock price now? (You may check in YahooFinance or MarketWatch)  {CURRENCY} '))
        current_invest_value = pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum() * current_stock_price
        print(f"Current investment's value: {CURRENCY} {round(current_invest_value,2)}")
        
        set_tax = float(input('Enter the Tax (%) required in your country: '))
        gain_loss_if_selling_in_current_price = round((((current_stock_price * total_shares_bought)*(1+(set_tax/100))) - (gross_amount)) ,2)
        print(f'If you sell all {total_shares_bought} shares at this current price, then deducting the tax, you will get: {CURRENCY} {gain_loss_if_selling_in_current_price}')
    
        if (current_invest_value *(1+(set_tax/100))) > gross_amount: 
            print(f'({round(current_invest_value*(1+(set_tax/100)),2)}-{gross_amount})*100/{gross_amount}')
            print(f'{round(((current_invest_value*(1+(set_tax/100)))-gross_amount)*100/gross_amount,2)}% gain! That is {CURRENCY}{round(current_invest_value*(1+(set_tax/100)))}! Congratulations! Keep on investing and learning! ')
        elif current_invest_value == gross_amount:
            print('Breakeven. You just paid your taxes without income. Congratulations on being a good citizen :D')
        else: 
            print(f'{CURRENCY} {gain_loss_if_selling_in_current_price}')
            print(f'{(gain_loss_if_selling_in_current_price - gross_amount)/gross_amount} %')
            print("Loss.. Don't worry, this is just a paperloss if you average down. Just make sure that the company is still worth investing in...")
   

    elif more_functions.upper() == 'B':
        buy_new_gross_amount = float(input(f'How much are you willing to add in your investment? {CURRENCY} '))
        buy_new_price_ave_down = float(input(f'How much is your bidding price? {CURRENCY} '))
            
        print(f'add_net_amount: {(buy_new_gross_amount*(1-(fees_percentage/100)))} ({fees_percentage/100})')

        new_shares_ave_down = (buy_new_gross_amount*(1-(fees_percentage/100)))/buy_new_price_ave_down
        new_total_shares_bought = total_shares_bought + new_shares_ave_down
        new_gross_amount = gross_amount + buy_new_gross_amount
        new_net_amount = net_amount.sum() + (buy_new_gross_amount*(1-(fees_percentage/100)))
        new_ave_share_price = new_net_amount/new_total_shares_bought
        print(f'new_shares_ave_down = {new_shares_ave_down}')
        print(f'new total shares bought = {new_total_shares_bought}')
        print(f'new gross_amount = {new_gross_amount}')
        print(f'new net_amount = {new_net_amount}')
        print(f'new_ave_share_price = {new_ave_share_price}')
        
        current_stock_price = float(input(f'To calculate the gains/loss ({CURRENCY} and %) before tax reduction, enter how much is the current market price? {CURRENCY} '))
        gains_loss_currency = (new_total_shares_bought*current_stock_price) - new_gross_amount
        gains_loss_percent = (((new_total_shares_bought*current_stock_price) - new_gross_amount)/new_gross_amount) * 100
        print(f'gains/loss = {CURRENCY} {round(gains_loss_currency,2)}')
        print(f'gains/loss = {round(gains_loss_percent,2)} % ')

    
    elif more_functions.upper() == 'C':
            set_target_gain = float(input('What is your preferred gains(%? [Y, otherwise, exiting...]  '))
            set_tax = float(input('Enter the Tax (%) required in your country: '))
            target_selling_price = round(total_shares_bought/((1-(fees_percentage/100))*(1-(set_tax/100))*(1+(set_target_gain/100))),2)
            print(f'To gain {set_target_gain}%, the target selling price is: {target_selling_price}')
    else:  
            print('exiting...')
            


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