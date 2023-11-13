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
    //var cant=0;
    var valor_temperatura=0;
    var valor_humedad=0;
    var socket = io();
    /** Sector Botones Emitir Socket**/
    document.querySelector("#btnconectado").addEventListener("change", function(){
        btnconectado = document.getElementById('btnconectado').value;
        socket.emit('acciones_arduino', {boton:btnconectado,valor: $('#medicion_puertos').val(), datosarduino:$('#medicion_puertos').val()});
    }, false);
    document.querySelector("#btndesconectado").addEventListener("change", function(){
        //cant =0;
        btndesconectado = document.getElementById('btndesconectado').value;
        socket.emit('acciones_arduino', {boton:btndesconectado,valor: "a", datosarduino:$('#medicion_puertos').val()});
        document.getElementById('btnapagado').checked=true;
    }, false);
    document.querySelector("#btnencendido").addEventListener("change", function(){
        /*if(cant==0){
            cant++;*/
            btnencendido = document.getElementById('btnencendido').value;
            socket.emit('acciones_arduino', {boton:btnencendido,valor: "e", datosarduino:$('#medicion_puertos').val()});
/*
        }else{
            socket.emit('acciones_arduino', {boton:"right",valor: "i", datosarduino:$('#medicion_puertos').val()});
        }*/
    }, false);
    document.querySelector("#btnapagado").addEventListener("change", function(){
        btnapagado = document.getElementById('btnapagado').value;
        socket.emit('acciones_arduino', {boton:btnapagado,valor: "d", datosarduino:$('#medicion_puertos').val()});
    }, false);
    /** Leer Socket 
    document.querySelector("#medicion_puertos").addEventListener("change", function(){
        socket.on("datosarduino", (data) => {
            console.log("Entró", data);
            console.log("Entró", $('#medicion_puertos').val());
            if(data.datosarduino == $('#medicion_puertos').val()){
                if(document.getElementById('btnconectado').value == data.boton){
                    document.getElementById('btnconectado').checked=true;
                }
                if(document.getElementById('btndesconectado').value == data.boton){
                    document.getElementById('btndesconectado').checked=true;
                    document.getElementById('btnapagado').checked=true;
                }
                if(document.getElementById('btnencendido').value == data.boton || data.boton =="right"){
                    document.getElementById('btnencendido').checked=true;
                    document.getElementById('btnconectado').checked=true;
                }
                if(document.getElementById('btnapagado').value == data.boton){
                    document.getElementById('btnapagado').checked=true;
                }
            }
            
        });
    }, false);**/
    socket.on("datosarduino", (data) => {
        //console.log("datosarduino",data);
        if(data.datosarduino == $('#medicion_puertos').val()){
            if(document.getElementById('btnconectado').value == data.boton){
                document.getElementById('btnconectado').checked=true;
            }
            /*if(document.getElementById('btndesconectado').value == data.boton){
                document.getElementById('btndesconectado').checked=true;
                document.getElementById('btnapagado').checked=true;
                valor_humedad =0;
                setInterval(charts(valor_humedad), 1500);
            }
            if(document.getElementById('btnencendido').value == data.boton || data.boton =="right"){
                document.getElementById('btnencendido').checked=true;
                document.getElementById('btnconectado').checked=true;
                valor_humedad = 80;
                
                setInterval(charts(valor_humedad), 1500);
            }
            if(document.getElementById('btnapagado').value == data.boton){
                document.getElementById('btnapagado').checked=true;
                valor_humedad = 50;
                setInterval(charts(valor_humedad), 1500);
            }*/

            /** Procesar los valores del Arduino **/
            if(data.dato_prueba == "0,0" || data.dato_prueba == "0,100"|| data.dato_prueba == "100,0"){
                document.getElementById('btnapagado').checked=true;
                setInterval(charts(0, 0), 1500);
            }else{
                
                document.getElementById('btnencendido').checked=true;
                let datos_arduino = data.dato_prueba.split(",");;
                for(let i=0; i< datos_arduino.length; i++){
                    console.log("datosarduino",datos_arduino);
                    setInterval(charts(datos_arduino[0], datos_arduino[1]), 1500);
                }
            }

        }
        
    });
    /** Fecha Actual **/
    updateDateTime();
    function updateDateTime() {
        // create a new `Date` object
        const now = new Date();
        const currentDateTime = now.toLocaleString("en-GB");
        const dateControl = document.querySelector('input[type="text"]');
        dateControl.value = currentDateTime;
    }
    setInterval(updateDateTime);
    function charts(temperatura,humedad){
        $(".gauge-temperature").gaugeMeter({ percent: temperatura});//{ percent: temperatura*100/50}
        $(".value-temperature").html(temperatura+" C°");    
        $(".gauge-humidity").gaugeMeter({ percent: humedad});
        $(".value-humidity").html(humedad+" %");
    }
    setInterval(charts(valor_temperatura,valor_humedad), 1500);
    
    

});
