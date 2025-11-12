#include <Arduino.h>
#include <WiFi.h>
#include "wifi.hpp"


const char* ssid     = "your_wifi_ssid";
const char* password = "your_wifi_password";

void init_Wifi() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("Connecting to WiFi...");

  
  WiFi.begin(ssid, password);

  
  int retryCount = 0;
  while (WiFi.status() != WL_CONNECTED && retryCount < 20) {
    delay(500);
    Serial.print(".");
    retryCount++;
  }

  Serial.println();

  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected successfully!");
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Failed to connect to WiFi.");
  }
}

