#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ESP8266HTTPClient.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS 2000
#define NTP_SERVER "pool.ntp.org"
#define TIMEZONE_OFFSET 19800  // Offset in seconds (5 hrs 30 min for IST)

// Wi-Fi Credentials
const char* ssid = "hotspot_ssid";
const char* password = "hotspot_password";

// Flask Server URL
const char* serverURL = "http://<local_web_server_url>/add_log";

// NTP Client Setup
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_SERVER, TIMEZONE_OFFSET);

PulseOximeter pox;
uint32_t tsLastReport = 0;

void onBeatDetected() {
    Serial.println("Beat!");
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");

    timeClient.begin();
    timeClient.update();

    Serial.print("Initializing MAX30100...");
    if (!pox.begin()) {
        Serial.println("FAILED");
        for (;;);
    }
    Serial.println("SUCCESS");

    pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
    pox.update();
    timeClient.update();  // Update time from NTP server

    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        float heartRate = pox.getHeartRate();
        float spO2 = pox.getSpO2();
        String timestamp = timeClient.getFormattedTime();

        Serial.print("Heart Rate: ");
        Serial.print(heartRate);
        Serial.print(" bpm / SpO2: ");
        Serial.print(spO2);
        Serial.print(" % / Time: ");
        Serial.println(timestamp);

        sendDataToServer(heartRate, spO2, timestamp);

        tsLastReport = millis();
    }
}

void sendDataToServer(float hr, float spo2, String timestamp) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        WiFiClient client;

        http.begin(client, serverURL);
        http.addHeader("Content-Type", "application/json");

        String jsonPayload = "{\"heart_rate\": " + String(hr) + 
                             ", \"spo2\": " + String(spo2) + 
                             ", \"timestamp\": \"" + timestamp + "\"}";

        int httpResponseCode = http.POST(jsonPayload);
        
        Serial.print("Server Response: ");
        Serial.println(httpResponseCode);

        http.end();
    } else {
        Serial.println("WiFi not connected, cannot send data.");
    }
}
