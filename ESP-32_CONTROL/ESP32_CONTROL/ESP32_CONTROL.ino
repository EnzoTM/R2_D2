#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>

const int motorb_pwm = 12; // PWM do Motor B é a potencia/velocidade do motor

int in1 = 14; //controla a direção do motor A (ir pra frente ou tras) 
int in2 = 27;
int in3 = 26;
int in4 = 25;  //controla a direção do motor  B(ir pra frente ou tras) 

const int motorA_pwm = 13; // PWM do Motor A é a potencia/velocidade do motor


const int motorb_pwmChannel = 0; //seta os canais de PWM do ESP32
const int motorA_pwmChannel = 1;


const int sensor_pin = 30;  //pin do sensor de proximidade

bool parada_emerg = false;

// variavel da velocidade do carro
int drivePower = 600;

const char* ssid = "R2D2";
const char* password = "R21234";


//A variavel "driveDirection" define em que direção o carro se move 
// Se o carro estiver fazendo curvas para a direita quando você pressiona o botão esquerdo, altere isso para LOW
//uint8_t driveDirection = HIGH;


//determina a velocidade com que o carro faz curvas 
// Pode ser ajustado entre 0 e 1023 (o carro provavelmente não vai fazer curvas se o valor for muito baixo), 
int steeringPower = 600;

//define em que direção o carro faz curvas
// Se o carro estiver se movendo para trás quando você pressiona o botão de avanço, altere isso para LOW
//uint8_t steerDirection = HIGH;

WebServer server(80);


void handleNotFound(){
  server.send(404, "text/plain", "Error: Not found");
}

// void verifica_sensor() {
//   int maximo = 10;
//   int dados_sensor = analogRead(sensor_pin); 
  
//   if (dados_sensor> maximo) {
//     parada_emerg = true;
//   } else {
//     parada_emerg = false;
//   }
// }




void setup(void){

  pinMode(motorb_pwm, OUTPUT);
  pinMode(motorA_pwm, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);


 // Configurar canais PWM, com uma resolução de 8 bits.
  ledcSetup(0, 5000, 8);
  ledcSetup(1, 5000, 8);
  ledcAttachPin(motorb_pwm, 0);
  ledcAttachPin(motorA_pwm, 1);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");


  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("WifiCar")) {
    Serial.println("MDNS Responder Started");
  }


   server.on("/frente", [](){
       Serial.println("para frente");
     if (parada_emerg) {
     server.send(200, "text/plain", "parada_emergencia");
     return;
  }

    ledcWrite(motorb_pwmChannel, drivePower);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    ledcWrite(motorA_pwmChannel, steeringPower);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);  
    server.send(200, "text/plain", "frente");
  });


  server.on("/tras", [](){
    Serial.println("tras");
    ledcWrite(motorb_pwmChannel, drivePower);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
    ledcWrite(motorA_pwmChannel, steeringPower);
     digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
    server.send(200, "text/plain", "tras");
  });

  server.on("/dir", [](){
    Serial.println("dir");
    ledcWrite(motorA_pwmChannel, steeringPower);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    ledcWrite(motorb_pwmChannel, drivePower);
     digitalWrite(in3, LOW);
     digitalWrite(in4, LOW);   
    server.send(200, "text/plain", "direita");
  });

  server.on("/esque", [](){
    Serial.println("esque");
    ledcWrite(motorA_pwmChannel, steeringPower);
     digitalWrite(in1, LOW);
     digitalWrite(in2, LOW);
    ledcWrite(motorb_pwmChannel, drivePower);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);   
    server.send(200, "text/plain", "esquerda");
  });



  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP Server Started");

  
}




void loop() {
 server.handleClient();
// verifica_sensor();

}
