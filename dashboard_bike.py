import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

st.title('Dashboard Bike Sharing Dataset')

# Load the CSV file
df = pd.read_csv('https://raw.githubusercontent.com/glendod/p/main/project/hour.csv')

# Convert to datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# User can choose date range using widget
st.sidebar.header('Filter Data by Date')
start_date = st.sidebar.date_input('Start Date', df['dteday'].min())
end_date = st.sidebar.date_input('End Date', df['dteday'].max())

# Convert the user-selected date to datetime64[ns] format
start_date = pd.to_datetime(start_date).tz_localize(None)
end_date = pd.to_datetime(end_date).tz_localize(None)

# Apply the filter
filtered_df = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

filtered_df['season'] = filtered_df['season'].replace({1:"musim dingin", 2:"musim semi", 3:"musim panas", 4:"musim gugur"})

filtered_df['weathersit'] = filtered_df['weathersit'].replace({1:"cerah", 2:"berkabut", 3:"hujan/salju ringan", 4:"cuaca ekstrem"})

data_by_season_weather = filtered_df.groupby(['season', 'weathersit'])['cnt'].sum().reset_index()

weather_order = ['cerah', 'berkabut', 'hujan/salju ringan', 'cuaca ekstrem']

palette = sns.color_palette("viridis", len(data_by_season_weather['weathersit'].unique()))

# Plotting
plt.figure(figsize=(12, 8))
sns.barplot(x='season', y='cnt', hue='weathersit', data=data_by_season_weather, palette=palette, hue_order=weather_order)
plt.title('Jumlah Orang yang Menyewa Sepeda berdasarkan Musim dan Cuaca', fontsize=16)
plt.xlabel('Musim', fontsize=14)
plt.ylabel('Jumlah Orang Menyewa Sepeda', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Cuaca', title_fontsize='14', fontsize='12', loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
sns.despine(trim=True, left=True)

# Add data labels on each bar
for p in plt.gca().patches:
    if not pd.isna(p.get_height()):
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10)

st.pyplot(plt)

# Data by hour
data_by_hour = filtered_df.groupby(['hr'])['cnt'].sum().reset_index()

plt.figure(figsize=(12, 8))
sns.barplot(x='cnt', y='hr', data=data_by_hour, orient='h', palette="viridis")
plt.title('Jumlah Orang yang menyewa sepeda berdasarkan jam', fontsize=16)
plt.xlabel('jumlah', fontsize=14)
plt.ylabel('jam', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
sns.despine(trim=True, left=True)

# Adding data labels on each bar
for p in plt.gca().patches:
    plt.gca().annotate(f'{int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height() / 2),
                        ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=10)

st.pyplot(plt)

# Group by month and sum the counts
data_by_month = filtered_df.groupby(filtered_df['dteday'].dt.to_period("M")).agg({'cnt': 'sum'}).reset_index()
data_by_month['month'] = data_by_month['dteday'].dt.strftime('%B') # Format to month name

# Set Seaborn style
sns.set(style="whitegrid")

# Define a color palette with distinct colors for each year
palette = sns.color_palette("viridis", n_colors=len(data_by_month['dteday'].dt.year.unique()))

# Plotting for each year
plt.figure(figsize=(15, 8))
for i, year in enumerate(data_by_month['dteday'].dt.year.unique()):
    data_by_year = data_by_month[data_by_month['dteday'].dt.year == year]
    sns.lineplot(x='month', y='cnt', data=data_by_year, marker='o', label=f'Jumlah Orang - {year}', color=palette[i])

plt.title('Jumlah Orang yang Menyewa Sepeda per Bulan', fontsize=16)
plt.xlabel('Bulan', fontsize=14)
plt.ylabel('Jumlah Orang', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
sns.despine(trim=True, left=True)

st.pyplot(plt)
