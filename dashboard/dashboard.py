import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter

st.set_page_config(page_title="Bike Sharing Analysis")

data = pd.read_csv('./data/combined_data_clean.csv')
# For Function
# Q1: Apa dampak hari libur terhadap jumlah penyewaan sepeda?
def comparison_data_holiday_and_nonholiday(data):
    comparison_holiday_user = data.groupby(
        [data['dteday'].dt.year.rename('year'), 
         data['dteday'].dt.month.rename('month'), 
         "holiday"]
    ).agg(cnt_sum=('cnt', 'sum'), cnt_mean=('cnt', 'mean')).reset_index()

    # Convert 'year' and 'month' to string to facilitate plotting
    comparison_holiday_user['year'] = comparison_holiday_user['year'].astype(str)
    comparison_holiday_user['month'] = comparison_holiday_user['month'].astype(str)
    comparison_holiday_user['holiday'] = comparison_holiday_user['holiday'].map({0: 'Non-Holiday', 1: 'Holiday'}).astype('category')
    # Create a new column 'year_month' to combine 'year' and 'month' for clearer x-axis labels
    comparison_holiday_user['year_month'] = comparison_holiday_user['year'] + '-' + comparison_holiday_user['month'].str.zfill(2)
    
    return comparison_holiday_user

# Function to plot average rentals for holidays vs non-holidays
def plot_holiday_comparison(data):
    mean_rentals_by_holiday = data.groupby('holiday')['cnt'].mean().reset_index()
    
    # Plotting within Streamlit
    fig, ax = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    sns.barplot(x='holiday', y='cnt', data=mean_rentals_by_holiday, color=color, ax=ax, alpha=0.6)
    ax.set_title('Perbandingan Rata-Rata Penyewaan Sepeda: Hari Libur vs Bukan Hari Libur')
    ax.set_xlabel('Jenis Hari')
    ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
    ax.set_xticklabels(['Non-Holiday', 'Holiday'])
    st.pyplot(fig)

# Function to plot average bike rentals by year and month for holiday vs non-holiday
def plot_monthly_rentals(data):
    plt.figure(figsize=(15, 8))  # Consider making the figure larger
    sns.barplot(x='year_month', y='cnt_mean', hue='holiday', data=data, palette='coolwarm')
    plt.title('Rata Rata Penyewaan Sepeda Berdasarkan Tahun dan Bulan: Hari Libur vs Bukan Hari Libur')
    plt.xlabel('Year-Month (YYYY-MM)')
    plt.ylabel('Rata-Rata Penyewaan Sepeda')
    plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability
    plt.legend(title='Holiday', loc='upper left', bbox_to_anchor=(1, 1))  # Move the legend outside of the plot
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal gridlines for easier reading
    plt.tight_layout()  # Adjust layout
    st.pyplot(plt.gcf())  # Display the plot in Streamlit
    
    
# Pertanyaan 2: Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda?
def comparison_seasonal_rentals(data):
    seasons_list = {
        1: "Musim Semi",
        2: "Musim Panas",
        3: "Musim Gugur",
        4: "Musim Dingin"
    }

    data = data.copy()

    data['seasons_descriptive'] = data['season'].map(seasons_list)

    comparison_seasons = data.groupby(by=["season","seasons_descriptive"]).agg({
        "cnt": ["sum", "mean"],
    })
    comparison_seasons.columns = ['Total Rentals', 'Average Rentals']
    comparison_seasons.reset_index(inplace=True)
    return comparison_seasons

