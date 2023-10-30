#include <WiFi.h>
#include <WiFiUdp.h>

const char *ssid = "House323";
const char *password = "kerala123";
const int udpPort = 12345;

WiFiUDP udp;

const int numLeds = 10;
int ledPins[numLeds] = {2, 4, 5, 12, 13, 14, 15, 16, 17, 18};
int currentLed = 0;

void setup()
{
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize UDP
  udp.begin(udpPort);

  // Set LED pins as OUTPUT
  for (int i = 0; i < numLeds; i++)
  {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop()
{
  int packetSize = udp.parsePacket();
  if (packetSize)
  {
    char incomingPacket[255];
    udp.read(incomingPacket, packetSize);
    incomingPacket[packetSize] = 0;

    int value = atoi(incomingPacket);
    Serial.print("Received value: ");
    Serial.println(value);

    // Turn off all LEDs
    for (int i = 0; i < numLeds; i++)
    {
      digitalWrite(ledPins[i], LOW);
    }

    // Turn on the corresponding LED
    if (value >= 0 && value < numLeds)
    {
      digitalWrite(ledPins[value], HIGH);
    }

    // Wait for 10 seconds
    delay(10000);

    // Turn off all LEDs
    for (int i = 0; i < numLeds; i++)
    {
      digitalWrite(ledPins[i], LOW);
    }
  }
}
