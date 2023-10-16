using System;
using System.Collections;
using System.IO.Ports;
using System.Windows.Forms;
using static System.Net.Mime.MediaTypeNames;

namespace arqui
{
    public partial class Form1 : Form
    {
        String[] ports;
        SerialPort port;
        bool isConnected = false;
        ArrayList datos = new ArrayList();
        
        public Form1()
        {
            InitializeComponent();
            getAvailableCOM_PORTS();

            foreach (string port in ports)
            {
                cboPuertos.Items.Add(port);
                if (ports[0] != null)
                    cboPuertos.SelectedItem = ports[0];
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            CambioEstado();
        }
        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            disconnectFromArduino();
            
        }
        #region Botones
        private void btnIzquierda_Click(object sender, EventArgs e)
        {
            CambioEstado(2);
            port.Write(string.Format(btnIzquierda.Text.ToLower()));
        }

        private void btnDerecha_Click(object sender, EventArgs e)
        {
            CambioEstado(3);
            port.Write(string.Format(btnDerecha.Text.ToLower()));
        }

        private void btnGrafico_Click(object sender, EventArgs e)
        {
            Mostrar_Grafico();
        }

        private void btnSensor_Click(object sender, EventArgs e)
        {
            if (isConnected)
                Estado_Sensor(btnSensor.Text);
        }
        private void btnIniciar_Click(object sender, EventArgs e)
        {
            if (!isConnected)
            {
                CambioEstado(1);
                connectToArduino();
            }
            else
            {
                CambioEstado();
                disconnectFromArduino();

            }
        }
        #endregion  

        #region Conexión Arduino

        private void getAvailableCOM_PORTS()
        {
            ports = SerialPort.GetPortNames();
        }
        
        private void connectToArduino()
        {
            isConnected = true;
            string selectedPort = cboPuertos.GetItemText(cboPuertos.SelectedItem);
            port = new SerialPort(selectedPort, 9600);
            port.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
            port.Open();
            btnIniciar.Text = "Conectado";
        }

        private void disconnectFromArduino()
        {
            isConnected = false;
            port.Close();
            btnIniciar.Text = "Desconectar";
        }

        private void DataReceivedHandler(
                        object sender,
                        SerialDataReceivedEventArgs e)
        {
            SerialPort sp = (SerialPort)sender;
            string indata = sp.ReadExisting();
            Console.WriteLine("Data Received:");

            Console.Write(indata);
            if (isConnected)
            {
                if (btnSensor.Text == "Encendido")
                {
                    txtRespuestaArduino.Invoke(new MethodInvoker(
                        delegate
                        {
                            bool formato_I = indata.Contains("i");
                            bool formato_D = indata.Contains("d");
                            txtRespuestaArduino.Text = formato_I ? "": formato_D ? "": txtRespuestaArduino.Text += indata;
                            if (formato_I) CambioEstado(2);
                            else if (formato_D) CambioEstado(3);

                        }));
                }
            }
        }

        #endregion

        #region Métodos

        private void CambioEstado(int estado = 0)
        {
            if(estado == 0)
            {
                btnIzquierda.Enabled = false;
                btnDerecha.Enabled = false;
                btnSensor.Enabled = false;
                btnGrafico.Enabled = false;

            }else if(estado == 1)
            {
                btnIzquierda.Enabled = false;
                btnDerecha.Enabled = true;
                btnSensor.Enabled = true;
                btnGrafico.Enabled = true;
            }else if(estado == 2)
            {
                btnIzquierda.Enabled = false;
                btnDerecha.Enabled = true;
                txtRespuestaArduino.Text = "";
                datos = new ArrayList();
            }
            else
            {
                btnIzquierda.Enabled = true;
                btnDerecha.Enabled = false;
                txtRespuestaArduino.Text = "";
                datos = new ArrayList();
            }
        }
        private void Estado_Sensor(string nombre_estado)
        {
            if (nombre_estado == "Apagado")
            {
                btnSensor.Text = "Encendido";
                port.Write(string.Format(btnSensor.Text.ToLower()));
            }
            else
            {
                btnSensor.Text = "Apagado";
                port.Write(string.Format(btnSensor.Text.ToLower()));
                txtRespuestaArduino.Text = "";
            }
        }

        private void Mostrar_Grafico()
        {
            // Ocultar el gráfico
            chart1.Visible = true;

            // Limpiar el gráfico antes de mostrar nuevos datos
            chart1.Series.Clear();

            // Crear una nueva serie para los datos
            var serie = new System.Windows.Forms.DataVisualization.Charting.Series("Datos");

            // Configurar el tipo de gráfico (en este caso, gráfico de líneas)
            serie.ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;

            string[] separatingStrings = { "\tr6\tr\tn", "\tr\tn", "\tr", "\r\n", "\n", "\r" };
            string[] words = txtRespuestaArduino.Text.Split(separatingStrings, StringSplitOptions.RemoveEmptyEntries);

            foreach (var word in words)
            {
                datos.Add(Convert.ToInt32(word));
            }
            foreach (int dato in datos)
            {
                serie.Points.AddY(dato);
            }

            // Agregar la serie al gráfico
            chart1.Series.Add(serie);
        }
 
        #endregion
    }
}
