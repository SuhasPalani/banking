import pymongo
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load the environment variables from .env file
load_dotenv()

# Get MongoDB URL from environment variables
mongo_url = os.getenv("MONGO_URI")  # Ensure you have the 'MONGO_URL' in your .env file

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client["banksDB"]  # Create or use an existing database
collection = db["banks"]  # Create or use an existing collection

# Define the JSON data (replace this with the actual JSON from the file)
data = {
    "banks": [
        {
            "name": "Greenfield Bank",
            "type": "Commercial Bank",
            "established": "1998",
            "branches": 120,
            "services": [
                "Savings Accounts",
                "Checking Accounts",
                "Student Loans",
                "Credit Cards",
                "Debit Cards",
                "Mortgages",
                "Personal Loans",
            ],
            "student_services": [
                "Student Checking Accounts",
                "Student Savings Accounts",
                "Low-Interest Student Loans",
                "Credit Card for Students with Low Limits",
                "Education Planning Tools",
            ],
            "online_features": [
                "Mobile Banking",
                "Online Bill Pay",
                "24/7 Customer Service",
                "Student Loan Management Tools",
                "Investment Management",
                "Credit Score Monitoring",
            ],
            "contact_details": {
                "phone": "+1-800-123-4567",
                "email": "support@greenfieldbank.com",
                "website": "https://www.greenfieldbank.com",
            },
            "location": {
                "headquarters": "New York, USA",
                "global_offices": ["USA", "UK", "Germany", "Canada"],
            },
            "atm_network": {"total_atms": 2500, "international_atms": True},
            "competitors": ["Sunrise Financial", "Pacific Trust Bank"],
        },
        {
            "name": "Sunrise Financial",
            "type": "Investment Bank",
            "established": "2005",
            "branches": 45,
            "services": [
                "Wealth Management",
                "Private Equity",
                "Stock Trading",
                "Asset Management",
                "Credit Cards",
                "Student Financial Planning",
            ],
            "student_services": [
                "Student Credit Cards with Rewards",
                "Low-Interest Student Loans",
                "Student Financial Planning and Budgeting Tools",
            ],
            "online_features": [
                "Brokerage Services",
                "Risk Management Tools",
                "Account Alerts",
                "Financial Advisors",
                "Student Loan Refinancing",
            ],
            "contact_details": {
                "phone": "+1-800-987-6543",
                "email": "help@sunrisefinancial.com",
                "website": "https://www.sunrisefinancial.com",
            },
            "location": {
                "headquarters": "San Francisco, USA",
                "global_offices": ["USA", "China", "India", "Singapore"],
            },
            "atm_network": {"total_atms": 500, "international_atms": False},
            "competitors": ["Greenfield Bank", "Pacific Trust Bank"],
        },
        {
            "name": "Pacific Trust Bank",
            "type": "Savings & Loan Association",
            "established": "2012",
            "branches": 80,
            "services": [
                "High-Interest Savings",
                "Certificates of Deposit",
                "Auto Loans",
                "Home Equity Loans",
                "Student Loans",
                "Credit Cards",
                "Debit Cards",
            ],
            "student_services": [
                "Student Loans with Flexible Repayment Options",
                "Student Checking and Savings Accounts",
                "No Annual Fee Credit Cards for Students",
                "Educational Resources for Financial Literacy",
            ],
            "online_features": [
                "Direct Deposit",
                "Loan Calculators",
                "Budgeting Tools",
                "Secure Transfers",
                "Student Loan Management",
                "Financial Literacy Resources",
            ],
            "contact_details": {
                "phone": "+1-888-234-5678",
                "email": "contact@pacifictrust.com",
                "website": "https://www.pacifictrustbank.com",
            },
            "location": {"headquarters": "Los Angeles, USA", "global_offices": ["USA"]},
            "atm_network": {"total_atms": 1500, "international_atms": False},
            "competitors": ["Greenfield Bank", "Sunrise Financial"],
        },
    ]
}

# Insert data into the MongoDB collection
result = collection.insert_many(data["banks"])

# Print result of insertion
print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
