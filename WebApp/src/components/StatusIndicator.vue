<template>
    <div :class="indicatorClass" class="status-indicator"></div>
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
  </script>
  
<style scoped>

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
  