import streamlit as st
import pandas as pd

CURRENCY = '$'

st.title("PyBlot's Basic Cost Averaging Calculator ")
st.subheader("Sample Computation - Part B:")

st.subheader('Sample Summary of Investment: ')

total_shares_bought = 120
cost_ave_result = 90
gross_amount = 10855
net_amount = float(cost_ave_result) * float(total_shares_bought)
st.markdown(f'''***Net investment amount: {CURRENCY} {net_amount}***''')
fees = gross_amount - (float(cost_ave_result)*float(total_shares_bought))
fees_percentage = (fees / gross_amount)*100

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
                            value=f"{CURRENCY} {net_amount:,}", 
                            border=True, 
                            help="Total amount paid solely for the stocks.")

col31, col32, = st.columns(2)
col31.metric(label="Total commission/spread/fees", 
                            value=f"{CURRENCY} {fees:,}", 
                            border=True, 
                            help="Total fees due to broker commission, spread, ...")
col32.metric(label="Total commission/spread/fees in percentage", 
                            value=f"{round(fees_percentage,4)} %", 
                            border=True, 
                            help="Total amount paid solely for the stocks.")


st.subheader('B: Buy more shares at your preferred price and get the updated average share price and gain/loss percentage of your investment.')
        
### CALCULATOR FORMULA - B ###
#buy_new_gross_amount = float(st.number_input(f'How much are you willing to add in your investment? {CURRENCY} '))
#buy_new_price_ave_down = float(st.number_input(f'How much is your bidding price? {CURRENCY} '))
# buy_new_gross_amount = 1000
# buy_new_price_ave_down = 60
# current_stock_price = 300

def calc_B(buy_new_gross_amount, buy_new_price_ave_down, current_stock_price):

    set_tax = 10

    st.markdown(f'''***If you add an investment amounting to = {CURRENCY} {buy_new_gross_amount}***''')
    st.markdown(f'''***And bid a share price =  {CURRENCY} {buy_new_price_ave_down}***''')
    st.markdown(f'Then the new summary of investment will be: ')


    new_shares_ave_down = (buy_new_gross_amount*(1-(fees_percentage/100))*(1-(set_tax/100)))/buy_new_price_ave_down
    new_total_shares_bought = total_shares_bought + new_shares_ave_down
    new_gross_amount = gross_amount + buy_new_gross_amount
    new_net_amount = net_amount + (buy_new_gross_amount*(1-(fees_percentage/100))*(1-(set_tax/100)))
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


st.write(f'Sample Calculation # 1')
# buy_new_gross_amount = 1000
# buy_new_price_ave_down = 60
# current_stock_price = 300
calc_B(1000, 60, 300)

st.write('-----------------------------------------------------') 
st.write(f'Sample Calculation # 2')
# buy_new_gross_amount = 1000
# buy_new_price_ave_down = 60
# current_stock_price = 300
calc_B(1000, 150, 300)