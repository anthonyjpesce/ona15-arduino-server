#include <Adafruit_CC3000.h>
#include <ccspi.h>
#include <SPI.h>
#include <string.h>

// These are the interrupt and control pins
#define ADAFRUIT_CC3000_IRQ   3  // MUST be an interrupt pin!
// These can be any two pins
#define ADAFRUIT_CC3000_VBAT  5
#define ADAFRUIT_CC3000_CS    10
// Use hardware SPI for the remaining pins
// On an UNO, SCK = 13, MISO = 12, and MOSI = 11
Adafruit_CC3000 cc3000 = Adafruit_CC3000(
    ADAFRUIT_CC3000_CS,
    ADAFRUIT_CC3000_IRQ,
    ADAFRUIT_CC3000_VBAT,
    SPI_CLOCK_DIVIDER
);

#define WLAN_SSID       "_ONA15" // wifi network name
#define WLAN_PASS       "onlinenews" // wifi network password
// Security can be WLAN_SEC_UNSEC, WLAN_SEC_WEP, WLAN_SEC_WPA or WLAN_SEC_WPA2
#define WLAN_SECURITY   WLAN_SEC_WPA2

const int sampleWindow = 1000; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;

const unsigned long
  dhcpTimeout     = 60L * 1000L, // Max time to wait for address from DHCP
  connectTimeout  = 15L * 1000L, // Max time to wait for server connection
  responseTimeout = 15L * 1000L; // Max time to wait for data from server
unsigned long
  currentTime = 0L;
Adafruit_CC3000_Client
  client;        // For WiFi connections

// Change the number after robot_id to the number for your robot
String postdata = "robot_id=1&volt=";

// We list IP here as a string for reference
// But we really want it as an integer
// You can use this site for Integer IP conversion:
// http://www.silisoftware.com/tools/ipconverter.php
char server[] = "52.26.235.236";
const uint32_t ip = 874179564;

void setup(void) {
  // TODO:
  // Don't think we need the ip variable here
  uint32_t ip = 0L, t;
  Serial.begin(9600);

  Serial.print(F("Hello! Initializing CC3000..."));
  if(!cc3000.begin()) hang(F("failed. Check your wiring?"));

  Serial.print(F("OK\r\nDeleting old connection profiles..."));
  if(!cc3000.deleteProfiles()) hang(F("failed."));

  Serial.print(F("OK\r\nConnecting to network..."));
  /* NOTE: Secure connections are not available in 'Tiny' mode! */
  if(!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) hang(F("Failed!"));

  Serial.print(F("OK\r\nRequesting address from DHCP server..."));
  for(t=millis(); !cc3000.checkDHCP() && ((millis() - t) < dhcpTimeout); delay(100));
  if(!cc3000.checkDHCP()) hang(F("failed"));
  Serial.println(F("OK"));

  while(!displayConnectionDetails());
}

void loop() {
    unsigned long startMillis= millis();  // Start of sample window
    unsigned int peakToPeak = 0;   // peak-to-peak level
    unsigned int signalMax = 0;
    unsigned int signalMin = 1024;
    unsigned long t = millis();

    // collect data every second
    while (millis() - startMillis < sampleWindow)
    {
      sample = analogRead(0);
      if (sample < 1024)  // toss out spurious readings
      {
         if (sample > signalMax)
         {
            signalMax = sample;  // save just the max levels
         }
         else if (sample < signalMin)
         {
            signalMin = sample;  // save just the min levels
         }
      }
    }

    peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude
    double volts = (peakToPeak * 3.3) / 1024;  // convert to volts

    Serial.print(F("OK\r\nConnecting to server..."));
    t = millis();
    do {
       client = cc3000.connectTCP(ip, 80);
    } while((!client.connected()) &&
          ((millis() - t) < connectTimeout));


   // If there's a successful connection, send the HTTP POST request
   if (client.connected()) {
     Serial.println("connecting...");

     client.println("POST /signal-submit/ HTTP/1.1");
     // EDIT: 'Host' to match your domain
     client.println("Host: 192.168.0.6");
     client.println("User-Agent: Arduino/1.0");
     client.println("Connection: close");
     client.println("Content-Type: application/x-www-form-urlencoded;charset=utf-8");
     client.print("Content-Length: ");
     client.println(postdata.length() + 3);
     client.println();
     client.print(postdata);
     client.print(volts);
   }
   else {
     // If you couldn't make a connection:
     Serial.println("Connection failed");
     Serial.println("Disconnecting.");
     client.stop();
   }


   Serial.println(volts);
}

// On error, print PROGMEM string to serial monitor and stop
void hang(const __FlashStringHelper *str) {
  Serial.println(str);
  for(;;);
}

bool displayConnectionDetails(void) {
  uint32_t addr, netmask, gateway, dhcpserv, dnsserv;

  if(!cc3000.getIPAddress(&addr, &netmask, &gateway, &dhcpserv, &dnsserv))
    return false;

  Serial.print(F("IP Addr: ")); cc3000.printIPdotsRev(addr);
  Serial.print(F("\r\nNetmask: ")); cc3000.printIPdotsRev(netmask);
  Serial.print(F("\r\nGateway: ")); cc3000.printIPdotsRev(gateway);
  Serial.print(F("\r\nDHCPsrv: ")); cc3000.printIPdotsRev(dhcpserv);
  Serial.print(F("\r\nDNSserv: ")); cc3000.printIPdotsRev(dnsserv);
  Serial.println();
  return true;
}
