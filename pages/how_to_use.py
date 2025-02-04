
import streamlit as st

st.title("How to use: PyBlot's Cost Averaging Calculator ")

st.text('\n')
st.subheader('Functions available:')
st.text('  - ADD: to fill up a purchase or investment')
st.text('  - VIEW: to display the currently entered transactions.')
st.text('  - EDIT: to re-enter each detail of the specified transaction based on row number. ')
st.text('  - REMOVE: to delete a transaction by entering the row number.')
st.text('  - CALCULATE has these successive operations:')
st.write('      - [By default] Get the summary of the current data (total shares bought, average price of purchases, total investment and fees.)')
st.write('      - [Part A] Provide the present market price of the stock to know if you have gains or losses in your investment ')
st.write('      - [Part B: Optional] If you refuse to add further investment and directly proceed to part C (getting target sell price based on profit percentage), just enter zeros in the additional investments.')
st.write('      - [Part C] Set your target earnings (in percentage) and get the target selling price to achieve such gain (after tax and broker fees). This way, you can easily monitor and set price alerts, as the stock reaches that price. It is good to have a sound plan and detach to emotions when it comes to investing :) ')
st.text('\n')


st.subheader("Disclaimers:")
st.markdown(''':orange[1. This calculator is intended to calculate positions for one stock only.]''')
st.markdown(''':orange[2. For now, the currency is hard-coded to USD ($). Next improvement is to represent the currency according to your input. However, this will not affect the numerical values.]''')
st.markdown(''':orange[3. This calculator is for public use, so the current data in the table may be changed by different users.]''')
st.markdown(''':orange-background[4. The formula of calculations are based on the assumption that **broker fees are applied in both buying and selling transactions.** And that **tax is applied only when stocks are sold.**]''')

st.subheader("Improvement Plans:")
st.markdown(''':violet[1. Option to set the fees in either percentage or amount.]''')
st.markdown(''':violet[2. Downloading the results into PDF.]''')
st.markdown(''':violet[3. Blank template for downloading, and the option to upload your own CSV file for easier input.]''')
st.markdown(''':violet[4. Visualizing the investment growth in a chart.]''')

st.subheader('Alternatively, you may also check these tools and references: ')
st.markdown(':gray[ https://www.investopedia.com/ask/answers/05/stockgainsandlosses.asp ]')
st.markdown(':gray[ https://stock-calculator.net/en/profit ]')
st.markdown(':gray[ https://www.stockaveragecalculator.com/ ]')
st.markdown(':gray[ https://www.inchcalculator.com/stock-average-calculator/ ]')
st.markdown(':gray[ https://goodcalculators.com/stock-calculator/ ]')
st.markdown(':gray[ https://downtownbedandbreakfast.com/article/how-do-you-calculate-the-percentage-gain-or-loss-on-an-investment/2420 ]')
