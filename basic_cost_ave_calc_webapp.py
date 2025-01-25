import pandas as pd
import functions_calc as fc
import streamlit as st

CURRENCY = '$'

def how_to_use():
    st.title("How to use: PyBlot's Basic Cost Averaging Calculator ")
    st.subheader("")
    st.markdown(':green[1. This calculator is intended to calculate positions for one stock only. ]')
    st.text('  - add: to fill up a purchase or investment')
    st.text('  - view: to display the currently entered transactions.')
    st.text('  - edit: to re-enter each detail of the Transaction_ID ')
    st.text('  - remove: to delete a transaction by entering its Transaction_ID')
    st.text('  - calculate has three successive operations:')
    st.write('      - get the summary of the current data (total shares bought, average price of purchases, total investment and fees.)')
    st.write('      - provide the present market price of the stock and know if you have gains or losses so far in your investment.')
    st.write('      - set your target earnings and monitor as the stock reaches the calculated price. It is good to have a sound plan and detach to emotions when it comes to investing :) ')
    st.text('\n')
    st.markdown(':blue[Alternatively, you may also check this tool: https://www.inchcalculator.com/stock-average-calculator/]')


def main_webapp():
    st.set_page_config(page_title='Cost_Average_Calculator', 
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
                #print(event)
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
                            value=f"{CURRENCY} {cost_ave_result:,}", 
                            border=True, 
                            help="Average price paid per stock, that is computed from all the purchases.")
                
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


                st.subheader('What can you calculate next? ')
                #st.write('  A: Calculate the gain/loss percentage based on the current price ')
                #st.write('  B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment. ')
                #st.write('  C: Determine the target selling price of all your current stocks based on your preferred gain percentage. ')

                # expanders
                st.markdown(''' :green[A: Calculate the gain/loss percentage based on the current price.]''')
                #st.markdown(''':red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in] :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
                current_stock_price = float(st.text_input(f'How much is the stock price now? (You may check in YahooFinance or MarketWatch)  {CURRENCY} '))
                current_invest_value = pd.to_numeric(df['Num_of_Stocks'], errors='coerce').sum() * current_stock_price
                st.write(f"Current investment's value: {CURRENCY} {round(current_invest_value,2):,}")
            
                set_tax = float(st.text_input('Enter the Tax (%) required in your country: '))
                gain_loss_if_selling_in_current_price = round((((current_stock_price * total_shares_bought)*(1+(set_tax/100))) - (gross_amount)) ,2)
                st.subheader(f'If you sell all {total_shares_bought:,} shares at this current price, then deducting the tax, your profit(or loss) is: {CURRENCY} {round(gain_loss_if_selling_in_current_price):,}')

                initial_gain_loss_percentage = ((current_invest_value*(1+(set_tax/100)))-gross_amount)*100/gross_amount

                if (current_invest_value *(1+(set_tax/100))) > gross_amount: 
                    #st.write(f'({round(current_invest_value*(1+(set_tax/100)),2)}-{gross_amount})*100/{gross_amount}')
                    st.subheader(f'That is {round(initial_gain_loss_percentage,2):,}% initial gain!')
                    st.write(f'The whole amount that you will receive after selling is: {CURRENCY}{round(current_invest_value*(1+(set_tax/100))):,}! ') 
                    st.write(f'Congratulations! Keep on investing and learning!')
                elif current_invest_value == gross_amount:
                    st.subheader('Breakeven. You just paid your taxes without income. Congratulations on being a good citizen :D')
                else: 
                    st.write(f'{CURRENCY} {gain_loss_if_selling_in_current_price:,}')
                    st.write(f'{((gain_loss_if_selling_in_current_price - gross_amount)/gross_amount):,} %')
                    st.write(f"{round(initial_gain_loss_percentage,2):,}% Loss.. Don't worry, this is just a paperloss if you average down. Just make sure that the company is still worth investing in...")
    
                # expander_common 
                st.markdown(''' :green[B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment.]''')
                
                #expander_common = st.expander('B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment. ', expanded=True)
                buy_new_gross_amount = float(st.text_input(f'How much are you willing to add in your investment? {CURRENCY} '))
                buy_new_price_ave_down = float(st.text_input(f'How much is your bidding price? {CURRENCY} '))
                    
                new_shares_ave_down = (buy_new_gross_amount*(1-(fees_percentage/100)))/buy_new_price_ave_down
                new_total_shares_bought = total_shares_bought + new_shares_ave_down
                new_gross_amount = gross_amount + buy_new_gross_amount
                new_net_amount = net_amount.sum() + (buy_new_gross_amount*(1-(fees_percentage/100)))
                new_ave_share_price = new_net_amount/new_total_shares_bought
                
                colB11, colB12 = st.columns(2, border=True)
                colB11.metric(label="Additional shares bought", 
                            value=f"{round(new_shares_ave_down,4):,} unit(s)", 
                            help="More units added")
                colB12.metric(label="Additional net amount invested", 
                            value=f"{CURRENCY} {round(buy_new_gross_amount*(1-(fees_percentage/100)),2):,}", 
                            help="From the provided additional investment, fees due to broker commission/spread have been deducted.")
            
                colB21, colB22 = st.columns(2, border=True)
                colB21.metric(label="New total shares bought", 
                            value=f"{round(new_total_shares_bought,4):,}", 
                            help="Sum of previous total and the newly purchased shares.")
                colB22.metric(label="New average price", 
                            value=f"{CURRENCY} {round(new_ave_share_price,2):,}", 
                            help="Average price paid per stock, that is computed from all the purchases.")

                colB31, colB32 = st.columns(2, border=True)
                colB31.metric(label="New total gross amount invested", 
                            value=f"{CURRENCY} {round(new_gross_amount,4):,}", 
                            help="Sum of all purchases with cummulative fees (broker commission / spread).")
                colB32.metric(label="New total net amount invested", 
                            value=f"{CURRENCY} {round(new_net_amount,2):,}", 
                            help="Sum of previous total and the new amount that is solely invested in the shares.")
                
                #current_stock_price = st.text_input(f'To calculate the gains/loss ({CURRENCY} and percentage) before tax reduction, enter how much is the current market price? ')
                gains_loss_currency = (new_total_shares_bought*current_stock_price) - new_gross_amount
                gains_loss_percent = (((new_total_shares_bought*current_stock_price) - new_gross_amount)/new_gross_amount) * 100
                #print(current_invest_value)
                #print(gains_loss_percent)
                #ave_down = st.columns(1, border=True)
                value_metric = round(gains_loss_percent,2)
                delta_metric = round((gains_loss_percent - initial_gain_loss_percentage),2)
                st.metric(f'new gains/loss after the additional investment = {CURRENCY} {round(gains_loss_currency,2):,} ({round(gains_loss_percent,2):,} %)', 
                        value = value_metric, 
                        delta = delta_metric, 
                        delta_color = 'normal', 
                        border = True,
                        help = 'A positive(arrow up) indicates if you have successfully averaged down (new gains is better than the initial gain percentage). A negative(arrow down) indicates that you averaged up.' )

                st.markdown(''':green[C: Determine the target selling price of all your current stocks based on your preferred gain percentage.]''')
                set_target_gain = float(st.text_input('What is your preferred gains (?)? '))
                target_selling_price_initial = round(total_shares_bought/((1-(fees_percentage/100))*(1-(set_tax/100))*(1+(set_target_gain/100))),2)
                target_selling_price_new = round(new_total_shares_bought/((1-(fees_percentage/100))*(1-(set_tax/100))*(1+(set_target_gain/100))),2)
                st.subheader(f'To gain {set_target_gain}% with the initial shares of {round(total_shares_bought,2)}, you should set the target selling price to: {CURRENCY} {target_selling_price_initial}')
                st.subheader(f'To gain {set_target_gain}% with the new total shares of {round(new_total_shares_bought,4)}, you should set the target selling price to: {CURRENCY} {target_selling_price_new}')
                
                break

            elif user_prompt == 'remove':
                all_events = fc.get_event() # Get the existing transactions
                #pprint(all_events)
                entry_to_remove = int(st.text_input('Enter the transaction_ID to remove: '))
                entry_to_remove = entry_to_remove-1
                if entry_to_remove not in range (len(all_events)):
                    st.warning('Provided Transaction_ID does not exist.')
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
                    st.warning('Provided Transaction_ID does not exist.')
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


pg = st.navigation([st.Page(main_webapp), st.Page(how_to_use)], position='sidebar', expanded=True)
pg.run()

#print('Hello')
#st.session_state