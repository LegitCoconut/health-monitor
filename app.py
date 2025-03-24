import io
import base64
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify, send_file , render_template, jsonify, request
from pymongo import MongoClient



app = Flask(__name__)

# MongoDB Connection
MONGO_URI = os.environ.get("MONGO_URI") 
client = MongoClient(MONGO_URI)
db = client["health_data"]
logs_collection = db["logs"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_logs")
def get_logs():
    logs = list(logs_collection.find({}, {"_id": 0}).sort([("_id", -1)]))  # Exclude ObjectId
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

@app.route("/generate_graph")
def generate_graph():
    logs = list(logs_collection.find({}, {"_id": 0}))  
    if not logs:
        return jsonify({"error": "No data available"}), 404

    df = pd.DataFrame(logs)
    df["time_of_check"] = pd.to_datetime(df["time_of_check"])  
    df.sort_values("time_of_check", inplace=True)

    plt.figure(figsize=(8, 5))
    plt.plot(df["time_of_check"], df["Heart_beat_rate"], label="Heart Rate (BPM)", marker='o')
    plt.plot(df["time_of_check"], df["Sp02_level"], label="SpO2 Level (%)", marker='s')
    plt.plot(df["time_of_check"], df["Temperature"], label="Temperature (°C)", marker='^')

    plt.xlabel("Time of Check")
    plt.ylabel("Values")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    # Save the image in memory
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches="tight")
    plt.close()
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
