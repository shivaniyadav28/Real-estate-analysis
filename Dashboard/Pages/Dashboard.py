# Terminal -> cd Dashboard -> Enter
# streamlit run Home.py -> Enter

import streamlit as st
import pandas as pd
import plotly.express as px


# Load the dataset

df = pd.read_csv(r'C:\Users\hp\OneDrive\Desktop\House_Sales_DataAnalysis\Analyzing Real Estate Prices\HouseSalesCleaned.csv')

# header

st.markdown(
    """
    <style>
    .custom-heading {
        color: #FFFFFF; /* White text */
        font-weight: bolder;
        background-color: #2C3E50; /* Dark Blue background */
        border: 2px solid #1ABC9C; /* Turquoise border */
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        font-size: 26px;
        width: 100%; /* Makes the header wider */
        box-sizing: border-box; /* Ensures padding and border are included in the width */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Applying the custom heading

st.markdown("<h1 class='custom-heading'>Analyzing Housing Price Dataset</h1>", unsafe_allow_html=True)

# Display the dataset

#df

# for filter title

st.sidebar.image("Assets\logo new.png",width = 200)
st.sidebar.header("Filter Options")

# Price filter

min_price, max_price = st.sidebar.slider("Price",
                                     min_value = int(df['price'].min()),
                                     max_value = int(df['price'].max()),
                                     value = (int(df['price'].min()), int(df['price'].max())))

# sqft_living filter

min_sqft_living, max_sqft_living = st.sidebar.slider("Sqft_living",
                                     min_value = int(df['sqft_living'].min()),
                                     max_value = int(df['sqft_living'].max()),
                                     value = (int(df['sqft_living'].min()), int(df['sqft_living'].max())))

# Floor filter

floors = st.sidebar.multiselect('Floors',
                                   options = df['floors'].unique(),
                                   default = df['floors'].unique())
if not floors:
    floors = df['floors'].unique() # Default to all options

# Condition filter

waterfront = st.sidebar.multiselect('Waterfront',
                                   options = df['waterfront'].unique(),
                                   default = df['waterfront'].unique())
if not waterfront:
    waterfront = df['waterfront'].unique() # Default to all options

#filter the data based on the user selection

filtered_df = df[
    (df['price'] >= min_price)& 
    (df['price'] <= max_price)&
    (df['sqft_living'] >= min_sqft_living)&
    (df['sqft_living'] <= max_sqft_living)&
    (df['floors'].isin(floors))&
    (df['waterfront'].isin(waterfront))
]
st.dataframe(filtered_df)

# Create a scatter chart for Relationship between Sqft Lot and Bedrooms.

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Relationship between Sqft Lot and Bedrooms</h1>",unsafe_allow_html=True)

rooms_lot = filtered_df.groupby('bedrooms') ['sqft_lot'].count().reset_index()

fig = px.scatter(rooms_lot , x = 'sqft_lot', y = 'bedrooms', title = 'Relationship between Sqft Lot and Bedrooms',color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>High Bedrooms, Small Lots:</b> Properties with up to 35 bedrooms often have small lot sizes (near 0 sqft).</li> 
        <li><b>Data Clustering:</b> Most properties cluster between 0-2,000 sqft with 0-10 bedrooms.</li> 
        <li><b>Few Large Lots:</b> Properties above 4,000 sqft are rare, usually having 0-5 bedrooms.</li> 
        <li><b>Outliers:</b> A few extreme cases, like 35 bedrooms on very small lots, may indicate data issues.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Create a bar chart for Price Trends to Number of Bedrooms

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Price Trends to Number of Bedrooms</h1>", unsafe_allow_html=True)

# Calculate the average price per number of bedrooms

bedroom_price = filtered_df.groupby('bedrooms')['price'].mean().reset_index()

fig = px.bar(bedroom_price, x='bedrooms', y='price', title='Price Trends to Number of Bedrooms', 
             labels={'bedrooms': 'Number of Bedrooms', 'price': 'Average Price (Millions)'}, 
             color='bedrooms', color_continuous_scale=px.colors.sequential.Viridis)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Price Increase:</b> Prices rise from 0.4M (0 bedrooms) to 1M (7 bedrooms).</li> 
        <li><b>Price Drop:</b> Prices fall to 0.6M for 10 bedrooms.</li> 
        <li><b>Stabilization:</b> After 10 bedrooms, prices stabilize and gradually rise.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Create a histogram for price distribution

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Price Distribution</h1>", unsafe_allow_html=True)

# Create a histogram for price distribution

fig = px.histogram(filtered_df, x='price', nbins=50, title='Price Distribution', 
                   labels={'price': 'Property Prices (Millions)'}, 
                   color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Price Concentration:</b> Most properties are priced between 0-1M.</li> 
        <li><b>Fewer Expensive Properties:</b> Property count decreases as prices rise.</li> 
        <li><b>Outliers:</b> A few luxury properties are priced up to 8M.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Creating the line chart for Date vs Price

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Date vs Price</h1>", unsafe_allow_html=True)

filtered_df['date'] = pd.to_datetime(filtered_df['date'])
date_price = filtered_df.groupby('date')['price'].mean().reset_index()

fig = px.line(date_price, x='date', y='price', title='Date vs Price', labels={'date': 'Date', 'price': 'Average Price (Millions)'}, color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Trends:</b> Property prices show noticeable trends from 2014-05-02 to 2015-05-15.</li> 
        <li><b>Fluctuations:</b> Prices fluctuate significantly, reflecting varying market activity.</li> 
        <li><b>Peaks and Troughs:</b> Prices peak and drop at different points, indicating seasonal trends.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Create a bar chart for Price Trends to Number of Floors

st.markdown("<h1 style='font-size:40px; text-align: center'>Price Trends to Number of Floors</h1>", unsafe_allow_html=True)

# Calculate the average price per number of floors

floors_price = filtered_df.groupby('floors')['price'].mean().reset_index()

fig = px.bar(floors_price, x='floors', y='price', title='Price Trends to Number of Floors', 
             labels={'floors': 'Number of Floors', 'price': 'Average Price (Millions)'}, 
             color='floors', color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Initial Price:</b> Properties with 1 floor average around 0.6M.</li> 
        <li><b>Peak Price:</b> 2-floor properties peak at 1M.</li> 
        <li><b>Price Drop:</b> 3-floor properties average around 0.5M.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Waterfront and View.

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Waterfront and View</h1>", unsafe_allow_html=True)

# Creating the heatmap.

waterfront_view = pd.crosstab(filtered_df['waterfront'], filtered_df['view'])
fig = px.imshow(waterfront_view, labels = dict(x = 'View', y = 'Waterfront', color = 'Count'),
          x = waterfront_view.columns,
          y = waterfront_view.index,
          color_continuous_scale = 'viridis')
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>High Count:</b> Non-waterfront properties (0) with low view ratings (0) are most common.</li> 
        <li><b>Low Count:</b> Waterfront properties (1) are fewer across all view ratings.</li> 
        <li><b>Correlation:</b> Waterfront properties tend to have higher view ratings.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)

#Cross-tabulation between Grade and Condition.

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Cross-tabulation between Grade and Condition</h1>", unsafe_allow_html=True)

# Creating the heatmap

grade_condition = pd.crosstab(filtered_df['grade'], filtered_df['condition'])
fig = px.imshow(grade_condition,
          labels = dict(x = 'Grade', y = 'Condition', color = 'count'),
          x = grade_condition.columns,
          y = grade_condition.index,
          color_continuous_scale= 'viridis',
          title = 'Cross-tabulation between Grade and Condition')        
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Data Concentration:</b> Most properties are around grade 3 and condition 7.</li> 
        <li><b>High Counts:</b> Grade 3 and condition 7 show the highest property counts (up to 4,000+).</li> 
        <li><b>Correlation:</b> Higher grades (3-4) link to better conditions (6-8).</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# House Price by Zipcode

st.markdown("<h1 style='font-size:40px; text-align: center'>House Price by Zipcode</h1>", unsafe_allow_html= True)

# Calculating median price by zipcode

zipcode_price = filtered_df.groupby('zipcode')['price'].median().reset_index()

# Creating the bar chart

fig = px.bar(zipcode_price, x='zipcode', y='price', title='House Price by Zipcode',
             labels={'zipcode': 'Zipcode', 'price': 'Median Price (Millions)'},
             color='zipcode', color_continuous_scale=px.colors.sequential.Viridis)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Price Range:</b> Median house prices range from below $500K to $1.5M across zip codes.</li> 
        <li><b>High-Price Areas:</b> Some zip codes exceed $1M due to location desirability.</li> 
        <li><b>Clusters & Outliers:</b> Similar-priced clusters exist, with a few outliers showing much higher values.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# House Price by year Built.

st.markdown("<h1 style='font-size:40px; text-align: center'>House Price by Year Built</h1>", unsafe_allow_html=True)

# Calculating median price by year built

yr_built_price = filtered_df.groupby('yr_built')['price'].median().reset_index()

# Creating the scatter chart with a regression line

fig = px.scatter(yr_built_price, x='yr_built', y='price', trendline='ols', 
                 title='House Price by Year Built',
                 labels={'yr_built': 'Year Built', 'price': 'Median Price (Millions)'}, 
                 color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Historical Trends:</b> House prices vary by year built, reflecting changing market conditions.</li> 
        <li><b>Price Variability:</b> Prices fluctuate due to factors like construction quality and demand.</li> 
        <li><b>Overall Trend:</b> The regression line shows whether prices increased or decreased over time.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Relationship between Sqft Living and Price

st.markdown("<h1 style='font-size:40px; text-align: center'>Relationship between Sqft Living and Price</h1>",unsafe_allow_html=True)

# Creating the scatter plot with a trend line

fig = px.scatter(filtered_df, x='sqft_living', y='price', trendline='ols', title='Relationship between Sqft Living and Price',
                 labels={'sqft_living': 'Square Footage of Living Space', 'price': 'Price (Millions)'}, color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Positive Correlation:</b> Larger homes tend to have higher prices.</li> 
        <li><b>Clustered Data:</b> Most homes are between 0-6,000 sqft and priced up to $2M.</li> 
        <li><b>Outliers:</b> Some larger homes (up to 14,000 sqft) are priced much higher.</li>
    </ul> 
    """, 
    unsafe_allow_html=True
)


