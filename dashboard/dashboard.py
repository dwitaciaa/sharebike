import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

sns.set(style="dark")

df = pd.read_csv("https://raw.githubusercontent.com/dwitaciaa/sharebike/main/dashboard/bike_hour.csv")
df.head()

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby('mnth').agg({
        'cnt': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)

    return monthly_rent_df

def create_seasonly_rent_df(df):
    seasonly_rent_df = df.groupby("season")[['registered', 'casual', 'cnt']].sum().reset_index()

    return seasonly_rent_df

def create_hourly_rent_df(df):
    hourly_rent_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_rent_df = hourly_rent_df.reset_index()

    return hourly_rent_df

# Filter data
min_date = pd.to_datetime(df["dteday"]).dt.date.min()
max_date = pd.to_datetime(df["dteday"]).dt.date.max()

with st.sidebar:
    # Menambahkan logo
    st.image("https://raw.githubusercontent.com/dwitaciaa/sharebike/main/dashboard/Bike%20Rent.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) &
                (df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
seasonly_rent_df = create_seasonly_rent_df(main_df)
hourly_rent_df = create_hourly_rent_df(main_df)

# Seasonly Rental
st.header('Bike Rental Dashboard :bike: :sparkles:')
st.subheader('Seasonly Rent')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x='season',
    y='registered',
    data=seasonly_rent_df,
    label='Registered',
    color='#DC143C',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=seasonly_rent_df,
    label='Casual',
    color='#20B2AA',
    ax=ax
)

ax.set_xlabel('season')
ax.set_ylabel('count of rental')
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#Hourly Rental
st.subheader('Hourly Rent')
fig = px.line(hourly_rent_df,
              x='hr',
              y=['casual', 'registered'],
              color_discrete_sequence=["yellow", "green"],
              title='').update_layout(xaxis_title='Hour', yaxis_title='count of rental' )

st.plotly_chart(fig, use_container_width=True)