def plot_seasonal_rentals(data):
    # Plotting Total and Average Rentals by Season
    season_labels = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur']
    unique_seasons = data['season'].unique()
    matched_labels = season_labels[:len(unique_seasons)]
    fig, ax1 = plt.subplots(figsize=(10, 6))

    def millions_formatter(x, pos):
        return f'{int(x)}'

    color = 'tab:red'
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Total Rental', color=color)
    ax1.bar(data['season'], data['Total Rentals'], color=color, alpha=0.6, label='Total Rentals')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    ax2 = ax1.twinx() # This is for plotting average rentals on the same plot
    color = 'tab:blue'
    ax2.set_ylabel('Rata-rata Rental', color=color)  # we already handled the x-label with ax1
    ax2.plot(data['season'], data['Average Rentals'], color=color, marker='o', label='Average Rentals')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Penyewaan Sepeda: Total vs Rata-rata per Musim')
    plt.xticks(unique_seasons, labels=matched_labels)
    st.pyplot(plt.gcf())
    
    
# Pertanyaan 3: Apakah kondisi cuaca mempengaruhi jumlah penyewaan sepeda?
def comparison_weather_conditions(data):
    weather_conditions = {
        1: "Cerah, Sedikit Awan, Sebagian Awan",
        2: "Kabut + Sedikit Awan, Mist Kabut + Sebagian Awan, Mist Kabut + Pecah Awan, Mist Kabut + Awan",
        3: "Salju Ringan, Hujan Ringan + Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar",
        4: "Hujan Lebat + Es Pallet + Badai Petir + Kabut, Salju + Kabut"
    }

    data['weathersit_descriptive'] = data['weathersit'].map(weather_conditions)
    weather_agg_sum = data.groupby('weathersit_descriptive')['cnt'].sum().reset_index()
    weather_agg_mean = data.groupby('weathersit_descriptive')['cnt'].mean().reset_index()

    return weather_agg_mean, weather_agg_sum

