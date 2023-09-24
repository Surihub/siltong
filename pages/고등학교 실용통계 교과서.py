import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Titanic dataset
@st.cache_data 
def load_data():
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    data = pd.read_csv(url)
    return data

# Main function to create the Streamlit app
def main():
    st.title("Titanic Dataset Visualization")

    # Load the dataset
    data = load_data()

    # Sidebar options
    st.sidebar.header("Visualization Options")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar Chart", "Histogram", "Pie Chart"])

    # Conditional rendering based on selected plot type
    if plot_type == "Bar Chart":
        st.sidebar.subheader("Bar Chart Configuration")
        x_column = st.sidebar.selectbox("Select X-axis Column", data.columns)
        y_column = st.sidebar.selectbox("Select Y-axis Column", data.columns)
        bar_chart = px.bar(data, x=x_column, y=y_column, title=f"Bar Chart: {x_column} vs {y_column}")
        st.plotly_chart(bar_chart)

    elif plot_type == "Histogram":
        st.sidebar.subheader("Histogram Configuration")
        x_column = st.sidebar.selectbox("Select Column for Histogram", data.columns)
        histogram = px.histogram(data, x=x_column, title=f"Histogram: {x_column}")
        st.plotly_chart(histogram)

    elif plot_type == "Pie Chart":
        st.sidebar.subheader("Pie Chart Configuration")
        label_column = st.sidebar.selectbox("Select Label Column", data.columns)
        pie_chart = px.pie(data, names=label_column, title=f"Pie Chart: {label_column} Distribution")
        st.plotly_chart(pie_chart)

    # Show the raw data if checkbox is selected
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.write(data)

if __name__ == "__main__":
    main()
