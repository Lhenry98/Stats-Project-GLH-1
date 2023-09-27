import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title= "Profit/Loss Report", layout= "wide")

#convert first columns to strings
df = pd.read_csv('WonderBus Festival.csv', dtype={'Invoice #':str, 'Ex. Order No':str})

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


# ---- MAIN PAGE ----
df_selection = df.query("Customer == @customer & Venue == @venue & Event == @event")

#download button
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_selection)

st.title("WonderBus Festival")

st.markdown("---")

#download button
st.download_button(
    label="Download",
    data=csv,
    file_name="Profit_Loss.csv",
    mime="text/csv"
)

#dataframe
st.dataframe(df_selection,
             column_config = {
                 "Purchase Price/tix": st.column_config.NumberColumn(format="$%d"), 
                 "Sell Price/tix": st.column_config.NumberColumn(format="$%d"), 
                 "Total Purchase Price": st.column_config.NumberColumn(format="$%d"), 
                 "Total Sell Price": st.column_config.NumberColumn(format="$%d"), 
                 "Profit Loss": None,
                 "ROI(%)": None,
                 "Margin": None,
                 "Shipping Cost": None,
                 "Tax": None
             }, 
            hide_index = True)

st.markdown("---")

st.title(":bar_chart: Sales Dashboard")

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

df_selection["Sale Date"] = df_selection["Sale Date"].str[:-5]
df_selection["Sale Date"] = df_selection["Sale Date"] + "00:00"
quant_sold_by_date = df_selection.groupby(by = ["Sale Date"]).sum()[["Sold Qty"]].sort_values(by = "Sold Qty")

#bar chart
fig_ticket_sales = px.bar(quant_sold_by_date,
                          x = quant_sold_by_date.index,
                          y = "Sold Qty",  
                          orientation = "v",
                          title = "<b>Quantity Sold by Date (Hourly)<b>",
                          color_discrete_sequence=['#ec7c34'] * len(quant_sold_by_date),
                          template = "plotly_white")

st.plotly_chart(fig_ticket_sales)

st.markdown("---")