def plot_weather_correlation(weather_sum, weather_mean):
    def autopct_format(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}% ({v:d})'.format(p=pct,v=val)
        return my_autopct

    # Plotting the sum counts of bike rentals in a pie chart
    plt.figure(figsize=(20, 8))

    # Plot for sum
    plt.subplot(1, 3, 1)
    patches, texts, autotexts = plt.pie(weather_sum['cnt'],
            autopct=autopct_format(weather_sum['cnt']), startangle=60)
    plt.title('Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    plt.axis('equal')

    # Plot for mean
    plt.subplot(1, 3, 2)
    patches, texts, autotexts = plt.pie(weather_mean['cnt'],
            autopct=autopct_format(weather_mean['cnt']), startangle=200)
    plt.title('Rata Rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    plt.axis('equal')

    # Adjust legend
    plt.legend(patches, weather_sum['weathersit_descriptive'], loc='center left', bbox_to_anchor=(-0.5, 0))

    # Show the plots
    plt.tight_layout()
    st.pyplot(plt.gcf())


# Pertanyaan 4: Bagaimana suhu dan suhu yang dirasakan berkorelasi dengan jumlah penyewaan sepeda?
def comparison_temperature(data):
    correlation_matrix = data[['temp', 'atemp', 'cnt']].corr()

    # Adjust bins to dynamically fit the data range while dividing it into quartiles
    min_temp, max_temp = data['temp'].min(), data['temp'].max()
    bins_temp = np.linspace(min_temp, max_temp, num=5)  # Creates 4 equal segments from min to max

    labels = ['Dingin', 'Sejuk', 'Hangat', 'Panas']
    data['temp_category'] = pd.cut(data['temp'], bins=bins_temp, labels=labels, include_lowest=True)

    comparison_temp_category = data.groupby('temp_category', observed=True).agg({
        "cnt": ["size", "sum", "mean"],
    })

    # Define bins for 'atemp' similar to 'temp'
    min_atemp, max_atemp = data['atemp'].min(), data['atemp'].max()
    bins_atemp = np.linspace(min_atemp, max_atemp, num=5)  # Creates 4 equal segments from min to max
    data['atemp_category'] = pd.cut(data['atemp'], bins=bins_atemp, labels=labels, include_lowest=True)

    # Perform groupby on 'atemp_category'
    comparison_atemp_category = data.groupby('atemp_category', observed=True).agg({
        "cnt": ["size", "sum", "mean"],
    })

    # Flatten the MultiIndex for comparison_temp_category
    comparison_temp_category.columns = ['_'.join(col).strip() for col in comparison_temp_category.columns.values]
    comparison_temp_category.reset_index(inplace=True)

    # Do the same for comparison_atemp_category
    comparison_atemp_category.columns = ['_'.join(col).strip() for col in comparison_atemp_category.columns.values]
    comparison_atemp_category.reset_index(inplace=True)

    return correlation_matrix, comparison_temp_category, comparison_atemp_category

def plot_correlation_temperature(correlation_matrix, comparison_temp_category, comparison_atemp_category):
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Korelasi antara Variabel Suhu, Sensasi Suhu, dan Jumlah Rental')
    st.pyplot(plt.gcf())

    plt.figure(figsize=(20, 8))
    plt.subplot(1, 2, 1)
    sns.barplot(x='temp_category', y='cnt_sum', data=comparison_temp_category, palette='coolwarm')
    plt.title('Total Penyewaan Sepeda berdasarkan Kategori Suhu')
    plt.xlabel('Kategori Suhu')
    plt.ylabel('Total Rentals')

    plt.subplot(1, 2, 2)
    sns.barplot(x='atemp_category', y='cnt_sum', data=comparison_atemp_category, palette='coolwarm')
    plt.title('Total Penyewaan Sepeda berdasarkan Kategori Sensasi Suhu')
    plt.xlabel('Kategori Sensasi Suhu')
    plt.ylabel('Total Rental')
    st.pyplot(plt.gcf())

# Pertanyaan 5 : Bagaimana tren penyewaan sepeda dari tahun ke tahun? Bulan dan tahun manakah yang memiliki permintaan penyewaan sepeda tertinggi/terendah?
def comparison_yearly_trends(data):
    monthly_rentals = data.groupby(by=[data['dteday'].dt.year.rename("Year"), data['dteday'].dt.month.rename("Month")]).agg({
        "cnt": ["sum", "mean"],
    })

    monthly_rentals.columns = ['Total Rentals', 'Average Rentals']
    return monthly_rentals

def plot_yearly_trends(monthly_rentals):
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Assuming 'Total Rentals' is indexed by a MultiIndex of (year, month), we'll first need to reset it for plotting
    monthly_rentals_reset = monthly_rentals.reset_index()  # This converts 'Year' and 'Month' from MultiIndex to columns
    monthly_rentals_reset['Year-Month'] = monthly_rentals_reset['Year'].astype(str) + '-' + monthly_rentals_reset['Month'].astype(str)

    # Bar chart
    ax1.bar(monthly_rentals_reset['Year-Month'], monthly_rentals_reset['Total Rentals'], color='lightblue', label='Total Rentals', width=0.4)

    # Creating ax2 for the line chart using the same x-axis but a different y-axis
    ax2 = ax1.twinx()
    ax2.plot(monthly_rentals_reset['Year-Month'], monthly_rentals_reset['Total Rentals'], color='green', label='Trend', marker='o', linewidth=2)

    # Titles and labels
    ax1.set_xlabel('Year-Month (YYYY-MM)')
    ax1.set_ylabel('Total Rentals', color='blue')
    ax2.set_ylabel('Trend', color='green')
    ax1.set_title('Bike Rentals: Total and Trend Over Time')
    ax1.tick_params(axis='x', rotation=45)

    # Legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)


# Pertanyaan 6: Bagaimana kecepatan angin mempengaruhi penyewaan sepeda?
def comparison_wind_speed(data):
    correlation_wind_count = data[['windspeed', 'cnt']].corr()

    # Define wind speed bins and labels
    bins = [data['windspeed'].min(), 0.1, 0.2, data['windspeed'].max()]
    labels = ['Rendah', 'Sedang', 'Tinggi']
    data['windspeed_category'] = pd.cut(data['windspeed'], bins=bins, labels=labels, include_lowest=True)

    # Aggregate bike rentals by wind speed category
    windspeed_effect = data.groupby('windspeed_category', observed=True)['cnt'].mean().reset_index()
    return correlation_wind_count, windspeed_effect

def plot_wind_speed_effect(correlation_wind_count, windspeed_effect):
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_wind_count, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Korelasi antara Kecepatan Angin dan Jumlah Rental')
    st.pyplot(plt.gcf())

    plt.figure(figsize=(8, 6))
    sns.barplot(x='windspeed_category', y='cnt', data=windspeed_effect, palette='coolwarm')
    plt.title('Rata-Rata Penyewaan Sepeda berdasarkan Kategori Kecepatan Angin')
    plt.xlabel('Kategori Kecepatan Angin')
    plt.ylabel('Rata-Rata Rental')
    st.pyplot(plt.gcf())


# Pertanyaan 7: Siapa yang lebih banyak menggunakan layanan penyewaan sepeda, pengguna biasa atau pengguna terdaftar?
def comparison_registered_vs_casual(data):
    user_comparison_year_month = data.groupby(
        [data['dteday'].dt.year.rename('year'),
        data['dteday'].dt.month.rename('month')]
    ).agg(
        casual_sum=('casual', 'sum'),
        registered_sum=('registered', 'sum'),
    ).reset_index()

    user_comparison_melted = user_comparison_year_month.melt(
        id_vars=['year', 'month'],
        value_vars=['casual_sum', 'registered_sum'],
        var_name='User_Type', 
        value_name='Count'
    )

    return user_comparison_melted

def plot_registered_vs_casual(user_comparison_melted):
    plt.figure(figsize=(15, 7))

    # Create the bar plot
    sns.barplot(x='month', y='Count', hue='User_Type', data=user_comparison_melted)

    # Set the title and labels
    plt.title('Bike Rentals: Casual vs. Registered Users')
    plt.xlabel('Bulan')
    plt.ylabel('Total Pengguna')
    plt.legend(title='User Type')
    st.pyplot(plt.gcf())

# Pertanyaan 8: Pada jam berapa saja penyewaan sepeda memiliki pengguna terbanyak dan tersedikit?
def comparison_hourly_rentals(data):
    average_hourly_user = data.groupby(by=[data['dteday'].dt.hour.rename('hour')]).agg(
        casual_sum=('casual', 'sum'),
        casual_mean=('casual', 'mean'),
        registered_sum=('registered', 'sum'),
        registered_mean=('registered', 'mean'),
        cnt_sum=('cnt', 'sum'),
        cnt_mean=('cnt', 'mean')
    ).reset_index()


    average_hourly_user.columns = [''.join(col).strip() for col in average_hourly_user.columns.values]

    # Reset the index if 'hour' is not already a column
    average_hourly_user.reset_index(inplace=True)
    return average_hourly_user

def plot_hourly_rentals(data, average_hourly_user):
    plt.figure(figsize=(12,6))
    boxplot_hour = sns.boxplot(x=data['dteday'].dt.hour, y='cnt', hue=data['dteday'].dt.hour, data=data, palette='coolwarm')
    boxplot_hour.set(xlabel ="Hour", ylabel = "Total User", title ='Distribution of Bike Rentals Per Hour')

    # Loop through each box to annotate the median
    for patch in boxplot_hour.artists:
        # Get the data from the patch
        x, y = patch.get_xdata(), patch.get_ydata()
        median_value = np.median(y)
        
        # Place a text annotation on the median line
        boxplot_hour.text(x[0] + patch.get_width() / 2, median_value, f'{median_value:.1f}', 
                ha='center', va='center', fontweight='bold', color='white', fontsize=8)

    # Show the plot
    st.pyplot(plt.gcf())

    plt.figure(figsize=(18, 6))

   # Total Rentals (Sum & Mean) per Hour
    ax1 = plt.subplot(1, 3, 1)
    sns.barplot(x='hour', y='cnt_sum', data=average_hourly_user, color='skyblue', label='Total Sum')
    ax1.set_xlabel('Jam dalam Sehari')
    ax1.set_ylabel('Total Rentals (Jumlah)')
    ax1.set_title('Total Rental (Jumlah dan Rata-Rata) per Jam')

    # Create a second y-axis for mean values
    ax2 = ax1.twinx()
    sns.lineplot(x='hour', y='cnt_mean', data=average_hourly_user, marker='o', color='orange', label='Total Mean', ax=ax2)
    ax2.set_ylabel('Total Rental (Rata - Rata)')
    ax2.set_ylim(0, average_hourly_user['cnt_mean'].max() * 1.1)  # Adjust the scale for visibility

    # Add legend for the first subplot
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='upper left')

    # Casual Rentals (Sum & Mean) per Hour
    ax3 = plt.subplot(1, 3, 2)
    sns.barplot(x='hour', y='casual_sum', data=average_hourly_user, color='lightgreen', label='Casual Sum')
    ax3.set_xlabel('Jam dalam Sehari')
    ax3.set_ylabel('Casual Rentals (Jumlah)')
    ax3.set_title('Casual Rentals (Jumlah dan Rata-rata) per Jam')

    # Create a second y-axis for mean values
    ax4 = ax3.twinx()
    sns.lineplot(x='hour', y='casual_mean', data=average_hourly_user, marker='o', color='darkgreen', label='Casual Mean', ax=ax4)
    ax4.set_ylabel('Casual Rentals (Rata-rata)')
    ax4.set_ylim(0, average_hourly_user['casual_mean'].max() * 1.1)  # Adjust the scale for visibility

    # Add legend for the second subplot
    h3, l3 = ax3.get_legend_handles_labels()
    h4, l4 = ax4.get_legend_handles_labels()
    ax3.legend(h3+h4, l3+l4, loc='upper left')

    # Add legend for the second subplot
    h3, l3 = ax3.get_legend_handles_labels()
    h4, l4 = ax4.get_legend_handles_labels()
    ax3.legend(h3+h4, l3+l4, loc='upper left')

    # Registered Rentals (Sum & Mean) per Hour
    ax5 = plt.subplot(1, 3, 3)
    sns.barplot(x='hour', y='registered_sum', data=average_hourly_user, color='thistle', label='Registered Sum')
    ax5.set_xlabel('Jam dalam Sehari')
    ax5.set_ylabel('Registered Rentals (Jumlah)')
    ax5.set_title('Registered Rentals (Sum & Mean) per Hour')

    # Create a second y-axis for mean values
    ax6 = ax5.twinx()
    sns.lineplot(x='hour', y='registered_mean', data=average_hourly_user, marker='o', color='purple', label='Registered Mean', ax=ax6)
    ax6.set_ylabel('Registered Rentals (Rata-rata)')
    ax6.set_ylim(0, average_hourly_user['registered_mean'].max() * 1.1)  # Adjust the scale for visibility

    # Add legend for the third subplot
    h5, l5 = ax5.get_legend_handles_labels()
    h6, l6 = ax6.get_legend_handles_labels()
    ax5.legend(h5+h6, l5+l6, loc='upper left')

    plt.tight_layout()
    st.pyplot(plt.gcf())


# Main Dashboard

st.title('Bike Sharing Analysis Dashboard')
st.write('Dashboard ini berisi analisis dari data penyewaan sepeda untuk menganalisis tren dan pola dalam penggunaan layanan penyewaan sepeda dari berbagai aspek, serta melihat korelasi satu variabel dengan yang lain.')

st.markdown("""
### Tentang Saya
- **Nama**: Patricia Ho
- **Email**: patricia.ho@student.pradita.ac.id
- **ID Dicoding**: [patricia_ho_rKsF](https://www.dicoding.com/users/patricia_ho_rksf)
""")

st.sidebar.header('Bike Sharing Analysis')

data["dteday"] = pd.to_datetime(data["dteday"])
min_date = data["dteday"].min().date()
max_date = data["dteday"].max().date()

with st.sidebar:
    st.image('./data/bicycle-vector.png', width=250)
    st.subheader('Filter Data Here')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    
data = data[(data["dteday"] >= str(start_date)) & 
            (data["dteday"] <= str(end_date))]
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Informasi Umum
st.subheader('Informasi Umum')
st.write(f'Berdasarkan data dari {start_date_str} hingga {end_date_str}, total pengguna yang menggunakan layanan penyewaan sepeda adalah')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", value=data['cnt'].sum())

with col2:
    st.metric("Registered Users", value=data['registered'].sum())

with col3:
    st.metric("Casual Users", value=data['casual'].sum())
    

# Pertanyaan 1: Apa dampak hari libur terhadap jumlah penyewaan sepeda? 
st.subheader('Holiday vs Non-Holiday Rental')
comparison_data_holiday_and_nonholiday_data = comparison_data_holiday_and_nonholiday(data)    
plot_holiday_comparison(data)
plot_monthly_rentals(comparison_data_holiday_and_nonholiday_data)

# Pertanyaan 2: Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda? 
st.subheader('Pengaruh Musim Terhadap Penyewaan Sepeda')
comparison_seasonal_rentals_data = comparison_seasonal_rentals(data)
plot_seasonal_rentals(comparison_seasonal_rentals_data)

# Pertanyaan 3: Apakah kondisi cuaca mempengaruhi jumlah penyewaan sepeda? 
st.subheader('Pengaruh Kondisi Cuaca Terhadap Penyewaan Sepeda')
weather_agg_mean, weather_agg_sum = comparison_weather_conditions(data)
plot_weather_correlation(weather_agg_sum, weather_agg_mean)

# Pertanyaan 4: Bagaimana suhu dan suhu yang dirasakan berkorelasi dengan jumlah penyewaan sepeda? 
st.subheader('Korelasi Suhu dan Suhu yang Dirasakan dengan Penyewaan Sepeda')
correlation_matrix, comparison_temp_category, comparison_atemp_category = comparison_temperature(data)
plot_correlation_temperature(correlation_matrix, comparison_temp_category, comparison_atemp_category)

# Pertanyaan 5: Bagaimana tren penyewaan sepeda dari tahun ke tahun? Bulan dan tahun manakah yang memiliki permintaan penyewaan sepeda tertinggi/terendah? 
st.subheader('Tren Penyewaan Sepeda dari Tahun ke Tahun')
monthly_rentals = comparison_yearly_trends(data)
plot_yearly_trends(monthly_rentals)

# Pertanyaan 6: Bagaimana kecepatan angin mempengaruhi penyewaan sepeda? 
st.subheader('Pengaruh Kecepatan Angin Terhadap Penyewaan Sepeda')
correlation_wind_count, windspeed_effect = comparison_wind_speed(data)
plot_wind_speed_effect(correlation_wind_count, windspeed_effect)

# Pertanyaan 7: Siapa yang lebih banyak menggunakan layanan penyewaan sepeda, pengguna biasa atau pengguna terdaftar?
st.subheader('Pengguna Terdaftar vs Pengguna Biasa')
user_comparison_melted = comparison_registered_vs_casual(data)
plot_registered_vs_casual(user_comparison_melted)

# Pertanyaan 8: Pada jam berapa saja penyewaan sepeda memiliki pengguna terbanyak dan tersedikit?
st.subheader('Frekuensi Penyewaan Sepeda Berdasarkan Jam')
average_hourly_user = comparison_hourly_rentals(data)
plot_hourly_rentals(data, average_hourly_user)


st.caption('Copyright (c) Dicoding 2024, Made By Patricia Ho | ML-27')





