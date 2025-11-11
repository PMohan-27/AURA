#include "main.cpp"
#include <WiFi.h>

// Replace with your network credentials
const char* ssid     = "your_wifi_ssid";
const char* password = "your_wifi_password";

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("Connecting to WiFi...");

  // Start connecting
  WiFi.begin(ssid, password);

  // Wait until connected
  int retryCount = 0;
  while (WiFi.status() != WL_CONNECTED && retryCount < 20) {
    delay(500);
    Serial.print(".");
    retryCount++;
  }

  Serial.println();

  // Check connection result
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

void loop() {
  // Keep checking WiFi status
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected! Reconnecting...");
    WiFi.reconnect();
    delay(5000);
  } else {
    Serial.print("WiFi connected, IP: ");
    Serial.println(WiFi.localIP());
    delay(10000);
  }
}
