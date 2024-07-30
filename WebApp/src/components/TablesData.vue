<template>
  <div class="q-pa-md">
    <h3 class ="propstitle">{{ props.title }}</h3>
    <div  class="row items-center q-gutter-sm" >
    <q-btn label="Apri" @click="openAllCabinets" class="col-auto" style="background: #67c7f0"/>
    <q-btn label="Chiudi" @click="closeAllCabinets" class="col-auto"  style="background: #ec6676"/>
    <q-select
      v-model="selectedStatus"
      :options="statusOptions"
      label="Filter by Status"
      outlined
      dense
      default="All"
      @update:model-value="filterByStatus"
      class="col"
    /></div>
    
    <div>
          <p> 

          </p>
    </div>
    <div v-for="(cabinetRows, idCabinet) in filteredRows" :key="idCabinet" class="mb-4">
      <div v-if="idCabinet === 0" style="
      font-size: 24px; 
      padding: 20px;
      background-color: #67c7f0; 
      border: 2px solid #67c; 
      border-radius: 10px; 
      text-align: center; 
      max-width: 600px; 
      margin: 20px auto; 
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      ">
        <p style="font-weight:bold; color: #333;"> Nessun dispositivo disponibile in questo POP.</p>
      </div>
      <div v-else>
        <q-expansion-item 
          ref="expansionItems" 
          :label="`Cabinet ${idCabinet}`" 
          v-model="expansionState[idCabinet]"
          icon="computer"
        >
        
        
          <q-table
            class="my-sticky-virtscroll-table"
            virtual-scroll
            flat bordered
            v-model:pagination="pagination"
            :rows-per-page-options="[0]"
            :virtual-scroll-sticky-size-start="48"
            row-key="index"
            :rows="cabinetRows"
            :columns="columns"
            :header-classes="headerClasses"
          >
            <template v-slot:body-cell-status="props">
              <q-td :props="props" class="status-cell">
                <status-indicator :status="props.row.status" />
              </q-td>
            </template>
          </q-table>
          <div  class="row items-center q-gutter-sm" >
          
            <div class="diagnostics"  v-if="diagnosticData[idCabinet]">
            
              <p v-for="(value, key) in Object.entries(diagnosticData[idCabinet]).slice(0, 2)" :key="key">{{ value[0]}} {{ value[1] }}</p>
            
            </div>
            
            <div class="diagnostics"  v-if="diagnosticData[idCabinet]">

              <p v-for="(value, key) in Object.entries(diagnosticData[idCabinet]).slice(2, 4)" :key="key">{{ value[0]}} {{ value[1] }}</p>

            </div>

            <div class="diagnostics"  v-if="diagnosticData[idCabinet]">

            <p v-for="(value, key) in Object.entries(diagnosticData[idCabinet]).slice(4, 6)" :key="key">{{ value[0]}} {{ value[1] }}</p>

            </div>

          
          
          </div>
        </q-expansion-item>
        <p>

        </p>
      </div>
    </div>

    
    
    <div class="row items-center q-gutter-sm">
      <div class="chartscontainer">
            <canvas :id="'devicePieChart'" class="piechart"></canvas>
            <canvas id="deviceLineChart" class="linechart"></canvas>
            
            <FloatingBarChart />
      </div>
      <div>
          <FloatingBarChart  class="floatingchart"/> 
      </div>
    </div>
       
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed} from 'vue'
import axios from 'axios'
import StatusIndicator from './StatusIndicator.vue'
import { QSelect, QExpansionItem, QTable, QTd, QBtn, Notify, colors} from 'quasar'
import io from 'socket.io-client'
import { Chart, registerables } from 'chart.js'
import FloatingBarChart from 'components/FloatingBarChart.vue'


Chart.register(...registerables)

const headerClasses = "text-center"
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const columns = [
  { name: 'iddevice', align: 'center', label: 'ID Device', field: 'iddevice', sortable: true },
  { name: 'serialnumber', label: 'Serial Number', field: 'serialnumber', sortable: true },
  { name: 'devicesize', label: 'Device Size', field: 'devicesize', sortable: true },
  { name: 'producer', label: 'Producer', field: 'producer', sortable: true },
  { name: 'yearofproduction', label: 'Year Of Prod.', field: 'yearofproduction', sortable: true},
  { name: 'status', label: 'Status', field: 'status', sortable: true},
  { name: 'usedslot', label: 'Used Slot', field: 'usedslot', sortable: true}, 
  { name: 'devicetype', label: 'Device Type', field: 'devicetype', sortable: true},
  { name: 'latest', label: 'Latest update', field: 'timelog', sortable: true},
  { name: 'device rep', label: 'Device Replaced', field: 'devicereplaced', sortable: true}
]


const groupedRows = ref({})
const filteredRows = ref({})
const selectedStatus = ref('All')
const statusOptions = ref([
     'All', 
    'Active & Inactive',
    'Active',
    'Inactive',
    'Removed'
])
const expansionState = ref({})
const diagnosticData = ref({})
const series = ref({})
let pieChartInstance = null
let lineChartInstance = null





