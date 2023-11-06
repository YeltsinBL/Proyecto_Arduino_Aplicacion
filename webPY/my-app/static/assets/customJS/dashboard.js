$(document).ready(function () {
    
    cbo_Sector = document.getElementById('sector_nombre').value;
    document.querySelector("#sector_nombre").addEventListener("change", function(){
        //Las instrucciones que desees ejecutar
        cbo_Sector = document.getElementById('sector_nombre').value;
        obtener_medicion_sector_humedad(cbo_Sector);
        obtener_medicion_sector_temperatura(cbo_Sector);
    }, false);
    
const ctx = document.getElementById('myChart');
const ctx_humedad = document.getElementById('myCharthumedad');
const myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [{ label: "Temperature",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(8, 0, 250, 1)',],
    },
  });
const myChart_humedad = new Chart(ctx_humedad, {
    type: "line",
    data: {
      datasets: [{ label: "Humedad",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(17, 178, 247, 1)',],
    },
  });
  // Llenar el gráfico cuando se visualiza por primera vez
  obtener_medicion_sector_humedad(cbo_Sector);
  obtener_medicion_sector_temperatura(cbo_Sector);
function addData(myChartvalue,label, data) {
    myChartvalue.data.labels.push(label);
    myChartvalue.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChartvalue.update();
  }

function removeFirstData(myChartvalue) {
    myChartvalue.data.labels.splice(0, 1);
    myChartvalue.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }
  const MAX_DATA_COUNT = 10;
  async function obtener_medicion_sector_humedad(valor = 3){    
    try {
        let total_humedad = myChart_humedad.data.labels.length;
        while (total_humedad >= 0) {
            myChart_humedad.data.labels.pop();
            myChart_humedad.data.datasets[0].data.pop();
            total_humedad--;
        }
        myChart_humedad.update();

        const dataPeticion = { valor };
        const headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        };
        // Axios: Envía solicitudes HTTP mediante promesas en JS
        const response = await axios.post("/buscando-medicion-sector", dataPeticion, { headers });
        if (!response.status) {
        console.log(`HTTP error! status: ${response.status} 😭`);
        }

        if (response.data.fin === 0) {
        return false;
        }

        if (response.data) {
            let miData = response.data;
            let str = String(miData);
            let arr = str.split("<br>");
            let claves = Object.keys(arr);
            for(let i=0; i< claves.length-1; i++){
                let clave = claves[i];
                let formatear = String(arr[clave]).split("\n")
                let array_valores = formatear.filter(Boolean);

                if (myChart_humedad.data.labels.length > MAX_DATA_COUNT) {
                    removeFirstData(myChart_humedad);
                }
                addData(myChart_humedad, array_valores[1], array_valores[0]);
            }
        }
    } catch (error) {
        console.error(error);
    }
  }
  async function obtener_medicion_sector_temperatura(valor = 3){
    try {
        let total_temperatura = myChart.data.labels.length;
        while (total_temperatura >= 0) {
            myChart.data.labels.pop();
            myChart.data.datasets[0].data.pop();
            total_temperatura--;
        }
        myChart.update();

        const dataPeticion = { valor };
        const headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        };
        // Axios: Envía solicitudes HTTP mediante promesas en JS
        const response = await axios.post("/buscando-medicion-sector-temperatura", dataPeticion, { headers });
        if (!response.status) {
        console.log(`HTTP error! status: ${response.status} 😭`);
        }

        if (response.data.fin === 0) {
        return false;
        }

        if (response.data) {
            let miData = response.data;
            let str = String(miData);
            let arr = str.split("<br>");
            let claves = Object.keys(arr);
            for(let i=0; i< claves.length-1; i++){
                let clave = claves[i];
                let formatear = String(arr[clave]).split("\n")
                let array_valores = formatear.filter(Boolean);

                if (myChart.data.labels.length > MAX_DATA_COUNT) {
                    removeFirstData(myChart);
                }
                addData(myChart,array_valores[1], array_valores[0]);
            }
        }
    } catch (error) {
        console.error(error);
    }
  }
  var socketio = io();
  socketio.on("datosmedicion", (data) => {
    if(data.medicion_sector==String(cbo_Sector)){
      let dato_humedad = data.humedad.split(",");
      for(let i=0; i< dato_humedad.length; i++){
        if (myChart_humedad.data.labels.length > MAX_DATA_COUNT) {
          removeFirstData(myChart_humedad);
        }
        addData(myChart_humedad,data.fecha_registro, dato_humedad[i]);
      }
      let dato_temperatura = data.temperatura.split(",");
      for(let i=0; i< dato_temperatura.length; i++){
        if (myChart.data.labels.length > MAX_DATA_COUNT) {
          removeFirstData(myChart);
        }
        addData(myChart,data.fecha_registro, dato_temperatura[i]);
      }
    }
  });
});
