<template>
  <BaseLayout>
    <!-- Aquí se encuentra el titulo de la página -->
    <template #section-title>
      Acceso a Servicios en Línea
    </template>
    
    <!-- Aquí está el contenido de la página - contenido de login.html -->
    <template #content>
      <!-- Alerta de error (se muestra con Vue) -->
      <div v-if="errorMessage" class="alert alert-error">
        {{ errorMessage }}
      </div>

      <!-- Alerta de información de conexión -->
      <div v-if="connectionStatus" class="alert alert-info">
        {{ connectionStatus }}
      </div>

      <!-- Formulario de acceso -->
      <form @submit.prevent="handleLogin" data-validate="submit" action="#" method="post" id="loginForm">
        <fieldset>
          <legend>
            <span class="nombre">Acceder</span>
          </legend>

          <div class="t-beaneditor-row">
            <label for="username" class="control-label">Nombre de Usuario:</label>
            <div class="input-wrapper">
              <input 
                v-model="username"
                data-required-message="Tiene que ingresar un valor para Nombre de Usuario."
                data-optionality="required"
                data-validation="true"
                id="username"
                name="username"
                type="text"
                class="form-control"
                placeholder="Ingrese su usuario"
                autocomplete="username"
              >
            </div>
          </div>

          <div class="t-beaneditor-row">
            <label for="password" class="control-label">Contraseña:</label>
            <div class="input-wrapper">
              <input
                v-model="password"
                data-required-message="Tiene que ingresar un valor para Contraseña."
                data-optionality="required"
                data-validation="true"
                value=""
                id="password"
                name="password"
                type="password"
                class="form-control"
                placeholder="Ingrese su contraseña"
                autocomplete="current-password"
              >
            </div>
          </div>

          <div class="button-row">
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="isLoading"
              id="submit_0"
              name="submit_0"
            >
              {{ isLoading ? 'Verificando...' : 'Acceder' }}
            </button>
            &nbsp;&nbsp;
            <a href="#" @click.prevent="forgotPassword" class="forgot-link">
              Olvidé mi contraseña
            </a>
          </div>
        </fieldset>
      </form>
    </template>
  </BaseLayout>
</template>

<script setup>
import { ref } from 'vue'
import BaseLayout from './BaseLayout.vue'
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

<style src="../styles/login.css"></style>
