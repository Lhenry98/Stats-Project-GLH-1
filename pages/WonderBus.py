import pandas as pd
import streamlit as st
import plotly.express as px
from Hello import uploaded_file

st.set_page_config(page_title= "Profit/Loss Report", layout= "wide")

df = pd.read_excel(io = uploaded_file)

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


st.dataframe(df_selection)


# ---- MAIN PAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# top kpi's
net_sales = round(df_selection["Profit Loss"].sum(), 2)
average_roi = round(df_selection["ROI(%)"].mean(), 2)
tot_quant_sold = df_selection["Sold Qty"].sum()

#first two columns
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Net Sales:")
    st.subheader(f"US $ {net_sales:,}")
with right_column:
    st.subheader("Quantity Sold:")
    st.subheader(f"{tot_quant_sold:,}")

st.markdown("---")

while(True):
    df = pd.read_excel(io = uploaded_file)
    time.sleep(5)

