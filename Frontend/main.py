import streamlit as st
from pages import page1

# Set the layout of the page
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Define a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Page 1", "Page 2", "Page 3"))

# Load the selected page
if page == "Page 1":
    page1.show()


# Footer
st.sidebar.info("Built with Streamlit")

