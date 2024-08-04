<template>
  <div v-if="show" class="typing-container">
    <div v-for="(line, index) in lines" :key="index" class="typing-line">
      <h1 v-show="currentIndex === index" :id="'typing-text-' + index"></h1>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const show = ref(true)
const lines = ref([
  "Benvenuto alla Dashboard!",
  "Per iniziare, espandi il menù a sinistra!"
])
const currentIndex = ref(0)

onMounted(() => {
  typeLine(0)
})

//Funzione che permette la scrittura di "Lines" con effetto scrittura. 

function typeLine(index) {
  const text = lines.value[index]
  const typingTextElement = document.getElementById(`typing-text-${index}`)
  
  if (!typingTextElement) return

  let currentCharIndex = 0

  function type() { //permette di scrivere lettera per lettera e poi passare alla riga successiva  
    if (currentCharIndex < text.length) {
      typingTextElement.textContent += text.charAt(currentCharIndex)
      currentCharIndex++
      setTimeout(type, 90) // Velocità dell'effetto di scrittura
    } else {
      setTimeout(() => {
        if (index < lines.value.length - 1) {
          currentIndex.value = index + 1
          typeLine(index + 1)
        }
      }, 2000) // Pausa tra le righe
      typingTextElement.classList.add('completed') 
    }
  }

  type() //chiamata ricorsiva a type 
}
</script>

<style scoped>
.typing-container {
  position: absolute;
  top: 50%;
  left: 43%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #333;
}

.typing-line {
  margin: 0;
  padding: 0;
}

h1 {
  font-size: 4rem; /* Dimensione del font modificata */
  color: #4a91e2a5; /* Colore del testo modificato */
  font-family: 'Roboto', sans-serif; /* Font personalizzato */
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  border-right: 0.15em solid #4a90e2; /* Colore del cursore */
  display: inline-block;
  animation: blink-caret 0.75s step-end infinite, fadeIn 1s ease-in-out forwards;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* Ombra del testo */
}

.completed {
  border-right: none; /* Rimuovi il cursore lampeggiante */
}

@keyframes blink-caret {
  from, to { border-color: transparent; }
  50% { border-color: #4a90e2; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
