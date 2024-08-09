import streamlit as st
import pandas as pd
import numpy as np

def show():
    # Page title
    st.title("Page 1 - Interactive Data Visualization")

    # Description
    st.write("This page demonstrates basic interactive components in Streamlit.")

    # Text input
    user_input = st.text_input("Enter your name:", "")
    if user_input:
        st.write(f"Hello, {user_input}!")

    # Button
    if st.button("Click me!"):
        st.write("Button clicked!")

    # Slider
    value = st.slider("Select a value:", 0, 100, 50)
    st.write(f"Selected value: {value}")

    # Generate random data
    data = pd.DataFrame(
        np.random.randn(50, 3),
        columns=["A", "B", "C"]
    )

    # Display data as a table
    st.write("Random Data")
    st.dataframe(data)

    # Line chart
    st.write("Line Chart")
    st.line_chart(data)

    # Bar chart
    st.write("Bar Chart")
    st.bar_chart(data)

    # Plotting using Matplotlib
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.hist(data['A'], bins=20)
    st.pyplot(fig)

if __name__ == "__main__":
    show()
