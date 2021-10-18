#include <Encoder.h>
#include <EtherCard.h>
#include <avr/pgmspace.h>

#define NUM_MUX_PORTS 8
#define TOTAL_ANALOG_PORTS 13
#define NUM_DIGITAL_PORTS 5
#define DIGITAL_ARRAY_COLS 5

static byte myip[] = { 192,168,0,74 };
static byte gwip[] = { 192,168,0,1 };
static byte mymac[] = { 0x74,0x69,0x69,0x2D,0x30,0x31 };
byte Ethernet::buffer[500];

const int muxAnalogChannel = A0;
const int muxChannels[] = {2, 3, 4};
const int analogChannels[] = {A1, A2, A3, A4, A5};
const int digitalChannels[] = {0, 1, 7, 8, 9};
Encoder encoder(5, 6);


unsigned int analogValues[TOTAL_ANALOG_PORTS];

//#############

unsigned int digitalValues[NUM_DIGITAL_PORTS][DIGITAL_ARRAY_COLS];
uint8_t portStates[NUM_DIGITAL_PORTS];
uint8_t colPointer = 0;
unsigned int colPointerTimer = 0;

//#############

unsigned int altura = 0;
String result;
char Buffer[256];
int data = 0;
int pos = 0;
int maskI = 0;


boolean ready = false;
unsigned int timer = 0;
unsigned int lastTime = 0;

void setup() {
  //Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    pinMode(muxChannels[i], OUTPUT);
  }
  for (int i = 0; i < 3; i++) {
    pinMode(digitalChannels[i], OUTPUT);
    digitalWrite(digitalChannels[i], LOW);
  }
  ether.begin(sizeof Ethernet::buffer, mymac, 10);
  ether.staticSetup(myip, gwip);
}

void loop(){
  altura = encoder.read();
/*  if (ready) {
    getValues();
    Serial.println(result);
    ready = false;
  }*/
  refresh();

   word len = ether.packetReceive();
   word pos = ether.packetLoop(len);
   
   if(pos) {
     BufferFiller bfill = ether.tcpOffset();
     getValues();
     result.toCharArray(Buffer, 256);
     bfill.emit_p(PSTR(
     "HTTP/1.0 200 OK\r\n"
     "Content-Type: text/html\r\n"
     "Pragma: no-cache\r\n"
     "\r\n"
     "$S"),
     Buffer);
     ether.httpServerReply(bfill.position());
   }
}

void refresh() {
/*  timer = millis();
  
  if(timer - lastTime > 250) {
    lastTime = timer;
    ready = true;
  }*/
  
  if (millis()-colPointerTimer >= 1000) {
    colPointer++;
    for (int i = 0; i < NUM_DIGITAL_PORTS; i++) {
      digitalValues[i][colPointer] = 0;
    }
  }
    
  for (int i = 0; i < NUM_DIGITAL_PORTS; i++) {
    if (digitalRead(digitalChannels[i]) != portStates[i] && digitalRead(digitalChannels[i]) == HIGH) {
      digitalValues[i][colPointer]++;
    }
  }

  for (pos = 0; pos < TOTAL_ANALOG_PORTS; pos++) {
    if (pos < NUM_MUX_PORTS) {
      data = pos;
      for (maskI = 2; maskI >= 0; maskI--) {
        if (1 & data){
          digitalWrite(muxChannels[maskI], HIGH);
        } else {
          digitalWrite(muxChannels[maskI], LOW);
        }
        data >>= 1;
      }
      analogValues[pos] = analogRead(A0);
    } else {
      analogValues[pos] = analogRead(analogChannels[(pos-NUM_MUX_PORTS)]);
    }
  }
}

void getValues() {
   result = "{\"a\":[";
   for (int i = 0; i < TOTAL_ANALOG_PORTS; i++) {
       result += analogValues[i];
       if ((i+1) != TOTAL_ANALOG_PORTS) {
         result += ",";
       }
   }
   result += "],\"f\":[";
   unsigned int tmp = 0;
   
   for (int i = 0; i < NUM_DIGITAL_PORTS; i++) {
     tmp = 0;
     for (int c = 0; c < DIGITAL_ARRAY_COLS; c++) {
       tmp = tmp + digitalValues[i][c];
     }
     result += tmp;
     if ((i+1) != NUM_DIGITAL_PORTS) {
       result += ",";
     }
   }
   result += "],\"e\":";
   result += altura;
   result += "]}";
   
}

