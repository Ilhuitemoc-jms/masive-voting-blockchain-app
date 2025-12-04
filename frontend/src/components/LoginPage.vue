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

      <!-- Alerta de éxito -->
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>

      <!-- Formulario de acceso -->
      <form @submit.prevent="handleLogin" data-validate="submit" action="#" method="post" id="loginForm">
        <fieldset>
          <legend>
            <span class="nombre">Acceder</span>
          </legend>

          <div class="t-beaneditor-row">
            <label for="username" class="control-label">Número de Cuenta:</label>
            <div class="input-wrapper">
              <input 
                v-model="username"
                data-required-message="Tiene que ingresar un valor para Número de Cuenta."
                data-optionality="required"
                data-validation="true"
                id="username"
                name="username"
                type="text"
                class="form-control"
                placeholder="Ingrese su número de cuenta"
                autocomplete="username"
                :disabled="isLoading"
              >
            </div>
          </div>

          <div class="t-beaneditor-row">
            <label for="password" class="control-label">Clave de Elector:</label>
            <div class="input-wrapper">
              <input
                v-model="password"
                data-required-message="Tiene que ingresar un valor para Clave de Elector."
                data-optionality="required"
                data-validation="true"
                id="password"
                name="password"
                type="password"
                class="form-control"
                placeholder="Ingrese su clave de elector"
                autocomplete="current-password"
                :disabled="isLoading"
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
          </div>
        </fieldset>
      </form>
    </template>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseLayout from './BaseLayout.vue'
import { loginUsuario, isAuthenticated } from '../scripts/login'

// Router para redirección
const router = useRouter()

// Variables reactivas
// username = no_cuenta (número de cuenta)
// password = clave_elector (clave de elector)
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Al montar, verificar si ya está autenticado
onMounted(() => {
  if (isAuthenticated()) {
    // Si ya tiene token, redirigir a applications
    router.push('/applications')
  }
})

// Función de login
const handleLogin = async () => {
  // Limpiar mensajes anteriores
  errorMessage.value = ''
  successMessage.value = ''
  
  // Validar campos
  if (!username.value || !password.value) {
    errorMessage.value = 'Por favor, complete todos los campos.'
    return
  }
  
  // Mostrar estado de carga
  isLoading.value = true
  
  try {
    // Llamar a la función de login
    // username = no_cuenta, password = clave_elector
    const result = await loginUsuario(username.value, password.value)
    
    if (result.success) {
      // Login exitoso
      successMessage.value = '¡Acceso exitoso! Redirigiendo...'
      
      // Redirigir a applications después de un breve delay
      setTimeout(() => {
        router.push('/applications')
      }, 500)
    } else {
      // Error en login
      errorMessage.value = result.error
    }
  } catch (error) {
    console.error('Error inesperado:', error)
    errorMessage.value = 'Error inesperado. Por favor, intente de nuevo.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style src="../styles/login.css"></style>

<style scoped>
.alert {
  padding: 12px 16px;
  margin-bottom: 16px;
  border-radius: 4px;
  font-size: 14px;
}

.alert-error {
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  color: #b91c1c;
}

.alert-success {
  background-color: #dcfce7;
  border: 1px solid #22c55e;
  color: #166534;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}
</style>
