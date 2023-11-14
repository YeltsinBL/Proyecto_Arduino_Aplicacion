#include <Servo.h>

#include "DHT.h"      // Incluimos las librerías para poder programar el sensor DHT
#include "DHT_U.h"

/**Mayra**/
int sensor = 31;    // Escogemos el pin 31 y lo llamaremos "sensor"
float temperatura=0.0;  // Creamos una variable "temperatura" la cual será de un valor flotante (decimales)
DHT dht(sensor,DHT11);  // Mediante este argumento le decimos a la librería DHT que usaremos el DHT11 y ese será nuestra entrada digital "sensor"
int cooler = 41;    // Escogemos el pin 41 y lo llamaremos "cooler"
int foco = 51;      // Escogemos el pin 51 y lo llamaremos "foco"


/**Sheyla**/
Servo myservo;
int two =2;
int three=3;
int tiempo;
int distancia;
int pinservo=4;
//int angulo = 90;

/**Adrian**/
int bomba=7;

//int carril=0;

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

/**PRUEBA**/
//double temperatura=0;
double humedad=0;

void setup() {
  Serial.begin(115200);
  //Serial.begin(9600);
  inputString.reserve(200);

  pinMode(led1,INPUT);
  pinMode(led2,INPUT);

  /**Sheyla**/
  pinMode(two,OUTPUT);
  pinMode(three, INPUT);
  myservo.attach(pinservo);

  /**Adrian**/
  pinMode(bomba,OUTPUT); /* Declaramos Pin #7 como salida */

  /**Mayra**/
  dht.begin();    // Con esta linea de código inicializaremos el sensor DHT11
  pinMode(sensor, INPUT);   // Configuración de pines, el pin sensor será una entrada digital
  pinMode(cooler, OUTPUT);  // El pin cooler será una salida digital
  pinMode(foco, OUTPUT);    // El pin foco será también una salida digital

  previousMillis = millis(); 
}

void loop() {
  puerta();
  //Serial.println("stringComplete:" + stringComplete);
  //if(stringComplete){
    // if (millis() - previousMillis >= interval) {
       //Serial.println("inputString:" + inputString.substring(0,1));
    // }
    if(inputString.substring(0,1)=="a"){
      //Serial.println("Apagado");
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      //angulo = 0;
      //myservo.write(angulo); 
    }
    // if(inputString.substring(0,1)=="e"){
    //   //Serial.println("Encendido");
    //   //botones();
    //   // digitalWrite(led2, HIGH);
    //   // digitalWrite(led1, LOW);
    //   angulo=0;
    //   //inputString = "i";      
    //   myservo.write(angulo); 
    //   // if (millis() - previousMillis >= interval) {
    //   //   Serial.println("Entro E");
    //   //   previousMillis = millis();
    //   //   sensorHumerdad();
    //   // }
    // }
    if(inputString.substring(0,1)=="e"){
      digitalWrite(led2, HIGH);
      digitalWrite(led1, LOW);
      //angulo=180;
      //carril=0;
      //myservo.write(angulo); 
      if (millis() - previousMillis >= interval) {
        //Serial.println("Entro I");
        previousMillis = millis();
        //puerta();
        sensortemperatura();
        sensorHumerdad();
      }
      //botones();
    }
    if(inputString.substring(0,1)=="d"){
      //digitalWrite(led1, LOW);
      //digitalWrite(led2, LOW);
      //temperatura = 0;
      //humedad = 0;
      //angulo=0;
      //carril=1;
      // myservo.write(angulo); 
      if (millis() - previousMillis >= interval) { 
      //   //Serial.println("Entro D");
        previousMillis = millis();   
      //   sensorHumerdad();
      }
      //botones();
      //humedad=0;
      //temperatura=0;
    }
    
      //botones();
  //}
  //delay (1000) ;
}
void sensorHumerdad(){
  soilMoistureValue = analogRead (A0);
  soilmoisturepercent = map (soilMoistureValue, Airvalue, WaterValue, 0, 100);
   if (soilmoisturepercent >= 100){
   //Serial.println("100");
    humedad= 100;
   }
   else if (soilmoisturepercent <=0){
   //Serial.println("0");
   humedad= 0;
   }
   else if (soilmoisturepercent >0 && soilmoisturepercent < 100){
   //Serial.println(soilmoisturepercent);
   humedad= soilmoisturepercent;
  }
  // //delay (1000) ;
  // temperatura= temperatura + 0.5;
  // if(temperatura>100){
  //   temperatura=0;
  // }
  // humedad= humedad - 0.5;
  // if(humedad==0){
  //   humedad=100;
  // }

  /**Adrian**/
  if (humedad>=100)  /* Agreagamos una condicion de funcionamiento en base a las lecturas*/
  {
    digitalWrite(bomba, LOW); /* Si se cumple la condicion la salida se desactiva, estado bajo */
  }
  else
  {
    digitalWrite(bomba, HIGH); /* Si no se cumple la condicion la salida se activa, estado alto */
  }

  Serial.println(String(temperatura) +","+ String(humedad));
  //Serial.println("Temperatura:"+String(temperatura) +"," +"Humedad:"+ String(humedad));
  //Serial.println(temperatura+(0.01*humedad));
  //Serial.print(temperatura);
  //Serial.print(',');
  //Serial.println(humedad);
}
void botones(){
  estado_pulsador1=digitalRead(pulsador1);
  estado_pulsador2=digitalRead(pulsador2);
  if(estado_pulsador1==HIGH){
    Serial.println("d");
    //angulo=180;
    //carril=1;
    digitalWrite(led1, HIGH);
    digitalWrite(led2, LOW);
    inputString = "d";
    //myservo.write(angulo);
    if (millis() - previousMillis >= interval) {
      //Serial.println("Entro Boton");
      previousMillis = millis();
      sensorHumerdad();
    }
  }
  if(estado_pulsador2==HIGH){
    Serial.println("i");
    //angulo=0;
    //carril=0;
    digitalWrite(led2, HIGH);
    digitalWrite(led1, LOW);
    inputString = "i";
    //myservo.write(angulo);
    if (millis() - previousMillis >= interval) {
      //Serial.println("Entro Boton");
      previousMillis = millis();
      sensorHumerdad();
    }
  }
  // else
  // if(carril==0){
  //   //digitalWrite(led2, HIGH);
  //   //digitalWrite(led1, LOW);
  //   angulo=0;
  //   inputString = "i";
  // }
  // else{
  //   //digitalWrite(led1, HIGH);
  //   //digitalWrite(led2, LOW);
  //   angulo=180;
  //   //Serial.println("Derecha");
  // }
  // myservo.write(angulo); 
  
  // if (millis() - previousMillis >= interval) { 
  //   Serial.println("Entro Boton");
  //   previousMillis = millis();   
  //   sensorHumerdad();
  // }
}

