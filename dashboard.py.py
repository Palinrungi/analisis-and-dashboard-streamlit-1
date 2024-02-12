import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False).reset_index().head(5)
    return bycity_df

def create_city_1_customer_df(df):
    city_1_customer_df = df.groupby(by = 'customer_city').customer_id.nunique().sort_values(ascending=True).reset_index()
    city_1_customer_df = city_1_customer_df[city_1_customer_df['customer_id'] == 1].sum()
    return city_1_customer_df

def create_average_per_year_df(df):
    average_per_year_df = df.groupby(df['review_creation_date'].dt.year)['review_score'].mean()
    return average_per_year_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["review_creation_date", "review_answer_timestamp"]
all_df.sort_values(by="review_creation_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


min_date = all_df['review_creation_date'].min()
max_date = all_df['review_creation_date'].max()

with st.sidebar:
     st.title('WINTERFEL SHOP')


     start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
     
main_df = all_df[(all_df['review_creation_date'] >= str(start_date)) & 
                (all_df['review_creation_date'] <= str(end_date))]

bycity_df = create_bycity_df(main_df)
city_1_customer_df = create_city_1_customer_df(main_df)
average_per_year_df = create_average_per_year_df(main_df)

st.header('WINTERFEL SHOP :sparkles:')

st.subheader('City wth the most customers')
colors = ['blue','grey','grey','grey','grey']
bycity_df.rename(columns={
    'customer_id' : 'customer_count'
}, inplace=True)

fig, ax = plt.subplots(figsize=(11, 6))
sns.barplot(
    x='customer_city',
    y='customer_count',
    data=bycity_df.sort_values(by='customer_count', ascending=False),
    hue='customer_city',
    palette=colors
)

plt.title(None)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader('City with the fewest customers')
labels = ['1 Customer', 'More than 1 customer']
sizes = [27.74, 100 - 27.74]

colors = ['blue', 'grey']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90, colors=colors)
ax.set_title(None)
ax.axis('equal')

st.pyplot(fig)

st.markdown('<span style="color:blue; font-size:22px">27.74% </span> dari <span style="color:blue; font-size:22px">4419</span> total kota merupakan kota yang hanya memiliki <span style="color:blue"> 1 customer </span>. Hal ini menunjukkan bahwa terdapat <span style="color:blue">1144 kota dengan 1 customer </span>', unsafe_allow_html=True)

st.subheader('Average per year')
fig, ax = plt.subplots(figsize=(11, 6))
average_per_year = pd.Series ({
    2016: 3.5,
    2017: 4.1,
    2018: 4.0
})

plt.bar(average_per_year.index, average_per_year, color=['blue', 'blue', 'blue'])
plt.xlabel('Tahun')
plt.ylabel('Rata-rata')
plt.title('Rata-rata review score dari Tahun 2016-2018')

# Menampilkan plot menggunakan Streamlit
st.pyplot(plt)

st.markdown('Dengan memeriksa rata-rata per tahun, dapat disimpulkan bahwa skor cenderung <span style="color:blue; font-size:20px">stabil</span> dari tahun ke tahun. Ini menunjukkan konsistensi dalam kualitas layanan atau produk selama periode waktu yang dianalisis.', unsafe_allow_html=True)