# Relationship between Sqft Lot and Price.

st.markdown("<h1 style='font-size:40px; text-align: center'>Relationship between Sqft Lot and Price</h1>",unsafe_allow_html=True)

# Creating the scatter plot with a trend line

fig = px.scatter(filtered_df, x='sqft_lot', y='price', trendline='ols', title='Relationship between Sqft Lot and Price',
                 labels={'sqft_lot': 'Square Footage of Lot', 'price': 'Price (Millions)'}, color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>General Trend:</b> Larger lot sizes are usually linked to higher prices, but the trend isn’t strictly linear.</li>
        <li><b>Clustered Data:</b> Most properties are in the lower range (below 500,000 sqft and $2M).</li> 
        <li><b>Outliers & Variation:</b> Some properties with smaller lots have high prices, suggesting other factors like location or zoning play a role.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)


# Relationship between Floors and Price.

st.markdown("<h1 style='font-size:40px; text-align: center'>Relationship between Floors and Price</h1>",unsafe_allow_html=True)

# Calculating median and standard deviation of price by floors

floors_price = filtered_df.groupby('floors')['price'].agg(['median', 'std']).reset_index()

# Creating the bar chart with error bars

fig = px.bar(floors_price, x='floors', y='median', error_y='std', title='Relationship between Floors and Price',
             labels={'floors': 'Number of Floors', 'median': 'Median Price (Thousands)', 'std': 'Standard Deviation'},
             color='floors', color_continuous_scale=px.colors.sequential.Inferno)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p> 
    <ul style='font-size:18px;'>
        <li><b>Price Increase Up to 2.5 Floors:</b> Price increases with floors until it peaks at 2.5 floors (~$700k).</li>
        <li><b>Price Drop After 2.5 Floors:</b> After 2.5 floors, price decreases or stabilizes (~$400k for 3 floors).</li> 
        <li><b>Threshold Insight:</b> Adding more floors beyond 2.5 may not increase property value.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)

