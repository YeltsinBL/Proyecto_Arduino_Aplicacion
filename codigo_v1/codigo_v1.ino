#include <Servo.h>

Servo myservo;

int pinservo=9;
int angulo = 90;
int carril=0;

/**botones*/
int pulsador1=6;
int led1=11;
int pulsador2=7;
int led2=10;
int estado_pulsador1=0;
int estado_pulsador2=0;

/**sensor de humedad*/
const int Airvalue = 472;
const int WaterValue = 250;
int soilMoistureValue = 0;
int soilmoisturepercent=0;

/**Controlar el inicio y apagado del sistema*/
//bool stringComplete=true;
String inputString ="apagado";
int iniciar=0;
const long interval = 2500; // tiempo a enviar
unsigned long previousMillis = 0;  // Tiempo anterior 0

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);

  pinMode(led1,INPUT);
  pinMode(led2,INPUT);

  myservo.attach(pinservo);
  previousMillis = millis(); 
}

void loop() {
  //Serial.println("stringComplete:" + stringComplete);
  //if(stringComplete){
    // if (millis() - previousMillis >= interval) {
       //Serial.println("inputString:" + inputString.substring(0,1));
    // }
    if(inputString.substring(0,1)=="a"){
      //Serial.println("Apagado");
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      angulo = 90;
      myservo.write(angulo); 
    }
    if(inputString.substring(0,1)=="e"){
      //Serial.println("Encendido");
      //botones();
      // digitalWrite(led2, HIGH);
      // digitalWrite(led1, LOW);
      angulo=0;
      inputString = "i";      
      myservo.write(angulo); 
      // if (millis() - previousMillis >= interval) {
      //   Serial.println("Entro E");
      //   previousMillis = millis();
      //   sensorHumerdad();
      // }
    }
    if(inputString.substring(0,1)=="i"){
      digitalWrite(led2, HIGH);
      digitalWrite(led1, LOW);
      angulo=0;
      carril=0;
      myservo.write(angulo); 
      if (millis() - previousMillis >= interval) {
        //Serial.println("Entro I");
        previousMillis = millis();
        sensorHumerdad();
      }
      //botones();
    }
    if(inputString.substring(0,1)=="d"){
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
      angulo=180;
      carril=1;
      myservo.write(angulo); 
      if (millis() - previousMillis >= interval) { 
        //Serial.println("Entro D");
        previousMillis = millis();   
        sensorHumerdad();
      }
      //botones();
    }
    
      botones();
  //}
  //delay (1000) ;
}
void sensorHumerdad(){
  soilMoistureValue = analogRead (A0);
  soilmoisturepercent = map (soilMoistureValue, Airvalue, WaterValue, 0, 100);
   if (soilmoisturepercent >= 100){
   Serial.println("100");

   }
   else if (soilmoisturepercent <=0){
   Serial.println("0");
   }
   else if (soilmoisturepercent >0 && soilmoisturepercent < 100){
   Serial.println(soilmoisturepercent);
  }
  //delay (1000) ;
}
void botones(){
  estado_pulsador1=digitalRead(pulsador1);
  estado_pulsador2=digitalRead(pulsador2);
  if(estado_pulsador1==HIGH){
    Serial.println("d");
    angulo=180;
    carril=1;
    digitalWrite(led1, HIGH);
    digitalWrite(led2, LOW);
    inputString = "d";
    myservo.write(angulo);
    if (millis() - previousMillis >= interval) {
      //Serial.println("Entro Boton");
      previousMillis = millis();
      sensorHumerdad();
    }
  }
  if(estado_pulsador2==HIGH){
    Serial.println("i");
    angulo=0;
    carril=0;
    digitalWrite(led2, HIGH);
    digitalWrite(led1, LOW);
    inputString = "i";
    myservo.write(angulo);
    if (millis() - previousMillis >= interval) {
      //Serial.println("Entro Boton");
      previousMillis = millis();
      sensorHumerdad();
    }
  }
  // else
  // if(carril==0){
  //   digitalWrite(led2, HIGH);
  //   digitalWrite(led1, LOW);
  //   angulo=0;
  //   inputString = "i";
  // }
  // else{
  //   digitalWrite(led1, HIGH);
  //   digitalWrite(led2, LOW);
  //   //angulo=180;
  //   //Serial.println("Derecha");
  // }
  // myservo.write(angulo); 
  
  // if (millis() - previousMillis >= interval) { 
  //   Serial.println("Entro Boton");
  //   previousMillis = millis();   
  //   sensorHumerdad();
  // }
}
void serialEvent() {
 // Verificar una a una el caractrer de los datos ingresados
  inputString ="";
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString = inputString + inChar;
    //Serial.println("Valor: "+inputString);
  }
}