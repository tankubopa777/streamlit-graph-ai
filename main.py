import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="Accident Data Viewer 2021")

# Add a title to the app
st.title("Accident Data Viewer 2021")

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("accident2021.csv")

df = load_data()

# Display the dataframe
st.dataframe(df)

# Add some basic statistics
st.subheader("Basic Statistics")
st.write(f"Total number of accidents: {len(df)}")
st.write(f"Number of columns: {len(df.columns)}")

# Add a section for user to select columns to view
st.subheader("Select columns to view")
selected_columns = st.multiselect("Choose columns", df.columns.tolist(), default=df.columns.tolist()[:5])

# Display selected columns
if selected_columns:
    st.dataframe(df[selected_columns])
else:
    st.warning("Please select at least one column.")