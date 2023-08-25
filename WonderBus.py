import pandas as pd
import streamlit as st
import plotly.express as px

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
    
df_selection = df.query("Customer == @customer & Venue == @venue & Event == @event")


st.dataframe(df_selection)


# ---- MAIN PAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# top kpi's
tot_sales = round(df_selection["Total Sell Price"].sum(), 2)
tot_quant_sold = df_selection["Sold Qty"].sum()

#first two columns
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {tot_sales:,}")
with right_column:
    st.subheader("Quantity Sold:")
    st.subheader(f"{tot_quant_sold:,}")

st.markdown("---")
