#include <SoftwareSerial.h>
SoftwareSerial TWE(5, 6); // RX, TX

#define ANALOGPIN_Light 0
#define ANALOGPIN_Humid 4

int humidity = 0;
int lightIntencity = 0;

void setup() {
  TWE.begin(38400);
  Serial.begin(38400);
}

void loop() {
  /*if (Serial.read() == '1') {*/
    lightIntencity = analogRead(ANALOGPIN_Light);
    humidity = analogRead(ANALOGPIN_Humid);

    if (isnan(humidity)) {
      Serial.println("Failed to read from YL_69!");
      return;
    }
    else if (isnan(lightIntencity)) {
      Serial.println("Failed to read from Photo Diode!");
      return;
    }

    Serial.print(humidity);
    Serial.print(" ");
    Serial.println(lightIntencity);

    for (byte i = 0 ; i < 5 ; ++i) {
      send(humidity, 0);
      delay(200);
    }
    for (byte i = 0 ; i < 5 ; ++i) {
      send(lightIntencity, 1);
      delay(200);
    }
 /* }*/
}

void send(int num,int val) {
  /* 桁数を計算 */
  int numlength = num;
  int digit = 0;
  while (numlength != 0) {
    numlength /= 10;
    ++digit;
  }

  /* 偶数長charに変換 */
  char str[10] = {0};
  if (digit % 2) {
    /* こうしたかったがコンパイルが通らない
    if(val == 0){
      sprintf(str, "%dE", num);
    }
    else{
      sprintf(str, "%dF", num);
    }*/
    /* のでこのまま */
    sprintf(str, "%dF", num);
    ++digit;
  }
  else {
    /*if(val == 0){
      sprintf(str, "%dEE", num);
    }
    else{
      sprintf(str, "%dFF", num);
    }*/
    sprintf(str, "%dFF", num);
    digit += 2;
  }

  /* 送信データに格納 */
  int DATA_SIZE = 8 + digit;
  char DATA[DATA_SIZE] = {0};
  sprintf(DATA, ":7800%sX\r\n", str);

  Serial.println(DATA);
  
  for (byte i = 0 ; i < DATA_SIZE ; i++) TWE.write((byte)DATA[i]);
}
