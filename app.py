from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS on all routes

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a database model for storing reviews
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, nullable=False)
    processed_review = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)

# Create the database within an application context
with app.app_context():
    db.create_all()

# Function to clean and process a review
def preprocess_review(review):
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    return ' '.join(review)

# Flask route for sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze_review():
    data = request.get_json()
    print("Received data:", data)  # This will print the data to the console
    review = data['review']
    processed_review = preprocess_review(review)
    sentiment = "Positive" if "good" in processed_review else "Negative"
    response = jsonify({"review": review, "processed_review": processed_review, "sentiment": sentiment})
    print("Response:", response.get_json())  # This prints the response data
    return response

# Root route to prevent unnecessary 404 errors
@app.route('/')
def home():
    return "Welcome to the Restaurant Review API!"

# Favicon route to handle favicon.ico requests
@app.route('/favicon.ico')
def favicon():
    return "", 204  # No content to return
  
# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5002)

