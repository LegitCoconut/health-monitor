
# HEALTH MONITORING SYSTEM

A simple health monitoring system which collects vital info on the patient and update the values to the server in realtime.

    1. ESP8266
    2. MAX30100 ( spo2 , heart rate monitor)
    3. MPU6050 ( for fall detection )
    4. DS18B20 ( temp sensing)
    5. BUZZER ( for alert if fall or decrease in vitals)



## HOW IT WORKS

- The monitor device collects data of the patients vitals such as heart_rate, sp02, temperature and also check if the patient has fall or not
- If vitals are under the minimum value alert will be given in buzzer and other online services ( telegram bot )
- The collected data is the send to the cloud server using the ESP8266 and the data is stored in the database
- A realtime log/Analytics is shown in a webpage that the server hosts with some simple statitics

## Setup the Arduino Hardware

Required components for the project

```info
  1. ESP8266
  2. MAX30100 
  3. MPU6050 
  4. DS18B20
  5. BUZZER 
  
  6.ARDUINO IDE
```

REFER DOCS ON HOW TO SETUP HARDWARE - [ link ]


## How to setup Server & backend


Clone the github repo to your local machine/server

```bash
  git clone https://github.com/LegitCoconut/health-monitor.git
  cd health-monitor
```
Connect your MongoDB Connection string
```python
    -- if using local mongoDB instance
    client = MongoClient("mongodb://localhost:27017/")

    -- if using cloud instance
    client = MongoClient("<replace_with_connection_string>")
```
    
Install virtual env if not there
```python
    pip install venv
```
Setup the virtual env 
```python
    python3 -m venv myenv

    -- for macOS & linux
    source myenv/bin/activate

    -- for windows
    myenv\Scripts\activate
```
Install the requirements
```python
    pip install requirements.txt
```
Run the Flask server for the web ui
```python
    python app.py
```

Run the test.py for adding some random data for testing
```python 
    python test.py
```