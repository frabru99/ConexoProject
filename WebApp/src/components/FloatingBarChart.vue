<template>
  <div class="fixed-container">
    <select v-model="selectedYear" @change="fetchData" class="year-selector">
      <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
    </select>
    <canvas ref="chartCanvas" class="chart-canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const chartCanvas = ref(null)
const chart = ref(null)
const selectedYear = ref(new Date().getFullYear()) // Anno corrente come valore predefinito
const years = ref([2023, 2024]) // Anni disponibili
const data = ref({ labels: [], datasets: [] })

const fetchData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:3000/cabinet/Roma/${selectedYear.value}`)
    const responseData = response.data
    updateChart(responseData)
  } catch (error) {
    console.error("Error fetching data:", error)
  }
}

const updateChart = (responseData) => {
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ]

  const deviceTypes = ["Router", "Switch", "Firewall", "PowerSupply"]

  // Prepara i dati per le barre
  const insertedData = months.map(month => responseData.inserted[month] || [0, 0, 0, 0])
  const removedData = months.map(month => responseData.removed[month] || [0, 0, 0, 0])

  // Dataset per i dispositivi inseriti
  const datasetsInserted = deviceTypes.map((device, index) => ({
    label: `${device} Inserted`,
    backgroundColor: `rgba(${index * 60}, ${index * 80}, 150, 0.5)`,
    borderColor: `rgba(${index * 60}, ${index * 80}, 150, 1)`,
    borderWidth: 1,
    data: insertedData.map(monthData => monthData[index] || 0),
    stack: `${device}Inserted`
  }))

  // Dataset per i dispositivi rimossi
  const datasetsRemoved = deviceTypes.map((device, index) => ({
    label: `${device} Removed`,
    backgroundColor: `rgba(${index * 60}, ${index * 80}, 255, 0.5)`,
    borderColor: `rgba(${index * 60}, ${index * 80}, 255, 1)`,
    borderWidth: 1,
    data: removedData.map(monthData => monthData[index] || 0),
    stack: `${device}Removed`
  }))

  // Aggiorna i dati del grafico
  data.value = {
    labels: months,
    datasets: [...datasetsInserted, ...datasetsRemoved]
  }

  if (chart.value) {
    chart.value.destroy()
  }
  
  chart.value = new Chart(chartCanvas.value, {
    type: 'bar',
    data: data.value,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true,
          title: {
            display: true,
            text: 'Month'
          }
        },
        y: {
          beginAtZero: true,
          min: -10,
          max: 10,
          title: {
            display: true,
            text: 'Count'
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.dataset.label || ''
              const value = context.raw
              return `${label}: ${value}`
            }
          }
        }
      }
    }
  })
}

onMounted(() => {
  fetchData() // Carica i dati iniziali
})

watch(selectedYear, () => {
  fetchData() // Ricarica i dati quando l'anno cambia
})
</script>

<style scoped>
.fixed-container {
  position: fixed; /* Fissa il contenitore nella posizione */
  top: 50%; /* Imposta la distanza dall'alto */
  right: 50px; /* Imposta la distanza da destra */
  width: 600px; /* Imposta una larghezza fissa se necessario */
  height: 600px; /* Imposta un'altezza fissa se necessario */
  padding: 20px; /* Spazio interno */
  background: white; /* Sfondo bianco per visibilitÃ  */
  border: 1px solid #ddd; /* Bordo sottile per definire il contenitore */
  z-index: 1000; /* Assicurati che il componente sia sopra gli altri contenuti */
}

.chart-canvas {
  width: 100%;
  height: 100%;
}

.year-selector {
  width: 100%;
  margin-bottom: 10px;
}
</style>