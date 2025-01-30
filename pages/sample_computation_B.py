import streamlit as st
import pandas as pd

CURRENCY = '$'

st.title("PyBlot's Basic Cost Averaging Calculator ")
st.subheader("Sample Computation - Part B:")

#st.subheader('*Sample* Summary of Investment: ')

total_shares_bought = 120
cost_ave_result = 90
gross_amount = 10855
net_amount = float(cost_ave_result) * float(total_shares_bought)
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

    st.markdown(f'''***An investment of USD {buy_new_gross_amount}***, and bid ***USD {buy_new_price_ave_down}*** per share has been added.''')
    st.markdown(f'''When the stock reaches the ***market price of {current_stock_price}***, then the new summary of investment will be: ''')

    new_shares_ave_down = (buy_new_gross_amount*(1-(fees_percentage/100)))/buy_new_price_ave_down
    new_total_shares_bought = total_shares_bought + new_shares_ave_down
    new_gross_amount = gross_amount + buy_new_gross_amount
    new_net_amount = net_amount + (buy_new_gross_amount*(1-(fees_percentage/100)))
    new_ave_share_price = new_net_amount/new_total_shares_bought
    gains_loss_currency = (new_total_shares_bought*current_stock_price*(1-(fees_percentage/100))) - new_gross_amount
    gains_loss_percent = (((new_total_shares_bought*current_stock_price*(1-(fees_percentage/100))) - new_gross_amount)/new_gross_amount) * 100
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

    colB41, colB42 = st.columns(2, border=True)
    colB41.metric(label="Total gain/loss", 
                value=f"{CURRENCY} {round(gains_loss_currency,2):,}", 
                help="Gains/losses in currency = (total_shares_bought * current_stock_price) - fees - gross_amount ")
    colB42.metric(label="Percent gain/loss", 
                value=f"{round(gains_loss_percent,4):,} %", 
                help="Gains/losses in percentage = ((total_shares_bought * current_stock_price) - fees - gross_amount) * 100 / gross_amount ")

    
    expander8 = st.expander("See the breakdown: ") 
    expander8.markdown(f'''**Additional shares bought** ''')
    expander8.markdown(f''' = (additional investment * (1-(fees_percentage/100))) / bid_price''')
    expander8.markdown(f''' = ({buy_new_gross_amount} * (1-({fees_percentage}/100))) / {buy_new_price_ave_down} ''')
    expander8.markdown(f''' = ({buy_new_gross_amount} * {(1-(fees_percentage/100))}) / {buy_new_price_ave_down} ''')
    expander8.markdown(f''' = {buy_new_gross_amount * (1-(fees_percentage/100))} / {buy_new_price_ave_down} ''')
    expander8.markdown(f''' = ***{buy_new_gross_amount * (1-(fees_percentage/100))  / buy_new_price_ave_down} unit(s)***''')
    
    expander8.markdown(f'''**Additional net amount invested** *(no tax applied when buying; only fees)*''')
    expander8.markdown(f''' = additional investment * (1-(fees_percentage/100))''')
    expander8.markdown(f''' = {buy_new_gross_amount} * (1-({fees_percentage}/100))  ''')
    expander8.markdown(f''' = {buy_new_gross_amount} * {(1-(fees_percentage/100))}  ''')
    expander8.markdown(f''' = ***{CURRENCY} {(buy_new_gross_amount * (1-(fees_percentage/100))):,}***''')
    
    expander8.markdown(f'''**New total shares bought** ''')
    expander8.markdown(f''' = initial total shares + ((additional investment * (1-(fees_percentage/100))) / bid_price)''')
    expander8.markdown(f''' = {total_shares_bought} + (({buy_new_gross_amount} * (1-({fees_percentage}/100))) / {buy_new_price_ave_down}) ''')
    expander8.markdown(f''' = {total_shares_bought} + {((buy_new_gross_amount * (1-(fees_percentage/100))) / buy_new_price_ave_down)} ''')
    expander8.markdown(f''' = ***{total_shares_bought + ((buy_new_gross_amount * (1-(fees_percentage/100))) / buy_new_price_ave_down)} unit(s)***''')

    expander8.markdown(f'''**New average price**''')
    expander8.markdown(f''' = (net amount invested + additional net amount invested) / (total shares bought + additional shares bought) ''')
    expander8.markdown(f''' = {new_net_amount} / {new_total_shares_bought}  ''')
    #expander8.markdown(f''' = {(buy_new_gross_amount * (1-(fees_percentage/100))) + net_amount} / {new_total_shares_bought} ''')
    expander8.markdown(f''' = ***{CURRENCY} {new_net_amount/new_total_shares_bought}***''')

    expander8.markdown(f'''**Initial versus New Average Price - comparison**''')
    expander8.markdown(f''' = initial average share price - new average price   ''')
    expander8.markdown(f''' = {cost_ave_result} - {new_ave_share_price}  ''')
    expander8.markdown(f''' = ***{cost_ave_result - new_ave_share_price}***''')

    expander8.markdown(f'''**New total gross amount invested**''')
    expander8.markdown(f''' = (gross amount invested + additional investment) ''')
    expander8.markdown(f''' = {gross_amount} + {buy_new_gross_amount} ''')
    expander8.markdown(f''' = ***{CURRENCY} {gross_amount + buy_new_gross_amount}***''')

    expander8.markdown(f'''**New total net amount invested**''')
    expander8.markdown(f''' = (net amount invested + additional net amount invested) ''')
    expander8.markdown(f''' = {(buy_new_gross_amount * (1-(fees_percentage/100)))} + {net_amount} ''')
    expander8.markdown(f''' = ***{CURRENCY} {new_net_amount}***''')



st.write(f'Sample Calculation # 1')
calc_B(1000, 60, 150)

st.write('-----------------------------------------------------') 
st.write(f'Sample Calculation # 2')
calc_B(1000, 150, 150)