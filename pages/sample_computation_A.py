import pandas as pd
import functions_calc as fc
import streamlit as st

CURRENCY = '$'

st.title("PyBlot's Basic Cost Averaging Calculator ")
st.subheader("Sample Computation - Part A: " )
all_sample = fc.get_sample() # Get the existing transactions
df = pd.DataFrame(all_sample)
st.table(all_sample)

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


other_fees = 30.00  
dividends = 10.00
col41, col42, = st.columns(2)
col41.metric(label="Other fees (maintenance, withdrawal, etc)", 
                            value=f"{CURRENCY} 30.00", 
                            border=True, 
                            help="You may also add fees that may have been visible later in your statement of account, for example, fees for account maintenance or withdrawal, etc...")
col42.metric(label="Dividends", 
                            value=f"{CURRENCY} 10.00", 
                            border=True, 
                            help="Please check your statement of account and add here the total dividends received for this stock.")

st.subheader('A: Calculate the gain/loss percentage based on the current price.')
set_tax = 10 

def calculationA_sample():
    values = [200, 103.7832, 90]
    sample_type = ['Investment with Gains', 'Breakeven', 'Investment with Losses']
    for index, current_stock_price in enumerate(values):
        st.write('-----------------------------------------------------') 
        st.markdown(f'***Sample Calculation # {index+1}: :blue-background[{sample_type[index]}]***')
        st.markdown(f'''Assuming the current stock price = ***{CURRENCY} {current_stock_price}***''')
        current_invest_value = total_shares_bought * current_stock_price
        st.write(f"""***Gross investment's value: {CURRENCY} {round(current_invest_value,4):,}***""" )
    
        set_tax = 10
        
        current_invest_value_minus_fees_and_tax = (total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100)) - other_fees + dividends
        
        gain_loss_if_selling_in_current_price =  ((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - (gross_amount) - other_fees + dividends
        
        initial_gain_loss_value = ((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount - other_fees + dividends
        initial_gain_loss_percentage = (((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount - other_fees + dividends )*100 / gross_amount


        #if with gains
        if  initial_gain_loss_value > 0.01:  
            st.markdown(f''':green[The total amount that you will receive after selling is: ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***!] ''') 
            st.markdown(f''':green[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the fees and tax and adding the received dividends, your profit is: ***{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}***]''')
            st.markdown(f''':green[That is ***{round(initial_gain_loss_percentage,4):,}%*** initial gain!]''')
            st.markdown(f''':green[Congratulations! Keep on investing and learning!]''')

            expander3 = st.expander("See the breakdown: ") 
            expander3.markdown(f"""***Gross investment value*** = total shares bought * current share price = {total_shares_bought} * {current_stock_price} = ***{CURRENCY} {total_shares_bought * current_stock_price}***""")
            expander3.markdown('''Derive the ***total amount that you will receive after selling:***''')
            expander3.markdown(f''' = [Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))] - other fees + dividends''')
            expander3.markdown(f''' = [{total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))] - other fees + dividends''')
            expander3.markdown(f''' = {total_shares_bought} * {current_stock_price} * {(1-(fees_percentage/100))} * {(1-(set_tax/100))} - {other_fees} + {dividends} = ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***''')
            expander3.markdown(f'''***Profit / Loss in currency*** ''')
            expander3.markdown(f''' = [Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))] - initial gross amount invested - other fees + dividends''')
            expander3.markdown(f''' = [{total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))] - {gross_amount} - {other_fees} + {dividends} = ***{CURRENCY} {round(initial_gain_loss_value,2):,}*** ''')
            expander3.markdown(f'''***Profit / Loss in percentage***  ''')
            expander3.markdown(f''' = [(Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))) - initial gross amount invested - other fees + dividends] *100 / Initial gross amount invested ''')
            expander3.markdown(f''' = [({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))) - {gross_amount} - {other_fees} + {dividends}] * 100 / {gross_amount}  = ***{round(initial_gain_loss_percentage,4):,} %*** ''')

        #elif breakeven (gain is between 0 and 0.01)    
        elif  0.0 <= initial_gain_loss_value <= 0.01: 
            #st.markdown(f''':blue[The total amount that you will receive after selling is: {CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}!] ''')
            st.markdown(f''':blue[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% fees and {set_tax}% tax, you are expected to receive: {CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}]''')
            st.markdown(f''':blue[Breakeven. You just paid your broker and taxes without income. Congratulations on being a good citizen!]''')

            expander4 = st.expander("See the breakdown: ") 
            expander4.markdown(f"""***Gross investment value*** = total shares bought * current_stock_price = {total_shares_bought} * {current_stock_price} = ***{CURRENCY} {total_shares_bought * current_stock_price}***""")
            expander4.markdown('''Derive the ***total amount that you will receive after selling:***''')
            expander4.markdown(f''' = [Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))]  - other fees + dividends''')
            expander4.markdown(f''' = [{total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))]  - {other_fees} + {dividends}''')
            expander4.markdown(f''' = {total_shares_bought} * {current_stock_price} * {(1-(fees_percentage/100))} * {(1-(set_tax/100))}  - {other_fees} + {dividends} = ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***''')
            expander4.markdown(f'''***Profit / Loss in currency*** ''')
            expander4.markdown(f''' = [Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))] - initial gross amount invested  - other fees + dividends''')
            expander4.markdown(f''' = [{total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))] - {gross_amount} - {other_fees} + {dividends} = ***{CURRENCY} {round(initial_gain_loss_value,2):,}*** ''')
            expander4.markdown(f'''***Profit / Loss in percentage*** ''')
            expander4.markdown(f''' = [(Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))) - initial gross amount invested - other fees + dividends] *100 / initial gross amount invested ''')
            expander4.markdown(f''' = [({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))) - {gross_amount} - {other_fees} + {dividends}] * 100 / {gross_amount} = ***{round(initial_gain_loss_percentage,4):,} %*** ''')

        #else with losses 
        else: 
            #st.markdown(f''':red[{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}]''')
            st.markdown(f''':red[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% fees and {set_tax}% tax, your balance will be deducted by: ***{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}***]''')
            st.markdown(f''':red[Your investment is at ***{round(initial_gain_loss_percentage,4):,}%*** loss. Do not worry, this is just a paperloss if you average down. Just make sure that the company is still worth investing in...]''')
            

            expander5 = st.expander("See the breakdown: ") 
            expander5.markdown(f"""***Gross investment value*** = total shares bought * current share price = {total_shares_bought} * {current_stock_price} = ***{CURRENCY} {total_shares_bought * current_stock_price}***""")
            expander5.markdown('''Derive the ***total amount that you will receive after selling:***''')
            expander5.markdown(f''' = Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100)) - other fees + dividends''')
            expander5.markdown(f''' = [{total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))] - {other_fees} + {dividends} ''')
            expander5.markdown(f''' = {total_shares_bought} * {current_stock_price} * {(1-(fees_percentage/100))} * {(1-(set_tax/100))} - {other_fees} + {dividends} = ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***''')
            expander5.markdown(f'''***Profit / Loss in currency*** ''')
            expander5.markdown(f''' = [Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))] - initial gross amount invested - other fees + dividends''')
            expander5.markdown(f''' = [{total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))] - {gross_amount} - {other_fees} + {dividends} = ***{CURRENCY} {round(initial_gain_loss_value,2):,}*** ''')
            expander5.markdown(f'''***Profit / Loss in percentage***  ''')
            expander5.markdown(f''' = [(Total shares bought * current share price * (1-(fees percentage/100)) * (1-(tax percentage/100))) - initial gross amount invested - other fees + dividends] * 100 / initial gross amount invested ''')
            expander5.markdown(f''' = [({total_shares_bought} * {current_stock_price} * (1-({fees_percentage}/100)) * (1-({set_tax}/100))) - {gross_amount} - {other_fees} + {dividends}] * 100 / {gross_amount} = ***{round(initial_gain_loss_percentage,4):,} %*** ''')


       



calculationA_sample()

