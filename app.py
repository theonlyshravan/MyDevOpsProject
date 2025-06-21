from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()  

MONGO_URI = os.getenv('MONGO_URI')

print(f"Attempting to connect with MONGO_URI: {MONGO_URI}")

app = Flask(__name__)

client = MongoClient(MONGO_URI)

db = client.flask_app_data

collection = db.user_data  

        
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=['GET'])
def display_form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        data_from_form = request.form.to_dict()
        try:
            collection.insert_one(data_from_form)
            print(f"Data submitted to MongoDB: {data_from_form}")
            return render_template('success.html')
        except Exception as e:
            print(f"Error submitting data to MongoDB: {e}")
            return render_template('form.html', error="Failed to submit data. Please check connection and try again.")
      
      
if __name__ == '__main__':  
        
    app.run(debug = True)