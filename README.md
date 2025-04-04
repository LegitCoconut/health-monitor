
# 🩺 Health Monitoring System

A **real-time IoT health monitoring system** that collects vital signs (heart rate, SpO₂, temperature) from wearable sensors, and logs all data to a Flask-based web dashboard for visualization and analytics.

---

## ⚙️ Hardware Components

| Component     | Function                             |
|--------------|---------------------------------------|
| **ESP8266**   | WiFi microcontroller (data transmission) |
| **MAX30100**  | Heart rate and SpO₂ sensor            |
| **DS18B20**   | Digital temperature sensor            |
| **Buzzer**    | Audio alert in case of abnormal values or fall |
| **Power**     | 3.3V regulated supply                 |

> 📄 Refer to [hardware setup guide](#) for circuit connection and Arduino IDE configuration.

---

## 📡 How It Works

1. **Sensor Data Collection**  
   ESP8266 reads from:
   - MAX30100 → `Heart_rate`, `SpO₂`
   - DS18B20 → `Temperature`

2. **Alert System**  
   - If any vital drops below threshold or is detected → buzzer rings.
   - Simultaneously, Telegram bot sends alert to caretaker.

3. **Data Transmission**  
   - ESP8266 sends data to Flask server via HTTP POST (`/add_log`) endpoint.

4. **Web Dashboard**  
   - Web UI shows real-time logs and plots (heart rate, SpO₂, temperature).
   - Alerts are also logged and visualized for analytics.

---

## 🌐 Software Architecture

**Backend**: Flask + MongoDB  
**Frontend**: HTML + Chart via Matplotlib  
**Data Storage**: MongoDB (Local/Cloud)  
**IoT Firmware**: Arduino (C++)

---

## 💾 Setting Up the Server & Backend

### 🔁 Clone the Repository

```bash
git clone https://github.com/LegitCoconut/health-monitor.git
cd health-monitor
```

### 🧪 Python Environment

Install virtual environment (optional but recommended):

```bash
python3 -m venv myenv
```

Activate it:

- Linux/macOS:
  ```bash
  source myenv/bin/activate
  ```

- Windows:
  ```cmd
  myenv\Scripts\activate
  ```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ MongoDB Setup

#### Local MongoDB:

```python
client = MongoClient("mongodb://localhost:27017/")
```

#### Cloud MongoDB (e.g., Atlas):

Set this as an environment variable:

```bash
export MONGO_URI="your_mongo_connection_string"
```

On Windows (CMD):

```cmd
set MONGO_URI="your_mongo_connection_string"
```

> You can also create a `.env` file and load it manually.

---

## 🚀 Run the Flask Server

```bash
python app.py
```

Flask app will run at: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Generate Test Data

To simulate sensor data:

```bash
python test.py
```

---

## ☁️ Deployment on Vercel (Optional)

1. Fork or push the project to your GitHub account.
2. Login to [Vercel](https://vercel.com), import the GitHub repo.
3. In **Project Settings > Environment Variables**, add:

| Key        | Value                        |
|------------|------------------------------|
| `MONGO_URI`| your MongoDB connection URI  |

4. Set **Framework Preset** as `Other` or `Flask`.
5. Vercel will auto-deploy your project.

> ⚠️ Note: Vercel is for frontend apps. For backend Flask, use **Render**, **Railway**, or deploy on **VPS** (DigitalOcean, EC2, etc.).

---

## 🧠 Code Overview (Crucial Sections)

### `app.py` (Flask Backend)

#### `@app.route("/add_log", methods=["POST"])`
Receives JSON data from ESP8266:
```json
{
  "Heart_beat_rate": 80,
  "Sp02_level": 96,
  "Temperature": 36.5,
  "time_of_check": "2025-04-04T12:30:00"
}
```
Inserts into MongoDB:  
```python
logs_collection.insert_one(data)
```

#### `@app.route("/stats")`
Calculates average, peak, and low values for each vital using:
```python
def compute_stats(field):
    ...
```

#### `@app.route("/generate_graph")`
Generates time-series graph using `matplotlib`, returns image as PNG:
```python
plt.savefig(img_io, format='png')
return send_file(img_io, mimetype='image/png')
```

---

## 📊 Web Dashboard Routes

| Endpoint         | Description                    |
|------------------|--------------------------------|
| `/`              | Main dashboard (`index.html`)  |
| `/get_logs`      | Returns all logs (JSON)        |
| `/add_log`       | Accepts data from device (POST)|
| `/stats`         | Returns statistical metrics    |
| `/generate_graph`| Returns graph (PNG image)      |

---

## 📦 Directory Structure

```bash
health-monitor/
│
├── app.py             # Main Flask backend
├── test.py            # Dummy data injector
├── requirements.txt   # Python dependencies
├── templates/
│   └── index.html     # Web dashboard UI
└── static/            # (Optional CSS/JS)
```

---

## 🛡️ Security Recommendations

- Validate incoming sensor data types.
- Use `.env` for secrets like DB credentials.
- Add basic auth to dashboard (Flask-login or JWT).
- Secure MongoDB with IP whitelisting or VPN.

---
