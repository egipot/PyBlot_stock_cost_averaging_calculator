import streamlit as st
import pandas as pd

st.title("How to use: PyBlot's Cost Averaging Calculator ")

st.text('\n')
st.subheader('Functions available:')
st.text('  - ADD: to fill up a purchase or investment. Different brokers provide various combinations of parameters during order/purchase transactions. As examples:')
st.write('      - Broker_A may ask you for the investment amount and bid price - also known as the ***limit order***, then they will calculate the units that can be bought. ***This calculator uses this approach in CALCULATE function (part B)*** ')
st.write('      - Broker_B may ask you for the investment amount only, and they will set the bid price according to the current market price - also known as the market order.')
st.write('      - Broker_C may ask you for the number of shares and bid price, then validating if the available balance is enough for such purchase.')

st.text('  - VIEW: to display the currently saved transactions.')
st.text('  - EDIT: to re-enter each detail of the specified transaction based on row number. ')
st.text('  - REMOVE: to delete a transaction by entering the row number.')
st.text('  - CALCULATE has these successive operations:')
st.write('      - [By default] Get the summary of the current data (total shares bought, average price of purchases, total investment and fees.)')
st.write('      - [Part A] Provide the present market price of the stock to know if you have gains or losses in your investment ')
st.write('      - [Part B: Optional] This section can simulate an average-down (buying more stocks at a lower price than the initial average price) or average-up (vice-versa) purchase. This will affect how your future profits/losses will be, based on the future market price. If you refuse to add further investment and directly proceed to part C (getting target sell price based on profit percentage), just enter zeros this section.')
st.write('      - [Part C] Set your target earnings (in percentage) and get the target selling price to achieve such gain (after tax and broker fees). This way, you can easily monitor and set price alerts, as the stock reaches that price. It is good to have a sound plan and detach to emotions when it comes to investing :) ')
st.text('\n')

st.subheader("Disclaimers:")
st.markdown(''':orange[1. This calculator is intended to calculate positions for one stock only.]''')
st.markdown(''':orange[2. No leveraging (1:1) is used during all the purchase transactions.]''')
st.markdown(''':orange[3. For now, the currency is hard-coded to USD ($). Next improvement is to represent the currency according to your input. However, this will not affect the numerical values.]''')
st.markdown(''':orange[4. This calculator is for public use, so the current data in the table may be changed by different users.]''')
st.markdown('''**:orange[5. Warning: Switching the page from the sidebar will restart the app, which means you need to select the function [add, view, edit, calculate, remove].]**''')
st.markdown(''':red-background[6. The formula of calculations are based on the assumption that **broker fees are applied in both buying and selling transactions.** And that **tax is applied only when stocks are sold.**]''')
st.text('\n')

st.subheader("Improvement Plans:")
st.markdown(''':violet[1. Option to set the fees in either percentage or amount.]''')
st.markdown(''':violet[2. Visualizing the investment growth in a chart.]''')
st.text('\n')

st.subheader('Alternatively, you may also check these tools and references: ')
st.write('      - https://www.investopedia.com/ask/answers/05/stockgainsandlosses.asp')
st.write('      - https://stock-calculator.net/en/profit ')
st.write('      - https://www.stockaveragecalculator.com/ ')
st.write('      - https://www.inchcalculator.com/stock-average-calculator/ ')
st.write('      - https://goodcalculators.com/stock-calculator/ ')
st.write('      - https://downtownbedandbreakfast.com/article/how-do-you-calculate-the-percentage-gain-or-loss-on-an-investment/2420 ')
