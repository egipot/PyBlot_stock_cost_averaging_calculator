
import streamlit as st

#st.set_page_config(page_title='Using Cost_Average_Calculator')
st.title("How to use: PyBlot's Basic Cost Averaging Calculator ")
st.subheader("")
st.markdown(''':orange[1. This calculator is intended to calculate positions for one stock only.]''')
st.markdown(''':orange[2. For now, the currency is hard-coded to USD ($). Next improvement is to represent the currency according to your input. However, this will not affect the numerical values.]''')

st.text('\n')
st.subheader('Functions available:')
st.text('  - ADD: to fill up a purchase or investment')
st.text('  - VIEW: to display the currently entered transactions.')
st.text('  - EDIT: to re-enter each detail of the specified transaction based on row number. ')
st.text('  - REMOVE: to delete a transaction by entering the row number.')
st.text('  - CALCULATE has three successive operations:')
st.write('      - get the summary of the current data (total shares bought, average price of purchases, total investment and fees.)')
st.write('      - provide the present market price of the stock and know if you have gains or losses so far in your investment.')
st.write('      - set your target earnings and monitor as the stock reaches the calculated price. It is good to have a sound plan and detach to emotions when it comes to investing :) ')
st.text('\n')
st.markdown(':orange[Alternatively, you may also check this tool: https://www.inchcalculator.com/stock-average-calculator/]')
