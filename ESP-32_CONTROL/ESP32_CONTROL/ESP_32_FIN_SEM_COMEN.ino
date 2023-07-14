#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>

const int motorb_pwm = 27; // PWM do Motor B é a potencia/velocidade do motor

int in1 = 12; //controla a direção do motor A (ir pra frente ou tras) 
int in2 = 14;
int in3 = 25;
int in4 = 33;  //controla a direção do motor  B(ir pra frente ou tras) 

const int motorA_pwm = 13; // PWM do Motor A é a potencia/velocidade do motor


const int echo=18;   //pins do sensor de proximidade e do led que acende quando o sensor estiver muito perto

const int trigger=5;
const int LED =2 ;

int duration; // variaveis para o calculo da distancia pelo sensor
int distance;

const int motorb_pwmChannel = 0; //seta os canais de PWM do ESP32
const int motorA_pwmChannel = 1;

bool parada_emerg = false; //variaveis de parada, emerg = parada temporaria pelo sensor
bool parada_SEMPRE = false; //para o ESP32 completamenta, parada por request HTTP

// variavel da velocidade do carro
int drivePower = 500;

const char* ssid = "iPhone de João Pedro (2)"; //"iPhone de João Pedro (2)"
const char* password = "jp123456";          //"jp123456"iPhone (8) 





//determina a velocidade com que o carro faz curvas 
// Pode ser ajustado entre 0 e 1023 (o carro provavelmente não vai fazer curvas se o valor for muito baixo), 
int steeringPower = 500;



WebServer server(80);


void handleNotFound(){
  server.send(404, "text/plain", "Error: Not found");
}

int sensor() {
digitalWrite(trigger, LOW); 
delayMicroseconds(2);

digitalWrite(trigger, HIGH);  // Manda um trigger que manda um sinal sonico
delayMicroseconds(10);            // espera 10 milisegundos
digitalWrite(trigger, LOW);   // para de mandar o sinal

// faz contas com a duração do echo para determinar a distancia
duration = pulseIn(echo, HIGH); 
distance= duration*0.034/2; //converte o tempo/duração do echo na distancia

/* if distance greater than 10cm, turn on LED */
if ( distance < 10){
digitalWrite(LED, HIGH);
parada_emerg = true;
return 1; } else {
digitalWrite(LED, LOW);
parada_emerg = false;
// print measured distance value on Arduino serial monitor
Serial.print("Distance: ");
Serial.print(distance);
Serial.println(" cm");
delay(400);
return 0;
}

}




void setup(void){

  pinMode(motorb_pwm, OUTPUT);
  pinMode(motorA_pwm, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(trigger, OUTPUT);
  pinMode(LED, OUTPUT); 
  pinMode(echo, INPUT); 



 // Configurar canais PWM, com uma resolução de 8 bits.
  ledcSetup(0, 5000, 8);
  ledcSetup(1, 5000, 8);
  ledcAttachPin(motorb_pwm, 0);
  ledcAttachPin(motorA_pwm, 1);

    Serial.begin(115200);


 WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(700);
    Serial.print(".");
      //Serial.println(WiFi.status()); 
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


  if (MDNS.begin("WifiCar")) {
    Serial.println("MDNS Responder Started");
  }
 server.on("/para", [](){
  parada_emerg = true;
  server.send(200, "text/plain", "Stopped");
  parada_SEMPRE = true;
     ledcWrite(motorb_pwmChannel, 0);
    ledcWrite(motorA_pwmChannel, 0); 
  return;
   }); 


server.on("/frente", [](){
   Serial.println("para frente");

   if (parada_emerg) {
     server.send(200, "text/plain", "parada_emergencia");
     return;
   }
   int MotorB_Power = drivePower;

   if(!parada_emerg){
    ledcWrite(motorb_pwmChannel, MotorB_Power);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    ledcWrite(motorA_pwmChannel, steeringPower);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);  
    server.send(200, "text/plain", "frente");
   }
});


  server.on("/tras", [](){

    Serial.println("tras");

  if(!parada_emerg){
    ledcWrite(motorb_pwmChannel, drivePower);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
    ledcWrite(motorA_pwmChannel, steeringPower);
     digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH); 
        server.send(200, "text/plain", "tras");
      }



  });



  server.on("/esque", [](){
    Serial.println("dir");
  if(!parada_emerg){
    unsigned long startTimeES = millis();
    while (millis() - startTimeES < 300) { 

    ledcWrite(motorA_pwmChannel, steeringPower);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    ledcWrite(motorb_pwmChannel, drivePower);
     digitalWrite(in3, LOW);
     digitalWrite(in4, LOW);   

      } 
       ledcWrite(motorA_pwmChannel, 0);
       ledcWrite(motorb_pwmChannel, 0);
      server.send(200, "text/plain", "direita");

  }

  });





  server.on("/dir", [](){   
    Serial.println("esque");

     if(!parada_emerg){
      unsigned long startTimeDI = millis();
    while (millis() - startTimeDI < 300){
    ledcWrite(motorA_pwmChannel, steeringPower);
     digitalWrite(in1, LOW);
     digitalWrite(in2, LOW);
    ledcWrite(motorb_pwmChannel, drivePower);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);   

     }
      ledcWrite(motorA_pwmChannel, 0);
    ledcWrite(motorb_pwmChannel, 0);
   server.send(200, "text/plain", "esquerda");

    }
  });




  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP Server Started");


}




void loop() {

  server.handleClient();
 int para = sensor();
 if (para == 1){
    ledcWrite(motorb_pwmChannel, 0);
    ledcWrite(motorA_pwmChannel, 0); 
   parada_emerg = true;
 }

 if (parada_SEMPRE) {

    ledcWrite(motorb_pwmChannel, 0);
    ledcWrite(motorA_pwmChannel, 0); 
    esp_deep_sleep_start(); 

  } 


  delay(15);
}