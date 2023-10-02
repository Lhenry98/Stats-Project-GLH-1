import pandas as pd
import streamlit as st
import plotly.express as px

if st.session_state.key not in {1, 3}:
    st.warning("You must log-in to see the content of this sensitive page! Head over to the log-in page.")
    st.stop()  # App won't run anything after this line

event_name = "Zilker Park"

st.set_page_config(page_title= "Profit/Loss Report", layout= "wide")

#convert first columns to strings
df = pd.read_csv(event_name + '.csv')
df = df.drop(["Invoice #", "Ex. Order No", "Purchase Price/tix", "Total Purchase Price", "Profit Loss" ,"ROI(%)" ,"Margin" ,"Shipping Cost" ,"Tax"], axis = 1)

# ---- SIDEBAR ----
#customer
st.sidebar.header("Please Filter Here:")
customer = st.sidebar.multiselect(
    label = "Select the Customers:",
    options = ["All"] + df["Customer"].unique().tolist(),
    default = "All")
if "All" in customer:
    customer = df["Customer"].unique().tolist()

#venue
venue = st.sidebar.multiselect(
    label = "Select the Venues:",
    options = ["All"] + df["Venue"].unique().tolist(),
    default = "All")
if "All" in venue:
    venue = df["Venue"].unique().tolist()
    
#ticket type
event = st.sidebar.multiselect(
    label = "Select the Ticket Names:",
    options = ["All"] + df["Event"].unique().tolist(),
    default = "All")
if "All" in event:
    event = df["Event"].unique().tolist()


# ---- MAIN PAGE ----
df_selection = df.query("Customer == @customer & Venue == @venue & Event == @event")

st.title(event_name)

st.markdown("---")

#download button
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_selection)

st.download_button(
    label="Download",
    data=csv,
    file_name="Profit_Loss.csv",
    mime="text/csv"
)

#dataframe
st.dataframe(df_selection,
             column_config = {
                 "Sell Price/tix": st.column_config.NumberColumn(format="$%d"), 
                 "Total Sell Price": st.column_config.NumberColumn(format="$%d")
             }, 
            hide_index = True)

st.markdown("---")

st.title(":bar_chart: Sales Dashboard")

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

st.markdown("##")

#df_selection["Sale Date"] = df_selection["Sale Date"].str[:-5]
#df_selection["Sale Date"] = df_selection["Sale Date"] + "00:00"
df_selection["Sale Date"] = df_selection["Sale Date"].str[:-8]
quant_sold_by_date = df_selection.groupby(by = ["Sale Date"]).sum()[["Sold Qty"]].sort_values(by = "Sold Qty")

#bar chart
fig_ticket_sales = px.bar(quant_sold_by_date,
                          quant_sold_by_date.index, 
                          y = "Sold Qty",  
                          orientation = "v",
                          title = "<b>Quantity Sold by Date<b>",
                          color_discrete_sequence=['#ec7c34'],
                          template = "plotly_white"
                         )

st.plotly_chart(fig_ticket_sales)

st.markdown("---")
