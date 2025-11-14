import streamlit as st

# Page configuration
st.set_page_config(page_title="Trading Calculator", page_icon="📊", layout="wide")

# Title and description
st.title("📊 Trading Calculator")
st.markdown("Calculate your trading profits with transaction fees")

# Fee percentage
FEE_PERCENTAGE = 1.12 # change accordinlgy

# Input section
st.subheader("Trade Details")

col1, col2, col3 = st.columns(3)

with col1:
    buy_price = st.number_input("Buy Price", min_value=0.0, value=100.0, step=1.0, format="%.2f")
    
with col2:
    sell_price = st.number_input("Sell Price", min_value=0.0, value=105.0, step=1.0, format="%.2f")

with col3:
    quantity = st.number_input("No. of Stocks", min_value=1, value=1, step=1)

# Trading day option
same_day = st.radio(
    "Trading Type",
    options=["Same Day Trading", "Sell on Another Day"],
    help="Same day trading: Fee charged once. Another day: Fee charged twice."
)

st.divider()

# Calculations
if same_day == "Same Day Trading":
    # Fee charged once (on buy)
    total_buy_value = buy_price * quantity
    buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
    total_cost = total_buy_value + buy_fee
    
    total_sell_value = sell_price * quantity
    sell_fee = 0
    proceeds = total_sell_value
    fee_count = "1x"
else:
    # Fee charged twice (on buy and sell)
    total_buy_value = buy_price * quantity
    buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
    total_cost = total_buy_value + buy_fee
    
    total_sell_value = sell_price * quantity
    sell_fee = total_sell_value * (FEE_PERCENTAGE / 100)
    proceeds = total_sell_value - sell_fee
    fee_count = "2x"

# Calculate gain/loss
gain_loss = proceeds - total_cost
gain_loss_percentage = (gain_loss / total_cost) * 100 if total_cost > 0 else 0

# Display results
st.subheader("📈 Calculation Results")

# Buy section
st.markdown("### 🟢 Buy Transaction")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Quantity", f"{quantity}")
with col2:
    st.metric("Buy Price", f"Rs. {buy_price:.2f}")
with col3:
    st.metric("Fee (1.12%)", f"Rs. {buy_fee:.3f}")
with col4:
    st.metric("Total Cost", f"Rs. {total_cost:.2f}", delta=None, delta_color="normal")

st.divider()

# Sell section
st.markdown("### 🔴 Sell Transaction")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Quantity", f"{quantity}")
with col2:
    st.metric("Sell Price", f"Rs. {sell_price:.2f}")
with col3:
    if same_day == "Same Day Trading":
        st.metric("Fee", "Rs. 0.00", help="No fee on same day sell")
    else:
        st.metric("Fee (1.12%)", f"Rs. {sell_fee:.3f}")
with col4:
    st.metric("Proceeds", f"Rs. {proceeds:.3f}")

st.divider()

# Profit/Loss section
st.markdown("### 💰 Profit/Loss Summary")
col1, col2, col3 = st.columns(3)

with col1:
    if gain_loss >= 0:
        st.metric("Gain/Loss", f"Rs. {gain_loss:.3f}", delta=f"+{gain_loss:.3f}", delta_color="normal")
    else:
        st.metric("Gain/Loss", f"Rs. {gain_loss:.3f}", delta=f"{gain_loss:.3f}", delta_color="inverse")

with col2:
    if gain_loss_percentage >= 0:
        st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"+{gain_loss_percentage:.2f}%")
    else:
        st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"{gain_loss_percentage:.2f}%", delta_color="inverse")

with col3:
    total_fees = buy_fee + sell_fee
    st.metric("Total Fees", f"Rs. {total_fees:.3f}", help=f"Fee charged {fee_count}")


st.markdown("")
st.markdown("")
# Info box
st.info(f"""
**Fee Structure:**
- Transaction Fee: **{FEE_PERCENTAGE}%**
- Same Day Trading: Fee charged **once** (on buy only)
- Sell on Another Day: Fee charged **twice** (on buy and sell)
""")

# Detailed breakdown (expandable)
with st.expander("📋 Detailed Breakdown"):
    st.markdown(f"""
    **Buy Transaction:**
    - Quantity: {quantity} stocks
    - Buy Price per Stock: Rs. {buy_price:.2f}
    - Total Buy Value: Rs. {total_buy_value:.2f}
    - Buy Fee ({FEE_PERCENTAGE}%): Rs. {buy_fee:.3f}
    - **Total Cost: Rs. {total_cost:.2f}**
    
    **Sell Transaction:**
    - Quantity: {quantity} stocks
    - Sell Price per Stock: Rs. {sell_price:.2f}
    - Total Sell Value: Rs. {total_sell_value:.2f}
    - Sell Fee: Rs. {sell_fee:.3f} {'(No fee - same day)' if same_day == 'Same Day Trading' else f'({FEE_PERCENTAGE}%)'}
    - **Proceeds: Rs. {proceeds:.3f}**
    
    **Summary:**
    - Total Fees Paid: Rs. {total_fees:.3f}
    - Net Gain/Loss: Rs. {gain_loss:.3f}
    - Return on Investment: {gain_loss_percentage:.2f}%
    """)