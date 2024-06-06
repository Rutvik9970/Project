from flask import Flask, render_template, jsonify
import subprocess
import pymongo

app = Flask(__name__)

# MongoDB configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["trending_topics"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['GET'])
def run_script():
    result = subprocess.run(['python', 'twitter_scraper.py'], capture_output=True, text=True)
    return jsonify({"message": "Script executed successfully", "result": result.stdout})

@app.route('/latest_results', methods=['GET'])
def latest_results():
    latest_record = collection.find().sort([("$natural", -1)]).limit(1)
    for record in latest_record:
        return jsonify(record)
    return jsonify({"message": "No records found"})

if __name__ == "__main__":
    app.run(debug=True)