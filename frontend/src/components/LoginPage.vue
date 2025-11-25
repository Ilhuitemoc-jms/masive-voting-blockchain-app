<template src="../templates/login.html"></template>

<script setup>
import { ref } from 'vue'
import '../scripts/login.js'

// Variables reactivas
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const connectionStatus = ref('')

// Funciones
const handleLogin = () => {
  // La lógica de login se manejará en login.js
  isLoading.value = true
  // Aquí se llamará a la función de login cuando esté implementada
}

const forgotPassword = () => {
  // La lógica de recuperación de contraseña se manejará en login.js
  console.log('Olvidé mi contraseña')
}
</script>

<style scoped src="../styles/login.css"></style>