const updatePieChart = () => {
  // Inizializza i contatori
  let totalActiveCount = 0
  let totalInactiveCount = 0
  let totalRemovedCount = 0
  

  // Itera su ogni cabinet e somma i dati
  for (const [idCabinet, cabinetRows] of Object.entries(filteredRows.value)) {
    if (idCabinet !== '0') {
      const activeCount = cabinetRows.filter(item => item.status === 'Active').length
      const inactiveCount = cabinetRows.filter(item => item.status === 'Inactive').length
      const removedCount = cabinetRows.filter(item => item.status === 'Removed').length

      totalActiveCount += activeCount
      totalInactiveCount += inactiveCount
      totalRemovedCount += removedCount
    }
  }


  if (pieChartInstance) {
    pieChartInstance.destroy()
  }

  //if (totalActiveCount != 0 |  totalInactiveCount!=0){
    // Crea un solo grafico con i dati aggregati
    const ctx = document.getElementById('devicePieChart').getContext('2d')
    pieChartInstance = new Chart(ctx, {
      type: 'pie',
      maintainAspectRatio: false,
      data: {
        labels: ['Active', 'Inactive', 'Removed'],
        datasets: [{
          data: [totalActiveCount, totalInactiveCount, totalRemovedCount],
          backgroundColor: ['#8bc5ec', '#3b5c8b', '#c26d76']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: "#5b8ed7",
              font: {
                size: 16
              }
            },
            
            
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.label || ''
                return label + ': ' + context.raw
              }
            }
          }
        }
      }
    })
  //}
}


const updateLineChart = () => {
  const { labels, datasets } = prepareLineChartData();

  if (lineChartInstance) {
    lineChartInstance.destroy();
  }

  
  const ctx = document.getElementById('deviceLineChart').getContext('2d');
  lineChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#5b8ed7'
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.dataset.label || '';
              const value = context.raw || 0;
              return `${label}: ${value}`;
            }
          },
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Date', // Modifica come necessario
            color: '#5b8ed7'
          },
          grid: {
            color: '#5b8ed7' // Cambia il colore delle linee della griglia dell'asse X
          },
          ticks: {
            color: '#5b8ed7'
          }
        },
        y: {
          beginAtZero: true,
          min: 0,
          max: 20,
          stepSize: 1,
          title: {
            display: true,
            text: 'Number of Replaced Device', // Modifica come necessario
            color: '#5b8ed7'
          },
          grid: {
            color: '#5b8ed7' // Cambia il colore delle linee della griglia dell'asse X
          },
          ticks : {
            color: '#5b8ed7'
          }

        }
      }
    }
  });
};

