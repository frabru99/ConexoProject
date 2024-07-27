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
        <q-toolbar-title class="q-mx-auto">
          <img src="src/assets/trace.svg" width="100px" height="100px" alt="Logo">
        </q-toolbar-title>

        <div class="q-mb-md">
      
          <img src="/icons/webex-seeklogo.png" width="170px" height="auto" alt="Webex" class="q-mr-xs" />
          
        </div>

        
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


<style>

.q-mb-md {
  margin-bottom: 16px; /* Modifica il valore del margine secondo necessità */
  margin-right: 16px;
  margin-top: 10px;
  

}


/* Aggiungi classi di allineamento per centrare il testo nella toolbar */
.text-right {
  text-align: right;
  margin-top: 30px;
  margin-right: 50px;
}
</style>