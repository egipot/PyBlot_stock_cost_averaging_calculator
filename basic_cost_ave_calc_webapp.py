import pandas as pd
import functions_calc as fc
import streamlit as st


CURRENCY = '$'


st.set_page_config(page_title='Cost_Average_Calculator', 
            layout='centered', initial_sidebar_state='auto')
st.title("PyBlot's Basic Cost Averaging Calculator")
st.text('This calculator aims to help determine the average share price that you paid for a stock and determine the target share price in your next purchase based on your preferred percentage gain(%).')

def on_change_user_prompt():
    st.session_state['selectbox']

options = ['add', 'view', 'edit', 'calculate', 'remove']

user_prompt = st.selectbox('How would like to proceed? ', options, index=None, 
                    key='selectbox',on_change=on_change_user_prompt, 
                    placeholder='Select an action here...')
while user_prompt:
    st.write('You selected: ', user_prompt )


    if user_prompt == 'add':
        try:
            event = fc.transaction_form()
            all_events = fc.get_event() # Get the existing transactions
            all_events.append(event) # Append the new event
            fc.write_event(all_events) # Write all events to the CSV file
            st.write('The updated transactions: ')
            st.table(all_events)
            break
        except:
            break

    elif user_prompt == 'view':
        event = fc.get_event()
        st.table(event)
        break


    elif user_prompt == 'calculate':
        all_events = fc.get_event() # Get the existing transactions
        df = pd.DataFrame(all_events)
        st.table(all_events)
        
        ### CALCULATOR FORMULA - A ###
        # Total owned stocks
        total_shares_bought = pd.to_numeric(df['Num_of_Shares'], errors='coerce').sum()

        # Convert 'Price_per_share' column to numeric, handling errors
        net_amount = pd.to_numeric(df['Num_of_Shares'], errors='coerce') * pd.to_numeric(df['Price_per_share'], errors='coerce')
        cost_ave_result = round(net_amount.sum() / total_shares_bought, 2)

        # Gross purchase price ((#shares * purchase price) + commissions)
        gross_amount = round(pd.to_numeric(df['Cost_of_Transaction'], errors='coerce').sum(), 2)

        # Total commission / spread / fees:
        fees = gross_amount - net_amount.sum()
        fees_percentage = round((fees / gross_amount)*100, 4)
        
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

        
        expander1 = st.expander("See the formula:")
        expander1.markdown(''':orange[Total shares bought = sum(Num_of_Shares)]''')
        expander1.markdown(''':orange[Average share price = (sum(Num_of_Shares * Price_per_share)) / sum(Num_of_Shares)]''')
        expander1.markdown(''':orange[Gross amount invested = sum(Cost_of_Transaction)]''')
        expander1.markdown(''':orange[Net amount invested = sum(Num_of_Shares * Price_per_share)]''')
        expander1.markdown(''':orange[Total fees in currency = sum(Cost_of_Transaction - (Num_of_Shares * Price_per_share))]''')
        expander1.markdown(''':orange[Total fees in percentage = sum(Cost_of_Transaction - (Num_of_Shares * Price_per_share)) / sum(Cost_of_Transaction)]''')


        st.markdown(''':blue[What can you calculate next?]''')
        st.markdown(''':blue[   A: Calculate the gain/loss percentage based on the current price] ''')
        st.markdown(''':blue[   B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment. ]''')
        st.markdown(''':blue[   C: Determine the target selling price of all your current stocks based on your preferred gain percentage.] ''')

        st.subheader('A: Calculate the gain/loss percentage based on the current price.')
        #st.markdown(''':red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in] :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
        current_stock_price = st.number_input(f'How much is the share price now? (You may check in YahooFinance or MarketWatch)  {CURRENCY}', step = 0.0001)
        current_invest_value = total_shares_bought * current_stock_price
        st.subheader(f"Gross investment's value: {CURRENCY} {round(current_invest_value,4):,}" )
    
        set_tax = st.number_input('Enter the Tax (%) required in your country: ')
        
        current_invest_value_minus_fees_and_tax = (total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))
        
        gain_loss_if_selling_in_current_price =  ((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - (gross_amount)
        
        initial_gain_loss_value = ((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount
        initial_gain_loss_percentage = (((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount)*100 / gross_amount


        if  initial_gain_loss_value > 0.01:  
            st.markdown(f''':green[The total amount that you will receive after selling is: ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***!] ''') 
            st.markdown(f''':green[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% tax, your profit is: ***{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}***]''')
            st.markdown(f''':green[That is ***{round(initial_gain_loss_percentage,4):,}%*** initial gain!]''')
            st.markdown(f''':green[Congratulations! Keep on investing and learning!]''')

            expander3 = st.expander("See the breakdown: ") 
            expander3.markdown(f"""***Gross investment value*** = total_shares_bought * current_stock_price = {total_shares_bought} * {current_stock_price} = ***{CURRENCY} {total_shares_bought * current_stock_price}***""")
            expander3.markdown('''Derive the ***total amount that you will receive after selling:***''')
            expander3.markdown(f''' = total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))''')
            expander3.markdown(f''' = {total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100)) ''')
            expander3.markdown(f''' = {total_shares_bought} * {current_stock_price} * {(1-(fees_percentage/100))} * {(1-(set_tax/100))} = ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***''')
            expander3.markdown(f'''***Profit / Loss in currency*** = (total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))) - gross_amount''')
            expander3.markdown(f''' = ({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))) - {gross_amount} = ***{CURRENCY} {round(initial_gain_loss_value,2):,}*** ''')
            expander3.markdown(f'''***Profit / Loss in percentage*** = ((total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100)))-gross_amount) *100 / gross_amount ''')
            expander3.markdown(f''' = (({total_shares_bought} * {current_stock_price}*(1-({fees_percentage}/100))*(1-({set_tax}/100)))-{gross_amount})*100/{gross_amount} = ***{round(initial_gain_loss_percentage,4):,} %*** ''')

            
        elif  0.0 <= initial_gain_loss_value <= 0.01: 
            #st.markdown(f''':blue[The total amount that you will receive after selling is: {CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}!] ''')
            st.markdown(f''':blue[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% tax, you are expected to receive: {CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}]''')
            st.markdown(f''':blue[Breakeven. You just paid your broker and taxes without income. Congratulations on being a good citizen!]''')

            expander4 = st.expander("See the breakdown: ") 
            expander4.markdown(f"""***Gross investment value*** = total_shares_bought * current_stock_price = {total_shares_bought} * {current_stock_price} = ***{CURRENCY} {total_shares_bought * current_stock_price}***""")
            expander4.markdown('''Derive the ***total amount that you will receive after selling:***''')
            expander4.markdown(f''' = total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))''')
            expander4.markdown(f''' = {total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100)) ''')
            expander4.markdown(f''' = {total_shares_bought} * {current_stock_price} * {(1-(fees_percentage/100))} * {(1-(set_tax/100))} = ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***''')
            expander4.markdown(f'''***Profit / Loss in currency*** = (total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))) - gross_amount''')
            expander4.markdown(f''' = ({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))) - {gross_amount} = ***{CURRENCY} {round(initial_gain_loss_value,2):,}*** ''')
            expander4.markdown(f'''***Profit / Loss in percentage*** = ((total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100)))-gross_amount) *100 / gross_amount ''')
            expander4.markdown(f''' = (({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100))*(1-({set_tax}/100)))-{gross_amount})*100/{gross_amount} = ***{round(initial_gain_loss_percentage,4):,} %*** ''')

        
        else: 
            #st.markdown(f''':red[{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}]''')
            st.markdown(f''':red[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% tax, your balance will be deducted by: ***{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}***]''')
            st.markdown(f''':red[Your investment is at ***{round(initial_gain_loss_percentage,4):,}%*** loss. Do not worry, this is just a paperloss if you average down. Just make sure that the company is still worth investing in...]''')
            
            expander5 = st.expander("See the breakdown: ") 
            expander5.markdown(f"""***Gross investment value*** = total_shares_bought * current_stock_price = {total_shares_bought} * {current_stock_price} = ***{CURRENCY} {total_shares_bought * current_stock_price}***""")
            expander5.markdown('''Derive the ***total amount that you will receive after selling:***''')
            expander5.markdown(f''' = total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))''')
            expander5.markdown(f''' = {total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100)) ''')
            expander5.markdown(f''' = {total_shares_bought} * {current_stock_price} * {(1-(fees_percentage/100))} * {(1-(set_tax/100))} = ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***''')
            expander5.markdown(f'''***Profit / Loss in currency*** = (total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))) - gross_amount''')
            expander5.markdown(f''' = ({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))) - {gross_amount} = ***{CURRENCY} {round(initial_gain_loss_value,2):,}*** ''')
            expander5.markdown(f'''***Profit / Loss in percentage*** = ((total_shares_bought * current_stock_price * (1-(fees percentage/100)) * (1-(tax/100))) - gross_amount) * 100 / gross_amount ''')
            expander5.markdown(f''' = (({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100))*(1-({set_tax}/100)))-{gross_amount}) * 100 / {gross_amount} = ***{round(initial_gain_loss_percentage,4):,} %*** ''')


        st.subheader('B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment.')
        
        ### CALCULATOR FORMULA - B ###
        buy_new_gross_amount = float(st.number_input(f'How much are you willing to add in your investment? {CURRENCY} '))
        buy_new_price_ave_down = float(st.number_input(f'How much is your bidding price? {CURRENCY} '))
        #st.write({buy_new_gross_amount}, {type(buy_new_gross_amount)})
        #st.write({buy_new_price_ave_down}, {type(buy_new_price_ave_down)})
        #st.write({buy_new_gross_amount in [0, 0.0] or buy_new_price_ave_down in [0, 0.0]})     


        if buy_new_gross_amount in [0, 0.0] or buy_new_price_ave_down in [0, 0.0]:
            new_shares_ave_down = 0
            new_ave_share_price = 0
            new_total_shares_bought = total_shares_bought
            new_gross_amount = gross_amount
            new_net_amount = net_amount.sum()
            gains_loss_currency =(total_shares_bought*current_stock_price*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount
            gains_loss_percent = (((total_shares_bought*current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100)) - gross_amount)/gross_amount) * 100
            value_metric = cost_ave_result
            delta_metric = 0
        else:
            new_shares_ave_down = (buy_new_gross_amount*(1-(fees_percentage/100))*(1-(set_tax/100)))/buy_new_price_ave_down
            new_total_shares_bought = total_shares_bought + new_shares_ave_down
            new_gross_amount = gross_amount + buy_new_gross_amount
            new_net_amount = net_amount.sum() + (buy_new_gross_amount*(1-(fees_percentage/100))*(1-(set_tax/100)))
            new_ave_share_price = new_net_amount/new_total_shares_bought
            gains_loss_currency = (new_total_shares_bought*current_stock_price*(1-(fees_percentage/100))*(1-(set_tax/100))) - new_gross_amount
            gains_loss_percent = (((new_total_shares_bought*current_stock_price*(1-(fees_percentage/100))*(1-(set_tax/100))) - new_gross_amount)/new_gross_amount) * 100
            value_metric = new_ave_share_price
            delta_metric = new_ave_share_price - cost_ave_result 
        

        colB11, colB12 = st.columns(2, border=True)
        colB11.metric(label="Additional shares bought", 
                    value=f"{round(new_shares_ave_down,4):,} unit(s)", 
                    help="More units added")
        colB12.metric(label="Additional net amount invested", 
                    value=f"{CURRENCY} {round(buy_new_gross_amount*(1-(fees_percentage/100)),2):,}", 
                    help="From the provided additional investment, fees due to broker commission/spread have been deducted.")
    
        colB21, colB22 = st.columns(2, border=True)
        colB21.metric(label="New total shares bought", 
                    value=f"{round(new_total_shares_bought,4):,} unit(s)", 
                    help="Sum of previous total and the newly purchased shares.")
        colB22.metric(label="New average price", 
                    value=f"{CURRENCY} {round(new_ave_share_price,4):,}", 
                    delta = delta_metric, 
                    delta_color = 'inverse',
                    help="Average price paid per stock, that is computed from all the purchases. A green indicates that you have successfully averaged down (new gains is better than the initial gain percentage). A negative(arrow down) indicates that you averaged up.")

        colB31, colB32 = st.columns(2, border=True)
        colB31.metric(label="New total gross amount invested", 
                    value=f"{CURRENCY} {round(new_gross_amount,4):,}", 
                    help="Sum of all purchases with cummulative fees (broker commission / spread).")
        colB32.metric(label="New total net amount invested", 
                    value=f"{CURRENCY} {round(new_net_amount,2):,}", 
                    help="Sum of previous total and the new amount that is solely invested in the shares.")
        
        
        
        st.subheader('C: Determine the target selling price of all your current stocks based on your preferred gain percentage.')
        set_target_gain = st.number_input('What is your target gain percentage (%)? ')
    
        ### CALCULATOR FORMULA - C ###
        target_selling_price = ((gross_amount) * (1 + (set_target_gain/100)))/(total_shares_bought*(1-(set_tax/100)))

        new_target_selling_price = ((new_gross_amount) * (1 + (set_target_gain/100)))/(new_total_shares_bought*(1-(set_tax/100)))

        st.markdown(f''':violet[To gain {set_target_gain}% with the initial shares of {round(total_shares_bought,2)}, you should set the target selling price to: ***{CURRENCY} {round(target_selling_price,2)}***]''')
        st.markdown(f''':violet[To gain {set_target_gain}% with the new total shares of {round(new_total_shares_bought,4)}, you should set the target selling price to: ***{CURRENCY} {round(new_target_selling_price,2)}***]''')
        
        expander2 = st.expander("See the breakdown: ") 
        expander2.markdown(f"""***Target selling price based on initial investment*** = (gross_amount * (1 + (set_target_gain/100))) / (total_shares_bought * (1-(set_tax/100)))""")
        expander2.markdown(f''' = ({gross_amount} * (1+({set_target_gain}/100))) / ({total_shares_bought} * (1-({set_tax}/100)))''')
        expander2.markdown(f''' = ({gross_amount} * {(1+(set_target_gain/100))}) / ({total_shares_bought} * {(1-(set_tax/100))})''')
        expander2.markdown(f''' = ***{CURRENCY} {(gross_amount * (1+(set_target_gain/100))) / (total_shares_bought * (1-(set_tax/100)))}***''')


        expander2.markdown(f"""***Target selling price with the additional investment*** = (gross_amount * (1 + (set_target_gain/100))) / (total_shares_bought * (1-(set_tax/100)))""")
        expander2.markdown(f''' = ({new_gross_amount} * (1+({set_target_gain}/100))) / ({new_total_shares_bought} * (1-({set_tax}/100)))"""''')
        expander2.markdown(f''' = ({new_gross_amount} * {(1+(set_target_gain/100))}) / ({new_total_shares_bought} * {(1-(set_tax/100))})''')
        expander2.markdown(f''' = ***{CURRENCY} {(new_gross_amount * (1+(set_target_gain/100))) / (new_total_shares_bought * (1-(set_tax/100)))}***''')

        break


    elif user_prompt == 'remove':
        try:
            all_events = fc.get_event() # Get the existing transactions
            st.table(all_events)
            entry_to_remove = int(st.text_input('Enter the row index: '))
            if entry_to_remove not in range (len(all_events)):
                st.warning('Provided row# does not exist.')
            else:
                all_events.pop(entry_to_remove)
                #pprint(all_events)
                st.info(f'Row #{entry_to_remove} has been removed.')
                st.write('The updated transactions: ')
                st.table(all_events)
                fc.write_event(all_events) # Write all events to the CSV file
                break
        except:
            break

    elif user_prompt == 'edit':
        try:
            all_events = fc.get_event() # Get the existing transactions
            st.table(all_events)
            entry_to_edit = int(st.text_input('Enter the row index: '))
            if entry_to_edit not in range (len(all_events)):
                st.warning('Provided row # does not exist.')
            else:
                edited = fc.transaction_form()
                all_events[entry_to_edit] = edited 
                #pprint(all_events)
                if True:
                    st.write(f'With the updated row #{entry_to_edit + 1}: ')
                    st.table(all_events)
                    fc.write_event(all_events) # Write all events to the CSV file
                    break
        
        except:
            break

    else:
        #print('exiting...')
        break