/**Sheyla**/
void puerta(){
  digitalWrite(two, HIGH);
  delay(1); 
  digitalWrite(two, LOW);
  tiempo= pulseIn(three,HIGH);
  distancia=tiempo/58.2;
  //Serial.println(distancia);
  delay(500);
  //condicionamos la puerta para que se habra a 50 centimetros o menos 
  if(distancia<=10)
  {
    myservo.write(90);
  }
  //condicionamos la puerta para que se cierrre a maás de 50 cm
  if(distancia>10)
  {
    myservo.write(0);
  }
}

void sensortemperatura() {   // Programa principal
  temperatura = dht.readTemperature();    // Creamos una variable llamada temperatura donde se almacenará lo leído por el sensor con el comando dht.readTemperature()

  //Serial.print("La temperatura es: ");    // Mostramos el mensaje en el monitor serial
  //Serial.print(temperatura);              // Mostramos la variable temperatura
  //Serial.println(" °C");                  // Mostramos "°C" en el monitor serial
 
  if (temperatura >= 29){                 // If: si la variable temperatura tiene un valor mayor o igual a 29 (°C) entonces:
    digitalWrite(foco, HIGH);             // Nuestro pin foco tendrá un valor high = 5 voltios por tanto el relay se desactivará y el foco se apaga (recordemos que el relay cambia de posición cuando su entrada data está conectada a tierra = 0 volts)
    digitalWrite(cooler, LOW);            // El pin cooler tendrá el valor low = 0 voltios por tanto el relay se activa y el ventilador se enciende
    //Serial.println("Ventilador encendido");   // Mostramos el mensaje en pantalla
  }
  if (temperatura < 24.5){               // If: si la variable temperatura tiene un valor menor o igual a 24.5 (°C) entonces:
    digitalWrite(cooler, HIGH);           // El pin cooler tendrá el valor HIGH por tanto el relay se desactiva, el ventilador se apaga
    digitalWrite(foco, LOW);              // El pin foco tendrá el valor LOW por tanto el relay se activa, el foco se enciende
    //Serial.println("Calefactor encendido");   // Mostramos el mensaje en pantalla
  }
  if(temperatura > 24.5 && temperatura < 29){ // IF: si la variable temperatura se encuentra en el rango de 24.5 - 29 (°C) entonces:
    digitalWrite(cooler,HIGH);             // El pin cooler tendrá el valor HIGH por tanto el relay se desactiva, el ventilador se apaga
    digitalWrite(foco, HIGH);               // El pin foco tendrá el valor HIGH por tanto el relay se desactiva, el foco se apaga
    //Serial.println("Estado Neutro");
  }
      //delay(2000);                        // Delay de 2 segundos para la lectura de la temperatura
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