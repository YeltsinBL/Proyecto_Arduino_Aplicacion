$(document).ready(function () {

  // Ocultar mensaje de registro
  var mensaje = document.getElementById('mensaje');
  mensaje.style.display = 'none';

    const ctx = document.getElementById('myChart');
  
    const myChart = new Chart(ctx, {
      type: "line",
      data: {
        datasets: [{ label: "Temperature",  }],
      },
      options: {
        borderWidth: 3,
        borderColor: ['rgba(255, 99, 132, 1)',],
      },
    });
  
    function addData(label, data) {
      myChart.data.labels.push(label);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
      });
      myChart.update();
    }
  
    function removeFirstData() {
      myChart.data.labels.splice(0, 1);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
      });
    }
  
    const MAX_DATA_COUNT = 10;
    //connect to the socket server.
    var socket = io.connect();
  
    $('form#form-control').submit(function(event) {
      // Validar campos
      let x = document.getElementById("temperatura_inicial").value;
      if (x < 0 || x > 100 || x == '') {
        document.getElementById("demo").innerHTML = "Valores permitidos desde 0 hasta 100";
      } 
      else {
        document.getElementById("demo").innerHTML = "";
        // Enviar datos al Socket
        socket.emit('my_room_event', {descripcion: $('#descripcion').val(), temperatura_inicial: $('#temperatura_inicial').val(),
        temperatura_final: $('#temperatura_final').val(), humedad_inicial: $('#humedad_inicial').val(), humedad_final: $('#humedad_final').val()});
        
        document.getElementById("mensaje").innerHTML = "Se guardó";
        mensaje.style.display = 'block';
        mensaje.style.opacity = '100';
        window.setTimeout(function() {
            $(".alert").fadeTo(1500,0).slideDown(1000, function(){
                  //$(".alert").remove();
                  mensaje.style.display = 'none';
              });
        },3000);
        document.getElementById("form-control").reset();
      }
      return false; // para no salir de la página principal
    });

    
    $('form#form-conectar').submit(function(event) {
      let _ = document.getElementById("conn").onclick = () => {
        // Enviar datos al Socket
        socket.emit('acciones_arduino', {boton:'conn',valor: $('#ports').val()});
        document.getElementById("mensaje_estado").innerHTML = "Se conectó al arduino";
        document.getElementById('mensaje_estado').style.display = 'block';
        document.getElementById('mensaje_estado').style.opacity = '100';
        window.setTimeout(function() {
            $(".alert_mensaje_estado").fadeTo(1500,0).slideDown(1000, function(){
                  document.getElementById('mensaje_estado').style.display = 'none';
              });
        },3000);
      };
      _ = document.getElementById("on").onclick = () => {
        // Enviar datos al Socket
        socket.emit('acciones_arduino', {boton:'on',valor: 'e'});
        document.getElementById("mensaje_estado").innerHTML = "Encendido";
        document.getElementById('mensaje_estado').style.display = 'block';
        document.getElementById('mensaje_estado').style.opacity = '100';
      };
      _ = document.getElementById("right").onclick = () => {
        // Enviar datos al Socket
        socket.emit('acciones_arduino', {boton:'right',valor: 'd'});
        document.getElementById("mensaje_estado").innerHTML = "Derecha";
        document.getElementById('mensaje_estado').style.display = 'block';
        document.getElementById('mensaje_estado').style.opacity = '100';
      };
      _ = document.getElementById("left").onclick = () => {
        // Enviar datos al Socket
        socket.emit('acciones_arduino', {boton:'left',valor: 'i'});
        document.getElementById("mensaje_estado").innerHTML = "Izquierda";
        document.getElementById('mensaje_estado').style.display = 'block';
        document.getElementById('mensaje_estado').style.opacity = '100';
      };
      _ = document.getElementById("dis").onclick = () => {
        // Enviar datos al Socket
        socket.emit('acciones_arduino', {boton:'dis',valor: 'a'});
        document.getElementById("mensaje_estado").innerHTML = "Desconectado";
        document.getElementById('mensaje_estado').style.display = 'block';
        document.getElementById('mensaje_estado').style.opacity = '100';
        window.setTimeout(function() {
            $(".alert_mensaje_estado").fadeTo(1500,0).slideDown(1000, function(){
                  document.getElementById('mensaje_estado').style.display = 'none';
              });
        },3000);
      };
      return false;
    });

    var lista_puertos=[];
    //recibir los datos
    socket.connect().on("updateSensorData", function (msg) {
      console.log("Received sensorData :: " + msg.date + " :: " + msg.value+" :: " + msg.puertos);
      let str = String(msg.puertos);
      let arr = str.split(",");
      if(lista_puertos.length < arr.length){
        lista_puertos = arr;
        lista_puertos.forEach(myFunction);
        function myFunction(item) {
          console.log(item);
          var aficiones = document.getElementById("ports");
          var option = document.createElement("option");
          option.text = item;
          option.value = item;
          aficiones.add(option);
        }
      }

      // Mostrar solo la cantidad de datos permitidos (10)
      if (myChart.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
      }
      addData(msg.date, msg.value);
    });
  });
