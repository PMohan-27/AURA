#include <Arduino.h>
#include "wifi.hpp"

void setup(){
    Serial.begin(115200);
    delay(1000);
    Serial.println("Beginning wifi initialization...");
    init_Wifi();
    Serial.println("Wifi initialization complete!");
}

void loop(){
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