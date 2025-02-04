import streamlit as st
import pandas as pd

CURRENCY = '$'

st.title("PyBlot's Basic Cost Averaging Calculator ")
st.subheader("Sample Computation - Part C:")

st.write('Assuming that you have: ')
st.markdown('''
            - Total shares bought: 120 units\n
            - Average share price: USD 90\n
            - Initial gross amount invested: USD 10,855\n
            - Initial net amount invested: USD 10,800\n
            - Total commission/spread/fees: USD 55\n
            - Total commission/spread/fees in percentage: 0.5067%\n
            ''')
total_shares_bought = 120
cost_ave_result = 90
gross_amount = 10855
net_amount = float(cost_ave_result) * float(total_shares_bought)
fees = gross_amount - (float(cost_ave_result)*float(total_shares_bought))
fees_percentage = (fees / gross_amount)*100


set_tax = 10
buy_new_gross_amount = 1000 
buy_new_price_ave_down = 60
current_stock_price = 150

st.markdown(f'''***Adding an investment of :violet-background[USD {buy_new_gross_amount}]***, with bid price set at ***:violet-background[USD {buy_new_price_ave_down} per share.]***''')
st.markdown('''
            - New total shares bought: 136.5822 units\n
            - New average share price: USD 86.3577\n
            - New gross amount invested: USD 11,855\n
            - New net amount invested: USD 11,794.93\n
            ''')


new_shares_ave_down = (buy_new_gross_amount*(1-(fees_percentage/100)))/buy_new_price_ave_down
new_total_shares_bought = total_shares_bought + new_shares_ave_down
new_gross_amount = gross_amount + buy_new_gross_amount
new_net_amount = 11794.93
new_ave_share_price = new_net_amount/new_total_shares_bought
gains_loss_currency = (new_total_shares_bought*current_stock_price*(1-(fees_percentage/100))*(1-(set_tax/100))) - new_gross_amount
gains_loss_percent = (((new_total_shares_bought*current_stock_price*(1-(fees_percentage/100))*(1-(set_tax/100))) - new_gross_amount)/new_gross_amount) * 100
value_metric = new_ave_share_price
delta_metric = new_ave_share_price - cost_ave_result 


st.subheader('C: Determine the target selling price of all your current stocks based on your preferred gain percentage.')
def calc_c(set_target_gain):
    st.markdown(f'Assuming that you set a target gain percentage of **:green[{set_target_gain} %]** :')
    st.markdown(f'And the tax required in your country is :red[{set_tax} %] :')
    ### CALCULATOR FORMULA - C ###
    target_selling_price = (gross_amount * (1 + (set_target_gain / 100))) / (total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))

    new_target_selling_price = (new_gross_amount * (1 + (set_target_gain / 100))) / (new_total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))

    st.markdown(f''':violet[To gain {set_target_gain}% with the initial shares of {round(total_shares_bought,2)}, you should set the target selling price to: ***{CURRENCY} {round(target_selling_price,2)}***]''')
    st.markdown(f''':violet[To gain {set_target_gain}% with the new total shares of {round(new_total_shares_bought,4)}, you should set the target selling price to: ***{CURRENCY} {round(new_target_selling_price,2)}***]''')
    
    expander2 = st.expander("See the breakdown: ") 
    #target = (gross_amount * (1 + (set_target_gain / 100))) / (total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))
    expander2.markdown(f"""***Target selling price based on initial investment*** = (Initial total gross amount invested * (1 + (target gain percentage / 100))) / (total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100)))) """)
    expander2.markdown(f''' = ({gross_amount} * (1 + ({set_target_gain} / 100))) / ({total_shares_bought} * (1 - (({set_tax} / 100) + ({fees_percentage} / 100))))''')
    expander2.markdown(f''' = ({gross_amount} * {(1 + (set_target_gain / 100))}) / ({total_shares_bought} * (1 - {((set_tax / 100) + (fees_percentage / 100))}))''')
    expander2.markdown(f''' = {(gross_amount * (1 + (set_target_gain / 100)))} / {(total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))}''')
    expander2.markdown(f''' = ***{CURRENCY} {(gross_amount * (1 + (set_target_gain / 100))) / (total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))}***''')

    expander2.markdown(f"""***Target selling price based on initial investment*** = (New total gross amount invested * (1 + (target gain percentage / 100))) / (New total shares bought * (1 - ((set_tax / 100) + (fees_percentage / 100)))) """)
    expander2.markdown(f''' = ({new_gross_amount} * (1 + ({set_target_gain} / 100))) / ({new_total_shares_bought} * (1 - (({set_tax} / 100) + ({fees_percentage} / 100))))''')
    expander2.markdown(f''' = ({new_gross_amount} * {(1 + (set_target_gain / 100))}) / ({new_total_shares_bought} * (1 - {((set_tax / 100) + (fees_percentage / 100))}))''')
    expander2.markdown(f''' = {(new_gross_amount * (1 + (set_target_gain / 100)))} / {(new_total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))}''')
    expander2.markdown(f''' = ***{CURRENCY} {(new_gross_amount * (1 + (set_target_gain / 100))) / (new_total_shares_bought * (1 - ((set_tax / 100) + (fees_percentage / 100))))}***''')




calc_c(50)
st.write('________________________________')
calc_c(80)
st.write('________________________________')
calc_c(100)

st.subheader ('Notice how the average-down share price after the additional investment affected the lower target selling price to get the preferred percent gain. ')