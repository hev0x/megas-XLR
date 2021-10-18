#include <EtherCard.h>
#include <avr/wdt.h>

static byte myip[] = { 
  192,168,0,74 };
static byte gwip[] = { 
  192,168,0,1 };
static byte mymac[] = { 
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

byte Ethernet::buffer[500];

#define NUM 11

const int digital = 2;
const int analog0 = A0;
const int analog1 = A1;
const int analog2 = A2;
const int analog3 = A3;
const int analog4 = A4;
const int analog5 = A5;

boolean ready = false;
unsigned int timer = 0;
unsigned int lastTime = 0;
int values[NUM] = {};
int analog0q[NUM] = {};
int analog1q[NUM] = {};
int analog2q[NUM] = {};
int analog3q[NUM] = {};
int analog4q[NUM] = {};
int analog5q[NUM] = {};

int digitalI = 0;
int lastDigitalI = 0;
int analogI = 0;
int lastAnalogI = 0;
String result;
char Buffer[36];


void setup() {
  ether.begin(sizeof Ethernet::buffer, mymac, 10);
  ether.staticSetup(myip, gwip);
  //Serial.begin(9600);
  attachInterrupt(0, triggerSPM, RISING);
  pinMode(digital, INPUT);
  digitalWrite(digital, LOW);
  wdt_enable(WDTO_500MS);
}

void loop(){
  wdt_reset();
  if (ready) {
    getValues();
   // Serial.println(result);
    ready = false;
  }
  refresh();

   word len = ether.packetReceive();
   word pos = ether.packetLoop(len);
   
   if(pos) {
     BufferFiller bfill = ether.tcpOffset();
     result.toCharArray(Buffer, 36); // Testar linha de envio de dados
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

void triggerSPM() {
  values[digitalI]++;
}

void refresh() {
  timer = millis();

  if(timer - lastTime > 250) {
    lastTime = timer;
    ready = true;
  }

  if (digitalI != lastDigitalI) {
    values[digitalI] = 0;
  }

  if (analogI != lastAnalogI) {
    analog0q[analogI] = analogRead(analog0);
    analog1q[analogI] = analogRead(analog1);
    analog2q[analogI] = analogRead(analog2);
    analog3q[analogI] = analogRead(analog3);
    analog4q[analogI] = analogRead(analog4);
    analog5q[analogI] = analogRead(analog5); //novo canal adicionado
}

  lastDigitalI = digitalI;
  digitalI = ((timer/1000)%NUM);
  lastAnalogI = analogI;
  analogI = ((timer/25)%NUM);
}

void getValues() {
  unsigned int digital, out1, out2, out3, out4, out5, out6;
  digital = out1 = out2 = out3 = out4 = out5 = out6 = 0;
  for (int i = 0; i < NUM; i++) {
    if (i != digitalI) {
      digital += values[i];
    }
    out1 += analog0q[i]; 
    out2 += analog1q[i]; 
    out3 += analog2q[i]; 
    out4 += analog3q[i];
    out5 += analog4q[i];
    out6 += analog5q[i]; 
  }
  out1 = out1/NUM;
  out2 = out2/NUM;
  out3 = out3/NUM;
  out4 = out4/NUM;
  out5 = out5/NUM;
  out6 = out6/NUM;
  
   digital = (digital/((NUM-1)*1.00))*60.00;
   
   result = "";
   result += digital;
   result += "|";
   result += out1;
   result += "|";
   result += out2;
   result += "|";
   result += out3;
   result += "|";
   result += out4;
   result += "|";
   result += out5;
   result += "|";
   result += out6;
}

