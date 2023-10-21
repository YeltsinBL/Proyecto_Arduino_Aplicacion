$(document).ready(function () {
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
      }
      return false; // para no salir de la página principal
    });

    //recibir los datos
    socket.connect().on("updateSensorData", function (msg) {
      console.log("Received sensorData :: " + msg.date + " :: " + msg.value);
  
      // Mostrar solo la cantidad de datos permitidos (10)
      if (myChart.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
      }
      addData(msg.date, msg.value);
    });
  });