# Relationship between View and Price.

st.markdown("<h1 style='font-size:40px; text-align: center'>Relationship between View and Price</h1>",unsafe_allow_html=True)

# Calculating median view and price

view_price = filtered_df.groupby('view')['price'].median().reset_index()

# Creating the box plot

fig = px.box(filtered_df, x='view', y='price', title='Relationship between View and Price',
             labels={'view': 'View Quality', 'price': 'Price (Millions)'},
             color='view', color_discrete_sequence=px.colors.sequential.Teal)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p>
    <ul style='font-size:18px;'>
        <li><b>Poor View (0-1):</b> Homes with lower view quality have lower and wider price ranges.</li>
        <li><b>Average View (2-3):</b> Improved views lead to higher prices with less price variation.</li>
        <li><b>Excellent View (4):</b> Homes with the best views have significantly higher prices, though with some price variability.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)

# Relationship between Condition and Price.

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Relationship between Condition and Price</h1>", unsafe_allow_html=True)

# Calculating median condition and price.

condition_price = filtered_df.groupby('condition')['price'].median().reset_index()

fig = px.bar(condition_price, x='condition', y='price', title='Relationship between Condition and Price', 
             labels={'condition': 'Property Condition', 'price': 'Median Price (Thousands)'}, 
             color='condition', color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p>
    <ul style='font-size:18px;'>
        <li><b>Condition 1 & 2:</b> Properties in poor condition (1 & 2) have an average price of around 200k.</li>
        <li><b>Condition 3 & 4:</b> Properties in average condition (3 & 4) show a price increase, averaging around 350k to 400k.</li>
        <li><b>Condition 5:</b> Properties in the best condition (5) have the highest average price, around 450k.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)


