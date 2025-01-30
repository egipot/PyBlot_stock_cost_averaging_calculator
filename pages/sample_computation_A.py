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


st.subheader('A: Calculate the gain/loss percentage based on the current price.')
set_tax = 10 

def calculationA_sample():
    values = [200, 103.3365, 90]
    sample_type = ['Investment with Gains', 'Breakeven', 'Investment with Losses']
    for index, current_stock_price in enumerate(values):
        st.write('-----------------------------------------------------') 
        st.write(f'Sample Calculation # {index+1}: {sample_type[index]}')
        st.markdown(f'''Assuming the current stock price = ***{CURRENCY} {current_stock_price}***''')
        current_invest_value = total_shares_bought * current_stock_price
        st.write(f"""***Gross investment's value: {CURRENCY} {round(current_invest_value,4):,}***""" )
    
        set_tax = 10
        
        current_invest_value_minus_fees_and_tax = (total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))
        
        gain_loss_if_selling_in_current_price =  ((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - (gross_amount)
        
        initial_gain_loss_value = ((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount
        initial_gain_loss_percentage = (((total_shares_bought * current_stock_price)*(1-(fees_percentage/100))*(1-(set_tax/100))) - gross_amount)*100 / gross_amount


        if  initial_gain_loss_value > 0.01:  
            st.markdown(f''':green[The total amount that you will receive after selling is: ***{CURRENCY} {round(current_invest_value_minus_fees_and_tax,2):,}***!] ''') 
            st.markdown(f''':green[If you sell all {round(total_shares_bought,2):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% fees and {set_tax}% tax, your profit is: ***{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}***]''')
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
            st.markdown(f''':blue[If you sell all {round(total_shares_bought,4):,} shares at the current price of {current_stock_price}, then deducting the {fees_percentage}% fees and {set_tax}% tax, you are expected to receive: {CURRENCY} {round(gain_loss_if_selling_in_current_price,4):,}]''')
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
            st.markdown(f''':red[If you sell all {round(total_shares_bought,2):,} shares at the current price of USD {current_stock_price}, then deducting the {fees_percentage}% fees and {set_tax}% tax, your balance will be deducted by: ***{CURRENCY} {round(gain_loss_if_selling_in_current_price,2):,}***]''')
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


calculationA_sample()

