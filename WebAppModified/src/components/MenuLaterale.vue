<template>
  <!--Al click di un POP, emette il titolo.-->
  <q-item
    clickable
    tag="a"
    target="_blank"
    @click="$emit('select', title)" 
  >
    <q-item-section
      v-if="props.icon"
      avatar
    >
      <q-icon :name="props.icon" />
    </q-item-section>

    <q-item-section class="clickable">
      <q-item-label>{{ props.title }}</q-item-label>
      <q-item-label caption>{{ props.caption }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script setup>

//Definizione template del Menù Laterale e i valori Presenti, presi tramite query. 
defineOptions({
  name: 'EsploraRisorse'
})

const props = defineProps({
  title: {
    type: String,
    required: true
  },

  caption: {
    type: String,
    default: ''
  },

  icon: {
    type: String,
    default: ''
  }
})


</script>

<style>

.clickable{
  font-size: 150%;
}
</style>
