<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title>
          <img src="src/assets/trace.svg" width="100px" height="100px">
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>
          Esplora i POP.
        </q-item-label>

        <EsploraRisorse
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
          @select="handleSelect"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <TablesData v-if="selectedTitle" :title="selectedTitle" />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EsploraRisorse from 'components/MenuLaterale.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import TablesData from 'components/TablesData.vue'

defineOptions({
  name: 'MainLayout'
})

const linksList = ref([])
const router = useRouter()

axios.get("http://192.168.1.14:3000/luoghi").then(response => {
  linksList.value = response.data
  console.log(linksList.value)
})

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const selectedTitle = ref(null)

function handleSelect(title) {
  selectedTitle.value = title
}
</script>
