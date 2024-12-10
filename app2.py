import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Function to fetch data from Alpha Vantage
def fetch_av_data(function, symbol, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "Note" in data or "Error Message" in data:
            st.error(f"API Error: {data.get('Note') or data.get('Error Message')}")
            return None
        return data
    else:
        st.error(f"HTTP Error: {response.status_code}")
        return None

# Function to format and display data
def display_data(data, title):
    st.subheader(title)
    if isinstance(data, dict):
        df = pd.DataFrame(data.items(), columns=["Field", "Value"])
        st.table(df)
    elif isinstance(data, list):
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write(data)

# Function to prettify field names
def prettify_field_name(field):
    return " ".join([word.capitalize() for word in field.split("_")])

# Main Streamlit App
def main():
    st.title("Stock Data Viewer")

    # Hard-coded API key (replace with your actual API key)
    api_key = "CLP9IN76G4S8OUXN"  # Replace with your API key

    # Sidebar for user input
    ticker = st.sidebar.text_input("Enter Stock Ticker Symbol", value="IBM").upper()

    if st.sidebar.button("Get Data"):
        # Define the endpoints to pull data
        functions = {
            "Company Overview": "OVERVIEW",
            "Income Statement": "INCOME_STATEMENT",
            "Balance Sheet": "BALANCE_SHEET",
            "Cash Flow": "CASH_FLOW",
            "Earnings": "EARNINGS"
        }

        # Tabs for each category
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Company Overview", "Income Statement", "Balance Sheet", "Cash Flow", "Earnings"]
        )

        # Fetch and display data for each tab
        for title, function in functions.items():
            data = fetch_av_data(function, ticker, api_key)

            if data:
                if function == "OVERVIEW":
                    with tab1:
                        st.header("Company Overview")
                        display_data(data, "Company Overview")

                elif function == "INCOME_STATEMENT":
                    with tab2:
                        st.header("Income Statement")
                        view_type = st.radio("Select View Type:", ("Annual", "Quarterly"), horizontal=True)
                        if view_type == "Annual" and "annualReports" in data:
                            display_data(data["annualReports"], "Annual Reports")
                        elif view_type == "Quarterly" and "quarterlyReports" in data:
                            display_data(data["quarterlyReports"], "Quarterly Reports")

                elif function == "BALANCE_SHEET":
                    with tab3:
                        st.header("Balance Sheet")
                        view_type = st.radio("Select View Type:", ("Annual", "Quarterly"), horizontal=True)
                        if view_type == "Annual" and "annualReports" in data:
                            display_data(data["annualReports"], "Annual Reports")
                        elif view_type == "Quarterly" and "quarterlyReports" in data:
                            display_data(data["quarterlyReports"], "Quarterly Reports")

                elif function == "CASH_FLOW":
                    with tab4:
                        st.header("Cash Flow")
                        view_type = st.radio("Select View Type:", ("Annual", "Quarterly"), horizontal=True)
                        if view_type == "Annual" and "annualReports" in data:
                            display_data(data["annualReports"], "Annual Reports")
                        elif view_type == "Quarterly" and "quarterlyReports" in data:
                            display_data(data["quarterlyReports"], "Quarterly Reports")

                elif function == "EARNINGS":
                    with tab5:
                        st.header("Earnings")
                        view_type = st.radio("Select View Type:", ("Annual", "Quarterly"), horizontal=True)
                        if view_type == "Annual" and "annualEarnings" in data:
                            display_data(data["annualEarnings"], "Annual Earnings")
                        elif view_type == "Quarterly" and "quarterlyEarnings" in data:
                            display_data(data["quarterlyEarnings"], "Quarterly Earnings")

                # Add Graphs for key financial metrics (if applicable)
                if function == "INCOME_STATEMENT" and "annualReports" in data:
                    with tab2:
                        st.markdown("### Revenue Over Time")
                        df = pd.DataFrame(data["annualReports"])
                        if "fiscalDateEnding" in df and "totalRevenue" in df:
                            df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"])
                            df["totalRevenue"] = pd.to_numeric(df["totalRevenue"], errors="coerce")
                            fig = px.line(df, x="fiscalDateEnding", y="totalRevenue", title="Revenue Over Time")
                            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
