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
          <img src="/icons/dtlabpw.png" width="190px" height="auto" alt="Webex" class="q-mr-xs" />
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>
          Monitora i POP.
        </q-item-label>

        <EsploraRisorse
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
          @select="handleSelect"
        />
      </q-list>

      <q-toggle
        v-model="isDarkMode"
        color="primary"
        @update:model-value="toggleDarkMode"
        toggle-order="tf"
        class="toggle"
        indeterminate-value="Toggle Dark Mode"
        :label="isDarkMode ? 'Light Mode' : 'Dark Mode'"
      />
    </q-drawer>

    <q-page-container>
      <img class="conexologo" src="public/x_conexo.png" v-if="!selectedTitle"> 
      <img class="italy" src="public/Italy.png" v-if="!selectedTitle"> 
      <TypingEffect v-if="!selectedTitle" />
      <TablesData v-if="selectedTitle" :title="selectedTitle" />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, watch } from 'vue'
import EsploraRisorse from 'components/MenuLaterale.vue'
import axios from 'axios'
import TablesData from 'components/TablesData.vue'
import TypingEffect from 'components/TypingEffect.vue'
import { Dark } from 'quasar'

const linksList = ref([])
const leftDrawerOpen = ref(false)
const isDarkMode = ref(false)
const selectedTitle = ref(null)

axios.get("http://127.0.0.1:3000/luoghi").then(response => {
  linksList.value = response.data
})

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const toggleDarkMode = () => {
  Dark.toggle()
}

function handleSelect(title) {
  selectedTitle.value = title
}
</script>

<style>
.q-mb-md {
  margin-bottom: 16px;
  margin-right: 16px;
  margin-top: 10px;
}

.text-right {
  text-align: right;
  margin-top: 30px;
  margin-right: 50px;
}

.toggle {
  position: fixed;
  bottom: 0;
}

.q-toggle__thumb .absolute .flex .flex-center .no-wrap {
  flex: none;
}

.conexologo{
  position: absolute;
  top: 50%;
  left: 8%;
  transform: translate(-50%, -50%);
  width: 200px;

}

.italy {
  position: absolute;
  top: 52%;
  left: 83%;
  transform: translate(-50%, -50%);
  width: 650px;
}
</style>
