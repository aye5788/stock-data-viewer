import streamlit as st
import requests
import pandas as pd

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
        # Check for error messages in the response
        if "Note" in data or "Error Message" in data:
            st.error(f"API Error: {data.get('Note') or data.get('Error Message')}")
            return None
        return data
    else:
        st.error(f"HTTP Error: {response.status_code}")
        return None

# Function to display data
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

def main():
    st.title("Stock Data Viewer")
    
    # Hard-coded API key (replace with your actual API key)
    api_key = "CLP9IN76G4S8OUXN"  # Replace with your Alpha Vantage API key

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
        
        for title, function in functions.items():
            data = fetch_av_data(function, ticker, api_key)
            if data:
                if function in ["INCOME_STATEMENT", "BALANCE_SHEET", "CASH_FLOW"]:
                    # Display annual reports
                    if 'annualReports' in data:
                        st.markdown(f"### {title} - Annual Reports")
                        display_data(data['annualReports'], f"{title} - Annual Reports")
                    # Display quarterly reports
                    if 'quarterlyReports' in data:
                        st.markdown(f"### {title} - Quarterly Reports")
                        display_data(data['quarterlyReports'], f"{title} - Quarterly Reports")
                elif function == "EARNINGS":
                    # Display annual earnings
                    if 'annualEarnings' in data:
                        st.markdown(f"### {title} - Annual Earnings")
                        display_data(data['annualEarnings'], f"{title} - Annual Earnings")
                    # Display quarterly earnings
                    if 'quarterlyEarnings' in data:
                        st.markdown(f"### {title} - Quarterly Earnings")
                        display_data(data['quarterlyEarnings'], f"{title} - Quarterly Earnings")
                else:
                    display_data(data, title)

if __name__ == "__main__":
    main()
