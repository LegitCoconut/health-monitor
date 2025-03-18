
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
