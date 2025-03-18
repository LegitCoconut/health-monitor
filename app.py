from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["health_data"]
logs_collection = db["logs"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_logs")
def get_logs():
    logs = list(logs_collection.find({}, {"_id": 0}))  # Exclude ObjectId
    return jsonify(logs)

@app.route("/stats")
def get_stats():
    logs = list(logs_collection.find({}, {"_id": 0}))  

    if not logs:
        return jsonify({"error": "No data available"}), 404

    def compute_stats(field):
        values = [log[field] for log in logs if field in log]
        if not values:
            return {"avg": 0, "peak": 0, "low": 0}
        return {
            "avg": round(sum(values) / len(values), 1),
            "peak": max(values),
            "low": min(values),
        }

    stats = {
        "Heart_beat_rate": compute_stats("Heart_beat_rate"),
        "Sp02_level": compute_stats("Sp02_level"),
        "Temperature": compute_stats("Temperature"),
    }

    return jsonify(stats)

@app.route("/add_log", methods=["POST"])
def add_log():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    logs_collection.insert_one(data)
    return jsonify({"message": "Log added successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
