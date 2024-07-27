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
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const indicatorClass = computed(() => {
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

const statusText = computed(() => {
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
  background-color: green;
}

.status-removed {
  background-color: red;
}

.status-inactive {
  background-color: orange;
}
</style>
