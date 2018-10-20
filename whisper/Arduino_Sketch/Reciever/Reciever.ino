#include <SoftwareSerial.h>
SoftwareSerial TWE(5, 6); // RX, TX
#define LED 13
 
 
void setup() {
  TWE.begin(38400);
  Serial.begin(38400);
  pinMode(LED, OUTPUT);
}
 
 
void loop() {
  byte recv [60] = {};
  byte count     = 0;
 
  //receive data
  while (TWE.available())
  {
    digitalWrite(LED, HIGH);
    recv [count] = TWE.read();
    count++;
  }

  /*Serial.println((char)recv);*/
 
  if (count > 0)
  {
    char DATA[20] = {0};
    int datalength = 0;

    if(count <= 20 && recv[4] == '0'){
      for(byte i = 5 ; i < count ; ++i){
        if(recv[i] == 'F') break;
        DATA[datalength] = recv[i];
        ++datalength;
      } 
    Serial.println(DATA);
    }
  }

  /*if (count > 0)
  {
    byte space [] = {1, 3, 5, 7, 9, 11, 19, 21, 25, 27, 31, 33, 35, 37, 47, 49};
    byte add      = 0;
    for (byte i = 0 ; i < count ; i++)
    {
      if (i == space[add])
      {
        Serial.print(" ");
        add++;
      }
 
      if (recv[i] == ':')
      {
        Serial.print(':');
      } else if (recv[i] == 13) {
        Serial.print(13, HEX);
      } else if (recv[i] == 10) {
        Serial.println(10, HEX);
      } else {
        if (recv[i] <= '9') recv[i] = recv[i] - '0';
        else if (recv[i] <= 'F') recv[i] = recv[i] - 'A' + 10;
 
        Serial.print(recv[i], HEX);
      }
    }
  }*/
  digitalWrite(LED, LOW);
}
