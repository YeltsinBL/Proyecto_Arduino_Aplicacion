#include <Servo.h>

Servo myservo;

int pinservo=9;
int angulo = 90;
int pulsador1=6;
int led1=11;
int pulsador2=7;
int led2=10;
int estado_pulsador1=0;
int estado_pulsador2=0;
int carril=0;

/**sensor de humedad*/
const int Airvalue = 472;
const int WaterValue = 250;
int soilMoistureValue = 0;
int soilmoisturepercent=0;

/**Controlar el inicio y apagado del sistema*/
bool stringComplete=true;
String inputString ="apagado";
int iniciar=0;

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);

  pinMode(led1,INPUT);
  pinMode(led2,INPUT);
  myservo.attach(pinservo);
}

void loop() {
  //Serial.println("stringComplete:" + stringComplete);
  if(stringComplete){
    //Serial.println("inputString:" + inputString);
    if(inputString.substring(0,1)=="a"){
      //Serial.println("Apagado");
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      angulo = 90;
      myservo.write(angulo); 
    }
    if(inputString.substring(0,1)=="e"){
      //Serial.println("Encendido");
      estado_pulsador1=digitalRead(pulsador1);
      estado_pulsador2=digitalRead(pulsador2);
      if(estado_pulsador1==HIGH){
        angulo=180;
        carril=1;
        Serial.println("d");
      }
      if(estado_pulsador2==HIGH){
        angulo=0;
        carril=0;
        Serial.println("i");
      }
      if(carril==0){
        digitalWrite(led2, HIGH);
        digitalWrite(led1, LOW);
        angulo=0;
        //Serial.println("Izquierda");
      }else{
        digitalWrite(led1, HIGH);
        digitalWrite(led2, LOW);
        angulo=180;
        //Serial.println("Derecha");
      }
      myservo.write(angulo); 
      sensorHumerdad();
    }
    if(inputString.substring(0,1)=="i"){
      digitalWrite(led2, HIGH);
      digitalWrite(led1, LOW);
      angulo=0;
      carril=0;
      myservo.write(angulo); 
      sensorHumerdad();
    }
    if(inputString.substring(0,1)=="d"){
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
      angulo=180;
      carril=1;
      myservo.write(angulo); 
      sensorHumerdad();
    }
  }
  delay (1000) ;
}
void sensorHumerdad(){
  soilMoistureValue = analogRead (A0) ;
  Serial.println (soilMoistureValue) ;
  soilmoisturepercent = map (soilMoistureValue, Airvalue, WaterValue, 0, 100);
  // if (soilmoisturepercent < 40) // change this at what level the pump turns on
  // {
  // Serial.println ("seco, Pump turning on");

  // }
  // else if (soilmoisturepercent > 50) // max water level should be
  // {
  // Serial.println("mojado, Pump turning off");

  // }
  //  if (soilmoisturepercent >= 100){
  //  Serial.println("100");

  //  }
  //  else if (soilmoisturepercent <=0){
  //  Serial.println("0");

  //  }
  //  else if (soilmoisturepercent >0 && soilmoisturepercent < 100){
  //  Serial.println(soilmoisturepercent);
  // Serial.println("%");
  // }
  delay (1000) ;
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