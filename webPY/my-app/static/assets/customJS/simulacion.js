$(document).ready(function () {
  obtener_puertos_disponibles();
  async function obtener_puertos_disponibles(){
      try {
          const headers = {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
          };
          // Axios: Envía solicitudes HTTP mediante promesas en JS
          const response = await axios.post("/lista_puertos_disponibles", { headers });
          if (!response.status) {
          console.log(`HTTP error! status: ${response.status} 😭`);
          }
  
          if (response.data.fin === 0) {
          return false;
          }
  
          if (response.data) {
              response.data.forEach(myFunction);
              function myFunction(item) {
                  var aficiones = document.getElementById("medicion_puertos");
                  var option = document.createElement("option");
                  option.text = item;
                  option.value = item;
                  aficiones.add(option);
              }
          }
      } catch (error) {
          console.error(error);
      }
  }
  
// Botella de agua
let waterElement = document.getElementById('water');
function fillBottle(value) {
  $(".value-agua").html(value+" L"); 
  if (value <= 160) {
    waterElement.style.height = `${value}px`; // Cambia la altura del agua
  } else {
    value = 160; // Limita el nivel máximo de agua
  }
}

// Puerta
// const doorElement = document.querySelector('.door');
// function toggleDoor(isOpen) {
//   if (isOpen) {
//     doorElement.classList.add("open");
//   } else {
//     doorElement.classList.remove("open");
//   }
// }
// toggleDoor();

//Ventilador
let bladesElement = document.getElementById('fan2');
function toggleFan(isFanOn) {
  if (isFanOn) {
    bladesElement.style.animationPlayState = 'running';
  } else {
    bladesElement.style.animationPlayState = 'paused';
  }
}

// Foco
let lampElement = document.getElementById('lamp');
function toggleLight(isLightOn) {
  if (isLightOn) {
    lampElement.classList.add('light-on');
  } else {
    lampElement.classList.remove('light-on');
  }
}

// Temperatura
const indicator = document.getElementById('indicator');
function setTemperature(value) {
  $(".value-temperatura").html(value+" C°");
  const percentage = value + '%';
  indicator.style.left = percentage;
}

// Humedad
const indicator_two = document.getElementById('indicator_two');
function setHumidity(value) {
  $(".value-humedad").html(value+" C°");
  indicator_two.style.left = value + '%';
}

// Pasar Agua
const indicator_three = document.getElementById('indicator_three');
const water_two = document.getElementById('water_two');
const cuadrado = document.getElementById('cuadrado');
function setPaseagua(value) {
  if(value){
    water_two.style.width = '100%';
    indicator_three.style.left = '100%';
    indicator_three.visibility='hidden';
    cuadrado.style.visibility='hidden';
  }else{
    water_two.style.width = '50%';
    indicator_three.style.left = '50%';
    indicator_three.visibility='visible';
    cuadrado.style.visibility='visible';
  }
}

  var socket = io();
  /** Sector Botones Emitir Socket**/
  document.querySelector("#btnconectado").addEventListener("change", function(){
      btnconectado = document.getElementById('btnconectado').value;
      socket.emit('acciones_arduino', {boton:btnconectado,valor: $('#medicion_puertos').val(), datosarduino:$('#medicion_puertos').val()});
  }, false);
  document.querySelector("#btndesconectado").addEventListener("change", function(){
      btndesconectado = document.getElementById('btndesconectado').value;
      socket.emit('acciones_arduino', {boton:btndesconectado,valor: "a", datosarduino:$('#medicion_puertos').val()});
      document.getElementById('btnapagado').checked=true;
      toggleLight(false);
      toggleFan(false);
      setPaseagua(false);
      setHumidity(0);
      setTemperature(0);
      fillBottle(0);
  }, false);
  document.querySelector("#btnencendido").addEventListener("change", function(){
      btnencendido = document.getElementById('btnencendido').value;
      socket.emit('acciones_arduino', {boton:btnencendido,valor: "e", datosarduino:$('#medicion_puertos').val()});
  }, false);
  document.querySelector("#btnapagado").addEventListener("change", function(){
      btnapagado = document.getElementById('btnapagado').value;
      socket.emit('acciones_arduino', {boton:btnapagado,valor: "d", datosarduino:$('#medicion_puertos').val()});
  }, false);

  socket.on("datosarduino", (data) => {
    console.log("datosarduino",data);
    if(data.datosarduino == $('#medicion_puertos').val()){
        if(document.getElementById('btnconectado').value == data.boton){
            document.getElementById('btnconectado').checked=true;
        }
        /** Procesar los valores del Arduino **/
        if(data.dato_prueba == "0,0,0" || data.dato_prueba == "0,100,0"|| data.dato_prueba == "100,0,0"){
            document.getElementById('btnapagado').checked=true;
        }else{            
            document.getElementById('btnencendido').checked=true;
            let datos_arduino = data.dato_prueba.split(",");;
            for(let i=0; i< datos_arduino.length; i++){
                console.log("datosarduino",datos_arduino);
                if(datos_arduino[0] >=29){
                  toggleLight(false);
                  toggleFan(true);
                }
                if(datos_arduino[0] <24.5){
                  toggleLight(true);
                  toggleFan(false);
                }
                if(datos_arduino[0] >24.5 && datos_arduino[0] <29){
                  toggleLight(false);
                  toggleFan(false);
                }
                setTemperature(datos_arduino[0]);
                setPaseagua((datos_arduino[1]>35)? false:true);
                setHumidity(datos_arduino[1]);
                fillBottle(datos_arduino[2]);
            }
        }
    }
  });
});
