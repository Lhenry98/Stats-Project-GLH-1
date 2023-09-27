import time
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime as dt

st.set_page_config(page_title= "Profit/Loss Report", layout= "wide")

#uploaded_file = st.file_uploader("Current file",type="xlsx")
#df = pd.read_excel(io = uploaded_file)
df = pd.read_csv("WonderBus Festival.csv")

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

df_selection = df.query("Customer == @customer & Venue == @venue & Event == @event")
df_selection["Sale Date"] = df_selection["Sale Date"].str[:-5]
df_selection["Sale Date"] = df_selection["Sale Date"] + "00:00"
quant_sold_by_date = df_selection.groupby(by = ["Sale Date"]).sum()[["Sold Qty"]].sort_values(by = "Sold Qty")

# ---- MAIN PAGE ----
st.dataframe(df_selection,
             column_config = {
                 "Profit Loss": None,
                 "ROI(%)": None,
                 "Margin": None,
                 "Shipping Cost": None,
                 "Tax": None})

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# top kpi's
tot_sales = round(df_selection["Total Sell Price"].sum(), 2)
average_roi = round(df_selection["ROI(%)"].mean(), 2)
tot_quant_sold = df_selection["Sold Qty"].sum()

#first two columns
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {tot_sales:,}")
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