//generazione colori, permette di generare colori nè troppo chiari nè troppo scuri
const getRandomColor = () => {
  const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

  // Funzione per calcolare la luminosità di un colore esadecimale
  const getLuminanceFromHex = (hex) => {
    // Rimuove il carattere '#' se presente
    hex = hex.replace(/^#/, '');

    // Converte i valori esadecimali in RGB
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Calcola la luminosità
    const a = [r, g, b].map(value => {
      value /= 255;
      return value <= 0.03928 ? value / 12.92 : Math.pow((value + 0.055) / 1.055, 2.4);
    });

    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
  };

  const minLum = 0.3; // Luminosità minima desiderata
  const maxLum = 0.7; // Luminosità massima desiderata
  let hexColor, luminance;

  do {
    // Genera un colore esadecimale casuale
    hexColor = '#' + [1, 1, 1].map(() => getRandomInt(0, 255).toString(16).padStart(2, '0')).join('');
    luminance = getLuminanceFromHex(hexColor);
  } while (luminance < minLum || luminance > maxLum);

  return hexColor.toUpperCase();
};


const prepareLineChartData = () => {
  const labels = []; // Etichette sull'asse X (ad esempio date)
  const datasets = [];

  for (const [idCabinet, cabinetRows] of Object.entries(filteredRows.value)) {

    
    console.log("Coppia")
    console.log([idCabinet, cabinetRows])

    if (idCabinet !== '0') {
      // Esempio di preparazione dati
      const replacedDevices = cabinetRows.filter(item => item.devicereplaced === null & item.idaction === 3 ); // Dispositivi sostituiti
      

      const dataMap = replacedDevices.reduce((acc, device) => {
        const date = new Date(device.timelog).toISOString().split('T')[0]; // Ottieni solo la parte della data
        if (!acc[date]) {
          acc[date] = 0;
        }
        acc[date]++;
        return acc;
      }, {});


      const data = Object.keys(dataMap).map(date => ({
        x: date,
        y: dataMap[date] || 0
      }));

      data.sort((a, b) => new Date(a.x) - new Date(b.x));

      datasets.push({
        label: `Cabinet ${idCabinet}`,
        data: data,
        fill: true,
        borderColor: getRandomColor(), // Funzione per generare colori casuali
        backgroundColor:  '#6fc2e54c',
        tension: 0.5
      });
    }
  }

  return { labels, datasets };
};


const loadData = async (title, update) => {
  try {
    const response = await axios.get(`http://127.0.0.1:3000/device/${title}`)
    const diagnosticResponse = await axios.get(`http://127.0.0.1:3000/cabinet/${title}`)
    const data = response.data
    

    if (pieChartInstance) {
      pieChartInstance.destroy()
    }

    if (lineChartInstance) {
      lineChartInstance.destroy();
    }

    if (data[0] !== 0) {

      const grouped = data.reduce((acc, item) => {
        item.forEach(element => {
          if (!acc[element.idcabinet]) {
            acc[element.idcabinet] = []
          }
          acc[element.idcabinet].push(element)
        })
        

        const keys = Object.keys(acc)

        keys.sort((key1, key2) => {
            // Sort alphabetically (ascending order)
            if (key1 < key2) return -1;
            if (key1 > key2) return 1;
            return 0;
        });

        const sortedAcc = {}

        for (const key of keys) {
            sortedAcc[key] = acc[key];
        }

        

        return sortedAcc
      }, {})
      groupedRows.value = grouped


      //per i dati di diagnostica....
      for (const idCabinet of Object.keys(grouped)) {
          diagnosticData.value[idCabinet] = diagnosticResponse.data[idCabinet]

      }
      
      filterByStatus()
      updatePieChart();
      updateLineChart();

      
       
      
      if(update == 0){
        initializeExpansionState()
      }
      
      
    } else {
      groupedRows.value = [0]
      filteredRows.value = [0]
    }

       
   

  } catch (error) {
    console.error('Errore nel recupero dei dati:', error)
  }
}

const filterByStatus = () => {
  if (selectedStatus.value == 'All') {
    filteredRows.value = groupedRows.value
  } else if (selectedStatus.value != 'Active & Inactive') {
    const filtered = {}
    for (const [key, value] of Object.entries(groupedRows.value)) {
      filtered[key] = value.filter(item => item.status === selectedStatus.value)
    }
    filteredRows.value = filtered
  } else {
    const filtered = {}
    for (const [key, value] of Object.entries(groupedRows.value)) {
      filtered[key] = value.filter(item => item.status === 'Active' | item.status === 'Inactive')
    }
    filteredRows.value = filtered
  }

  
}

const initializeExpansionState = () => {
  for (const idCabinet in groupedRows.value) {
    if (!expansionState.value.hasOwnProperty(idCabinet)) {
        expansionState.value[idCabinet] = false
    }
  }
}

const openAllCabinets = () => {
  
  Object.keys(filteredRows.value).forEach(idCabinet => {
    if (idCabinet != 0 & expansionState.value[idCabinet] === false) {
      expansionState.value[idCabinet] = true
    } 
  })
}





//funzione di notifica
const showNotification = (message) => {
 
  Notify.create({
    message: message,
    color: 'primary',
    textColor: 'white',
    position: 'bottom-right',
    timeout: 5000,
    actions: [{ icon: 'close', color: 'white' }],
    classes: 'my-custom-notification'
  })
}


const closeAllCabinets = () => {
  
  Object.keys(filteredRows.value).forEach(idCabinet => {
    if (idCabinet != 0 & expansionState.value[idCabinet] === true) {
      expansionState.value[idCabinet] = false
    } 
  })
}


onMounted(() => {
  
  loadData(props.title, 0)
  
 

  const socket = io('http://127.0.0.1:3000')
  
  socket.on('update_data', (data) => {
    loadData(props.title, 1)
    showNotification("Aggiornamenti nel POP di " + data.position)
  })
})

watch(() => props.title, (newParams) => {
  
  if (newParams) {
     
    loadData(newParams, 0)
    
    
  }
}, { immediate: true })


      
      
  
</script>


<style>
  .propstitle {
    font-size: 40px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 25px;
    margin-top: 8px;
  }
  .my-custom-notification .q-notification__inner {
      font-size: 100px;
   }

   .diagnostics{
    font-size:  17px;
    font-weight: bold;
    margin-top: 20px;
    margin-left: 20px;
    margin-right: 20px;
   }

  .piechart {
    width: 100% !important;
    height: 100% !important;
  }

  .linechart{
    width: 100% !important;
    margin-right: 400px;
    height: 100% !important;
    margin-left: 8%;
  }


  .chartscontainer{
    position: relative;
    width: auto;
    max-width: auto; /* Imposta la larghezza massima */
    height: 400px; /* Imposta l'altezza fissa per il grafico */
    padding-bottom: 0px;
    margin-left: 100px;
    
    display: flex;
    justify-content: space-around;
    margin-top: 200px;
  }
  
    
   
   
</style>