# Relationship between Grade and Price.

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Relationship between Grade and Price</h1>", unsafe_allow_html=True)

# Calculating median Grade and price.

grade_price = filtered_df.groupby('grade')['price'].median().reset_index()

fig = px.bar(grade_price, x='grade', y='price', title='Relationship between Grade and Price', 
             labels={'grade': 'Grade', 'price': 'Median Price (Millions)'}, 
             color='grade', color_discrete_sequence=px.colors.sequential.Teal)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p>
    <ul style='font-size:18px;'>
        <li><b>Low-Grade Homes (1-4):</b> Prices are below 0.5M.</li>
        <li><b>Mid-Grade Homes (5-8):</b> Prices range from 0.5M to 1M.</li>
        <li><b>High-Grade Homes (9-12):</b> Prices range from 1M to 2.5M.</li>
        <li><b>Top-Grade Homes (13):</b> Price reaches up to 3M.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)

# Relationship between Waterfront and Price.

st.markdown("<h1 style = 'font-size:40px; text-align: center'>Relationship between Waterfront and Price</h1>",unsafe_allow_html=True)

# Creating the violin plot with a color palette

fig = px.violin(filtered_df, x='waterfront', y='price', title='Relationship between Waterfront and Price', 
                labels={'waterfront': 'Waterfront Status', 'price': 'Price (Millions)'}, 
                color='waterfront', color_discrete_sequence=px.colors.sequential.Inferno)
st.plotly_chart(fig)

st.markdown(
    """
    <p style='font-size:25px;'><b>Summary</b></p>
    <ul style='font-size:18px;'>
        <li><b>Non-Waterfront Properties:</b> Prices around 0.4M.</li>
        <li><b>Waterfront Properties:</b> Prices around 1.2M with a wider range.</li>
        <li><b>Price Premium:</b> Waterfront properties are significantly more expensive.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)

# header

st.markdown(
    """
    <style>
    .custom-heading {
        color: #FFFFFF; /* White text */
        font-weight: bolder;
        background-color: #2C3E50; /* Dark Blue background */
        border: 2px solid #1ABC9C; /* Turquoise border */
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        font-size: 26px;
        width: 100%; /* Makes the header wider */
        box-sizing: border-box; /* Ensures padding and border are included in the width */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Applying the custom heading

st.markdown("<h1 class='custom-heading'>Overall Summary and Key Takeaways</h1>", unsafe_allow_html=True)

#summary

st.markdown("""
<p style='font-size:20px;'><b>Summary</b></p>
<ul style='font-size:18px;'>
    <li><b>Price Distribution:</b> Location and property size are key drivers, with higher values near water.</li>
    <li><b>High-Value Properties:</b> Larger size, more rooms, renovations, and high grades increase prices.</li>
    <li><b>Neighborhood & Location:</b> Larger properties and desirable locations (latitude/longitude) correlate with higher prices.</li>
    <li><b>Recommendations:</b> Invest in properties near water, renovate mid-range properties for value increase, and focus on desirable features like size and views.</li>
</ul>
""", unsafe_allow_html=True)


