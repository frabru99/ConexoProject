<template>
  <div class="status-indicator-container">
    <div :class="indicatorClass" class="status-indicator">
      <q-tooltip
        anchor="top middle"
        self="bottom middle"
        :offset="[0, 8]" 
      >
        {{ statusText }}
      </q-tooltip>
    </div>
  </div>
</template>

<script setup>

//Template e Script degli indicatori di stato nella Tabella di ogni Cabinet. 

import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true //a seconda dello stato
  }
})

const indicatorClass = computed(() => {  //Affidiamo una classe all'indicatore a seconda dello stato 
  switch (props.status) {
    case 'Active':
      return 'status-active'
    case 'Removed':
      return 'status-removed'
    case 'Inactive':
      return 'status-inactive'
    default:
      return ''
  }
})

const statusText = computed(() => { //A seconda dello stato affidiamo pure una scritta. 
  switch (props.status) {
    case 'Active':
      return 'The device is currently active'
    case 'Removed':
      return 'The device has been removed'
    case 'Inactive':
      return 'The device is inactive'
    default:
      return 'Unknown status'
  }
})
</script>

<style scoped>
/*
  Stile dell'indicatore
*/ 


.status-indicator-container {
  position: relative;
  display: inline-block;
}

.status-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: inline-block;
  margin: auto; /* Centro automaticamente */
}

.status-active {
  background-color: #8bc5ec;
}

.status-removed {
  background-color: #c26d76;
}

.status-inactive {
  background-color: #3b5c8b;
}
</style>
