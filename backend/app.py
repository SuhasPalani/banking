from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import pymongo

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Use environment variable for secret key
app.secret_key = os.getenv("SECRET_KEY")

# Use environment variable for Mongo URI
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# Function to insert bank data into the MongoDB
def insert_initial_data():
    db = mongo.db  # Use the PyMongo connection already established
    collection = db["banks"]

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
                "location": {
                    "headquarters": "Los Angeles, USA",
                    "global_offices": ["USA"],
                },
                "atm_network": {"total_atms": 1500, "international_atms": False},
                "competitors": ["Greenfield Bank", "Sunrise Financial"],
            },
        ]
    }

    # Insert data into the MongoDB collection only if it doesn't already exist
    for bank in data["banks"]:
        # Check if the bank already exists by its name
        existing_bank = collection.find_one({"name": bank["name"]})
        if not existing_bank:  # If no existing document found with this name
            result = collection.insert_one(bank)
            print(f"Inserted {bank['name']} into MongoDB.")
        else:
            print(f"Bank '{bank['name']}' already exists, skipping insertion.")

@app.route("/api/banks", methods=["GET"])
def get_banks():
    try:
        # Retrieve all banks from the MongoDB collection
        banks = list(mongo.db.banks.find({}, {"_id": 0}))
        return jsonify(banks)
    except Exception as e:
        return jsonify({"error": f"Failed to connect to MongoDB: {str(e)}"}), 500

# User Authentication Routes
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    
    # Check if user already exists by email
    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400

    # If not, hash the password and insert the new user into the database
    hashed_pw = generate_password_hash(data["password"])
    mongo.db.users.insert_one({"email": email, "password": hashed_pw})
    
    return jsonify({"message": "User created"}), 201

@app.route("/signin", methods=["POST"])
def signin():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})
    
    if user and check_password_hash(user["password"], data["password"]):
        session["user"] = data["email"]
        return jsonify({"message": "Logged in"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/apply-card", methods=["POST"])
def apply_card():
    data = request.json

    # Validate required fields
    if not data.get("name") or not data.get("email") or not data.get("cardType"):
        return jsonify({"message": "All fields are required"}), 400

    # Insert application into MongoDB
    mongo.db.card_applications.insert_one({
        "name": data["name"],
        "email": data["email"],
        "cardType": data["cardType"],
    })

    return jsonify({"message": "Application submitted successfully!"}), 201

    
    
if __name__ == "__main__":
    insert_initial_data()  # Insert the data when the app starts
    app.run(debug=True)