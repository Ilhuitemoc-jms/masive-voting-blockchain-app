<template src="../templates/dashboard_login.html"></template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { logout } from '../scripts/login'

// Función para manejar el logout
const handleLogout = (event) => {
  event.preventDefault()
  logout()
}

// Agregar event listener al enlace de logout cuando el componente se monte
onMounted(() => {
  const logoutLink = document.getElementById('logout-link')
  if (logoutLink) {
    logoutLink.addEventListener('click', handleLogout)
  }
})

// Limpiar event listener cuando el componente se desmonte
onUnmounted(() => {
  const logoutLink = document.getElementById('logout-link')
  if (logoutLink) {
    logoutLink.removeEventListener('click', handleLogout)
  }
})
</script>

<style src="../styles/login.css"></style>
