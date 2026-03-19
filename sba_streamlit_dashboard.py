# Importing libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="SBA Loan Dashboard", layout="wide")

st.title("SBA Loan Dashboard") #Title of the Dashboard
st.write("Interactive business analytics dashboard analyzing SBA loan performance") #Short description of the dashboard

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("SBAcase.11.13.17.csv")
    
    df = df.rename(columns={ #Rename the column
        "DisbursementGross":"LoanAmount"
    })
    
    df = df.fillna(0) #Set 0 for missing values
    
    return df

df = load_data()

# Business size categorization
def categorize_business(emp):
    if emp < 5:
        return "Micro"
    elif emp < 50:
        return "Small"
    else:
        return "Medium"

df["BusinessSize"] = df["NoEmp"].apply(categorize_business)

# KPI metrics
avg_loan = df["LoanAmount"].mean() # Get the average Loan of the entire dataset
defaulted_loans = df[df["Default"] == 1] #store the defaulted loans
count_defaulted_loans = len(defaulted_loans) #count the defaulted loans     
total_loans = len(df) #count the loans

col1, col2, col3 = st.columns(3)

col1.metric("Average Loan Amount (USD)", f"${avg_loan:,.2f}") # Average loan
col2.metric("Count of Loan Defaulted", f"{count_defaulted_loans:,.0f}") #Count of Defaulted Loans
col3.metric("Total Loans", f"{total_loans:,}") # Count of Loans

st.divider()

# Loan Distribution
st.subheader("Loan Amount Distribution") # Display the subtitle

fig1 = px.histogram(
    df,
    x="LoanAmount",
    nbins=40,
    title="Distribution of SBA Loan Amounts"
)

st.plotly_chart(fig1, use_container_width=True)

# Loan vs Defaulted
st.subheader("Loan Amount Distribution: Defaulted vs. Non-Defaulted Loans") # Display the subtitle

df['DefaultStatus'] = df['Default'].map({0: 'Non-Defaulted', 1: 'Defaulted'})

# Details of the histogram chart
fig2 = px.histogram(df, x='LoanAmount', color='DefaultStatus', nbins=50,
                   title='Loan Amount Distribution: Defaulted vs. Non-Defaulted Loans',
                   labels={'LoanAmount': 'Loan Amount', 'DefaultStatus': 'Loan Status'},
                   barmode='overlay', opacity=0.7)

st.plotly_chart(fig2, use_container_width=True) #plot the histogram

# Average loan by business size
st.subheader("Average Loan by Business Size") # Display the subtitle
avg_loans = df.groupby("BusinessSize")["LoanAmount"].mean().reset_index()

# Details of the Bar chart
fig3 = px.bar(
    avg_loans,
    x="BusinessSize",
    y="LoanAmount",
    title="Average Loan Amount by Business Size"
)

st.plotly_chart(fig3, use_container_width=True) #plot the bar

# API Integration
st.subheader("USD to PHP Exchange Rate") # Display the subtitle
# Get the current USD rate
try:
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url, timeout=5)
    data = response.json()
    php_rate = data["rates"]["PHP"]
except:
    php_rate = 55.0

st.write(f"Current USD to PHP Rate: {php_rate}") # Display the text and the current rate

avg_loan_php = avg_loan * php_rate # Computes the average Loan amount in PHP
st.write(f"Average Loan Amount in PHP: ₱{avg_loan_php:,.2f}")  # Display the text and the computed average loan amount in PHP
