async function buscadorTableMedicion(tableId) {
  let fecha_desde,fecha_hasta, busqueda, url;
  url = "/buscando-medicion";

  // Verificar si el valor ingresado tiene formato fecha
  const DATE_REGEX = /^(0[1-9]|[1-2]\d|3[01])(\/)(0[1-9]|1[012])\2(\d{4})$/
  const CURRENT_YEAR = new Date().getFullYear()

  const validateDate = (birthDate) => {
      
    // Comprobar formato dd/mm/yyyy, que el no sea mayor de 12 y los días mayores de 31
    if (!birthDate.match(DATE_REGEX)) {
      return false
    }
    
    // Comprobar los días del mes
    const day = parseInt(birthDate.split('/')[0])
    const month = parseInt(birthDate.split('/')[1])
    const year = parseInt(birthDate.split('/')[2])
    const monthDays = new Date(year, month, 0).getDate()
    if (day > monthDays) {
      return false
    }
    
    // Comprobar que el año no sea superior al actual
    if (year > CURRENT_YEAR) {
      return false
    }
    return true
  }

  fecha_desde = document.getElementById("fecha_desde").value;
  fecha_hasta = document.getElementById("fecha_hasta").value;
  
  if((validateDate(fecha_desde) &&  validateDate(fecha_hasta) ||
      (fecha_desde =="" && fecha_hasta ==""))) {
    const dataPeticion = { fecha_desde,fecha_hasta };
    const headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    };

    try {
      // Axios: Envía solicitudes HTTP mediante promesas en JS
      const response = await axios.post(url, dataPeticion, { headers });
      if (!response.status) {
        console.log(`HTTP error! status: ${response.status} 😭`);
      }

      if (response.data.fin === 0) {
        $(`#${tableId} tbody`).html("");
        $(`#${tableId} tbody`).html(`
        <tr>
          <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda: <strong style="text-align:center;color: #222;">${fecha_desde} - ${fecha_hasta}</strong></td>
        </tr>`);
        return false;
      }

      if (response.data) {
        $(`#${tableId} tbody`).html("");
        let miData = response.data;
        $(`#${tableId} tbody`).append(miData);
      }
    } catch (error) {
      console.error(error);
    }
  }
}

async function buscar(tableId){
  buscadorTableMedicion(tableId);
}