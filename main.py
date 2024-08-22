# import streamlit as st
# import pandas as pd

# # Set page title
# st.set_page_config(page_title="Accident Data Viewer 2021")

# # Add a title to the app
# st.title("Accident Data Viewer 2021")

# # Load the CSV file
# @st.cache_data
# def load_data():
#     return pd.read_csv("accident2021.csv")

# df = load_data()

# # Display the dataframe
# st.dataframe(df)

# # Add some basic statistics
# st.subheader("Basic Statistics")
# st.write(f"Total number of accidents: {len(df)}")
# st.write(f"Number of columns: {len(df.columns)}")

# # Add a section for user to select columns to view
# st.subheader("Select columns to view")
# selected_columns = st.multiselect("Choose columns", df.columns.tolist(), default=df.columns.tolist()[:5])

# # Display selected columns
# if selected_columns:
#     st.dataframe(df[selected_columns])
# else:
#     st.warning("Please select at least one column.")
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Set page config
st.set_page_config(page_title="Accident Data Analysis 2021", layout="wide")

# Load data more efficiently
@st.cache_data
def load_data():
    dtypes = {
        'วันที่เกิดเหตุ': str,
        'เวลา': str,
        'LATITUDE': float,
        'LONGITUDE': float,
        'ผู้เสียชีวิต': int,
        'ผู้บาดเจ็บสาหัส': int,
        'ผู้บาดเจ็บเล็กน้อย': int
    }
    df = pd.read_csv("accident2021.csv", dtype=dtypes)
    
    # Convert date column to datetime
    df['วันที่เกิดเหตุ'] = pd.to_datetime(df['วันที่เกิดเหตุ'], format='%d/%m/%Y', errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['วันที่เกิดเหตุ'])
    
    return df

df = load_data()

st.title("Accident Data Analysis 2021")

# 1. Analysis of accident trends
st.header("1. Analysis of Accident Trends")

# Daily trend
fig, ax = plt.subplots(figsize=(12, 6))
daily_accidents = df['วันที่เกิดเหตุ'].dt.date.value_counts().sort_index()
sns.lineplot(x=daily_accidents.index, y=daily_accidents.values, ax=ax)
ax.set_title("Daily Accident Frequency")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Accidents")
plt.xticks(rotation=45)
st.pyplot(fig)

# Hourly trend
fig, ax = plt.subplots(figsize=(12, 6))
df['hour'] = pd.to_datetime(df['เวลา']).dt.hour
hourly_accidents = df['hour'].value_counts().sort_index()
sns.barplot(x=hourly_accidents.index, y=hourly_accidents.values, ax=ax)
ax.set_title("Hourly Accident Frequency")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Number of Accidents")
st.pyplot(fig)

# 2. Identification of high-risk areas
st.header("2. Identification of High-risk Areas")

# Map of accident locations (using Streamlit's map function)
st.subheader("Map of Accident Locations")
# Filter out rows with NaN values in LATITUDE or LONGITUDE
map_data = df.dropna(subset=['LATITUDE', 'LONGITUDE'])

if not map_data.empty:
    st.map(map_data[['LATITUDE', 'LONGITUDE']])
else:
    st.warning("No valid location data available for mapping.")

# Show statistics about the mapped data
st.write(f"Total accidents: {len(df)}")
st.write(f"Accidents with valid coordinates: {len(map_data)}")
st.write(f"Percentage of accidents mapped: {len(map_data) / len(df) * 100:.2f}%")

# 3. Analysis of accident causes
st.header("3. Analysis of Accident Causes")

# Suspected causes
fig, ax = plt.subplots(figsize=(12, 6))
causes = df['มูลเหตุสันนิษฐาน'].value_counts()
sns.barplot(x=causes.values, y=causes.index, ax=ax)
ax.set_title("Frequency of Suspected Causes")
ax.set_xlabel("Number of Accidents")
st.pyplot(fig)

# Weather conditions
fig, ax = plt.subplots(figsize=(10, 10))
weather = df['สภาพอากาศ'].value_counts()
ax.pie(weather.values, labels=weather.index, autopct='%1.1f%%')
ax.set_title("Accidents by Weather Condition")
st.pyplot(fig)

# 4. Analysis of vehicle types
st.header("4. Analysis of Vehicle Types")

vehicle_columns = ['รถจักรยานยนต์', 'รถยนต์นั่งส่วนบุคคล', 'รถปิคอัพบรรทุก4ล้อ', 'รถบรรทุก6ล้อ', 'รถอื่นๆ']
fig, ax = plt.subplots(figsize=(12, 6))
vehicle_counts = df[vehicle_columns].sum()
sns.barplot(x=vehicle_counts.index, y=vehicle_counts.values, ax=ax)
ax.set_title("Frequency of Vehicle Types in Accidents")
ax.set_xlabel("Vehicle Type")
ax.set_ylabel("Number of Accidents")
plt.xticks(rotation=45)
st.pyplot(fig)

# 5. Analysis of accident severity
st.header("5. Analysis of Accident Severity")

severity_columns = ['ผู้เสียชีวิต', 'ผู้บาดเจ็บสาหัส', 'ผู้บาดเจ็บเล็กน้อย']
fig, ax = plt.subplots(figsize=(12, 6))
severity_data = df[severity_columns].sum()
sns.barplot(x=severity_data.index, y=severity_data.values, ax=ax)
ax.set_title("Accident Severity")
ax.set_xlabel("Severity Type")
ax.set_ylabel("Number of People")
plt.xticks(rotation=45)
st.pyplot(fig)

# Correlation between vehicle types and severity
st.subheader("Correlation between Vehicle Types and Accident Severity")
correlation = df[vehicle_columns + severity_columns].corr()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Note on additional analyses
st.header("Additional Analyses")
st.write("""
The following analyses would require more complex data processing or additional data:
- Accident prevention and reduction planning
- Predictive modeling
- Detailed reporting and data presentation
""")