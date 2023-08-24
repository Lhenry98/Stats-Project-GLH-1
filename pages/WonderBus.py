import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

st.set_page_config(page_title= "Profit/Loss Report", layout= "wide")

df = pd.read_excel(io = "WonderBus Festival.xlsx")

# ---- SIDEBAR ----
#event
st.sidebar.header("Please Filter Here:")
customer = st.sidebar.multiselect(
    label = "Select the Customer:",
    options = ["All"] + df["Customer"].unique().tolist(),
    default = "All")

if "All" in customer:
    customer = df["Customer"].unique().tolist()

#venue
venue = st.sidebar.multiselect(
    label = "Select the Venue:",
    options = ["All"] + df["Venue"].unique().tolist(),
    default = "All")

if "All" in venue:
    venue = df["Venue"].unique().tolist()
    
event = st.sidebar.multiselect(
    label = "Select the Event Date:",
    options = ["All"] + df["Event"].unique().tolist(),
    default = "All")

if "All" in event:
    event = df["Event"].unique().tolist()
'''
start_date = datetime(2020, 1, 1)
end_date = start_date + timedelta(weeks = 1)

sell_date = st.sidebar.slider(
    label = "Select Ticket Sale Date",
    min_value = start_date, 
    max_value = end_date,
    value = (start_date, end_date),
    step = timedelta(days = 1))
'''
df_selection = df.query("Customer == @customer & Venue == @venue & Event == @event")


st.dataframe(df_selection)


# ---- MAIN PAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# top kpi's
net_sales = round(df_selection["Profit Loss"].sum(), 2)
average_roi = round(df_selection["ROI(%)"].mean(), 2)
tot_quant_sold = df_selection["Sold Qty"].sum()
quant_sold_by_date = df_selection.groupby(by = ["Sale Date"]).sum()[["Sold Qty"]].sort_values(by = "Sold Qty")

#first two columns
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Net Sales:")
    st.subheader(f"US $ {net_sales:,}")
with right_column:
    st.subheader("Quantity Sold:")
    st.subheader(f"{tot_quant_sold:,}")

st.markdown("##")

#bar chart
fig_ticket_sales = px.bar(quant_sold_by_date, 
                          x = quant_sold_by_date.index, 
                          y = "Sold Qty", 
                          orientation = "v",
                          title = "<b>Quantity Sold by Date<b>",
                          color_discrete_sequence=['#ec7c34'] * len(quant_sold_by_date),
                          template = "plotly_white")

st.plotly_chart(fig_ticket_sales)

st.markdown("---")