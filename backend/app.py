from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import pymongo
from bson import ObjectId
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Use environment variable for secret key
app.secret_key = os.getenv(
    "SECRET_KEY", "your-secret-key"
)  # Loads SECRET_KEY from .env

# MongoDB credentials and URI
MONGODB_USER = os.getenv("MONGODB_USER")  # Loads the MongoDB username from .env
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")  # Loads the MongoDB password from .env

# Construct the MongoDB URI dynamically
MONGODB_URI = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@bank.hphlh.mongodb.net/banking_db?retryWrites=true&w=majority&appName=bank"

# Configure Flask app with MongoDB URI
app.config["MONGO_URI"] = MONGODB_URI
mongo = PyMongo(app)

# EmailJS configuration
EMAILJS_USER_ID = "duGyQMPA15QXvU-LA"
EMAILJS_SERVICE_ID = "default_service"
EMAILJS_TEMPLATE_ID_APPROVAL = "template_jwoiro3"
EMAILJS_TEMPLATE_ID_REJECTION = "template_jwoiro3"

def insert_initial_data():
    try:
        # Get the banks collection (it will be created if it doesn't exist)
        collection = mongo.db.banks

        banks_data = [
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

        # Insert each bank individually
        for bank in banks_data:
            existing_bank = collection.find_one({"name": bank["name"]})
            if not existing_bank:
                collection.insert_one(bank)
                print(f"Inserted {bank['name']} into MongoDB.")
            else:
                print(f"Bank '{bank['name']}' already exists, skipping insertion.")

        return True
    except Exception as e:
        print(f"Error inserting initial data: {str(e)}")
        return False


@app.route("/api/banks", methods=["GET"])
def get_banks():
    try:
        banks = list(mongo.db.banks.find({}, {"_id": 0}))
        return jsonify(banks)
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve banks: {str(e)}"}), 500


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]

    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400

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
    required_fields = ["name", "email", "cardType", "address", "phone", "dob", "income", "agreeTerms", "bankName"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    # Insert into the database
    mongo.db.card_applications.insert_one({
        "name": data["name"],
        "email": data["email"],
        "cardType": data["cardType"],
        "address": data["address"],
        "phone": data["phone"],
        "dob": data["dob"],
        "income": data["income"],
        "agreeTerms": data["agreeTerms"],
        "bankName": data["bankName"],  # Add bankName to the data
    })

    return jsonify({"message": "Application submitted successfully!"}), 201

def send_email(to_email, template_id, template_params):
    url = "https://api.emailjs.com/api/v1.0/email/send"
    payload = {
        "user_id": EMAILJS_USER_ID,
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": template_id,
        "template_params": {
            "to_email": to_email,
            **template_params
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 200

@app.route("/admin_console", methods=["GET"])
def get_card_applications():
    try:
        applications = list(mongo.db.card_applications.find())
        for app in applications:
            app['_id'] = str(app['_id'])
            if 'status' not in app:
                app['status'] = 'Pending'
        return jsonify(applications)
    except Exception as e:
        print(f"Error fetching applications: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/admin_console/approve/<application_id>", methods=["POST"])
def approve_application(application_id):
    try:
        application = mongo.db.card_applications.find_one_and_update(
            {"_id": ObjectId(application_id)},
            {"$set": {"status": "Approved"}},
            return_document=True
        )
        
        if application:
            # Send approval email here
            # For now, we'll just print a message
            print(f"Approval email sent to {application['email']}")
            return jsonify({"message": "Application approved and email sent"}), 200
        return jsonify({"message": "Application not found"}), 404
    except Exception as e:
        print(f"Error approving application: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/admin_console/reject/<application_id>", methods=["POST"])
def reject_application(application_id):
    try:
        application = mongo.db.card_applications.find_one_and_update(
            {"_id": ObjectId(application_id)},
            {"$set": {"status": "Rejected"}},
            return_document=True
        )
        
        if application:
            # Send rejection email here
            # For now, we'll just print a message
            print(f"Rejection email sent to {application['email']}")
            return jsonify({"message": "Application rejected and email sent"}), 200
        return jsonify({"message": "Application not found"}), 404
    except Exception as e:
        print(f"Error rejecting application: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if insert_initial_data():
        print("Initial data inserted successfully")
        app.run(debug=True)
    else:
        print("Failed to insert initial data")
