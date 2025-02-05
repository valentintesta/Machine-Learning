import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns 
import altair as alt
from matplotlib import pyplot as plt    
#pip install streamlit-extras
from streamlit_extras.dataframe_explorer import dataframe_explorer

from streamlit_extras.metric_cards import style_metric_cards 
# config the page width 

st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")

#title
st.markdown(
    "<h1 style='color: red;'>Business Intelligent Analytics</h1>", 
    unsafe_allow_html=True
)


# subtitle
st.markdown(
        """
    <h3 style="margin-bottom: 5px;">Raw Dataset</h3>
    <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
    """,
    unsafe_allow_html=True
    )

#load dataset
df=pd.read_csv('data.csv')


st.dataframe(df,use_container_width=True)




# sidebar date picker 

with st.sidebar:
 st.title("Select Date Range")
 start_date=st.date_input(label="Start Date")
 
with st.sidebar:
 end_date=st.date_input(label="End Date")

# massage for select range date 

if start_date and end_date:
    st.error(f"You have selected the date range: {start_date} to {end_date}")


# filter date range 

df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

with st.expander("Filter Data CSV"):
    filter_df =dataframe_explorer(df2,case=False)
    st.dataframe(filter_df, use_container_width=True)

     
a1,a2=st.columns(2)
    
# Visualization 1: Product Quantities
with a1:
    st.markdown(
        """
    <h3 style="margin-bottom: 5px;">Products & Quantities</h3>
    <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
    """,
    unsafe_allow_html=True
    )
    source = pd.DataFrame({
        "Quantity ($)": df2["Quantity"],
        "Product": df2["Product"]
      })
    bar_chart = alt.Chart(source).mark_bar().encode(
        x="sum(Quantity ($)):Q",
        y=alt.Y("Product:N", sort="-x")
    )
    st.altair_chart(bar_chart, use_container_width=True)
    
# Metric Cards
with a2:
    st.markdown(
        """
        <h3 style="margin-bottom: 5px;">Dataset Metrics</h3>
        <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    col1.metric(label="All Inventory Products", value=df2["Product"].count(), delta="Number of Items in stock")
    col2.metric(label="Sum of Product Price (USD):", value=f"{df2['TotalPrice'].sum():,.0f}", delta=f"{df2['TotalPrice'].median():,.0f}")

    col11, col22, col33 = st.columns(3)
    col11.metric(label="Maximum Price (USD):", value=f"{df2['TotalPrice'].max():,.0f}", delta="High Price")
    col22.metric(label="Minimum Price (USD):", value=f"{df2['TotalPrice'].min():,.0f}", delta="Low Price")
    col33.metric(label="Total Price Range (USD):", value=f"{df2['TotalPrice'].max() - df2['TotalPrice'].min():,.0f}", delta="Annual Salary Range")

    # Style the metric cards
    style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd", box_shadow="#F71938")


b1,b2=st.columns(2)


fixed_corner_radius = 10  # Set your desired fixed value for corner radius

# Display chart with Products and Total Price
with b1:
    st.markdown(
        """
        <h3 style="margin-bottom: 5px;">Products & Total Price</h3>
        <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
        """,
        unsafe_allow_html=True
    )

    # Ensure df2 has the required columns
    if "Product" in df2.columns and "TotalPrice" in df2.columns and "Category" in df2.columns:
        source = df2
        
        # Create the bar chart with a fixed corner radius
        bar_chart = alt.Chart(source).mark_bar(cornerRadius=fixed_corner_radius).encode(
            x=alt.X('Product:N', axis=alt.Axis(labelAngle=0)),
            y='sum(TotalPrice):Q',  # Use sum of TotalPrice if needed (if there are multiple entries per product)
            color='Category:N'  # Color bars based on Category
        ).interactive()  # Add interactivity for zooming and panning
        
        # Display the chart in Streamlit
        st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)
    else:
        st.error("⚠️ Missing 'Product', 'TotalPrice', or 'Category' column in dataset.")
        
        
with b2: 
    st.markdown(
        """
        <h3 style="margin-bottom: 5px;">Products & Unit Price</h3>
        <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
        """,
        unsafe_allow_html=True
    )
    energy_source = pd.DataFrame({
    "Product": df2["Product"],
    "UnitPrice ($)":  df2["UnitPrice"],
    "Date": df2["OrderDate"]
    })

     # Create an interactive selection
    highlight = alt.selection_single(
        on="mouseover", fields=["Product"], nearest=True
    )

    # Base Chart
    base = alt.Chart(energy_source).encode(
        x=alt.X("month(Date):O", title="Month"),
        y=alt.Y("sum(UnitPrice ($)):Q", title="Total Unit Price ($)"),
        color="Product:N"
    )

    # Bar chart with dynamic highlighting
    bars = base.mark_bar().encode(
        size=alt.condition(highlight, alt.value(20), alt.value(10))  # Bar width changes on hover
    ).add_selection(highlight)  # Enable interaction

    # Display in Streamlit
    st.altair_chart(bars, use_container_width=True, theme="streamlit")
    
    
 
 #select only numeric or number data
 
 
p1, p2 = st.columns(2)

with p1:
    st.markdown(
        """
        <h3 style="margin-bottom: 5px;">Features by Frequency</h3>
        <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
        """,
        unsafe_allow_html=True
    )

    # Dropdowns for feature selection
    feature_x = st.selectbox('Select feature for X (Qualitative)', df2.select_dtypes("object").columns)
    feature_y = st.selectbox('Select feature for Y (Quantitative)', df2.select_dtypes("number").columns)

    # Scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2["Product"], ax=ax)  # Fixed `df.Product` -> `df2["Product"]`
    st.pyplot(fig)
    
    
    
with p2:
    st.markdown(
        """
        <h3 style="margin-bottom: 5px;">Feature Distribution</h3>
        <hr style="height:3px; border:none; background-color:red; margin-top:5px; margin-bottom:0px;">
        """,
        unsafe_allow_html=True
    )

    # Dropdown to select a feature
    feature = st.selectbox('Select a feature', df2.select_dtypes("object").columns)

    # Plot histogram
    fig, ax = plt.subplots()
    ax.hist(df2[feature], bins=20, color="red", edgecolor="black")  # Improved styling

    # Set the title and labels
    ax.set_title(f'Histogram of {feature}', fontsize=14)
    ax.set_xlabel(feature, fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)

    # Display the plot
    st.pyplot(fig)
