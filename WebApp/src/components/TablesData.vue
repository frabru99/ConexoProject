<template>
  <div class="q-pa-md">
    <q-select
      v-model="selectedStatus"
      :options="statusOptions"
      label="Filter by Status"
      outlined
      dense
      default="All"
      @update:model-value="filterByStatus"
    />
    <div v-for="(cabinetRows, idCabinet) in filteredRows" :key="idCabinet" class="mb-4">
      <div v-if="idCabinet === 0" style="
      font-size: 24px; 
      padding: 20px;
      background-color: #ffdddd; 
      border: 2px solid #f99; 
      border-radius: 10px; 
      text-align: center; 
      max-width: 600px; 
      margin: 20px auto; 
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      ">
        <p style="font-weight:bold; color: #333;"> Nessun dispositivo disponibile in questa regione.</p>
      </div>
      <div v-else>
        <q-expansion-item :label="`Cabinet ${idCabinet}`" icon="folder">
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
        </q-expansion-item>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import StatusIndicator from './StatusIndicator.vue'
import { QSelect, QExpansionItem, QTable, QTd } from 'quasar'
import io from 'socket.io-client';

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
  { name: 'devicetype', label: 'Device Type', field: 'devicetype', sortable: true}
]

const rows = ref([])
const groupedRows = ref({})
const filteredRows = ref({})
const selectedStatus = ref('All')
const statusOptions = ref([
     'All',
    'Active',
    'Inactive',
    'Removed'
])

const loadData = async (title) => {
  try {
    const response = await axios.get(`http://192.168.1.14:3000/device/${title}`)
    const data = response.data

    if (data[0] !== 0) {
      const grouped = data.reduce((acc, item) => {
        item.forEach(element => {
          if (!acc[element.idcabinet]) {
            acc[element.idcabinet] = []
          }
          acc[element.idcabinet].push(element)
        })
        return acc
      }, {})
      groupedRows.value = grouped
      filterByStatus()
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
    console.log(selectedStatus.value)
    console.log(groupedRows.value)
    console.log(filteredRows.value)
  } else {
    const filtered = {}
    for (const [key, value] of Object.entries(groupedRows.value)) {
      filtered[key] = value.filter(item => item.status === selectedStatus.value)
    }

   
    console.log(filtered)
    
    filteredRows.value = filtered

    console.log(groupedRows.value)
  }
}

onMounted(() => {
  loadData(props.title)


  const socket = io('http://192.168.1.14:3000');

  socket.on('update_data', () => {
      loadData(props.title); // Ricarica i dati quando si riceve una notifica
  });

  

})

watch(() => props.title, (newParams) => {
  if (newParams) {
    loadData(newParams)
  }

  
}, { immediate: true })
</script>

