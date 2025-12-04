import { createRouter, createWebHistory } from 'vue-router'

// Importa los componentes .vue (orquestadores)
import LoginPage from '@/components/LoginPage.vue'
import ApplicationsView from '@/components/ApplicationsView.vue'
import VotingForm from '@/components/VotingForm.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/applications',
    name: 'Applications',
    component: ApplicationsView,
    meta: { requiresAuth: true }  // Ruta protegida
  },
  {
    path: '/voting',
    name: 'Voting',
    component: VotingForm,
    meta: { requiresAuth: true }  // Ruta protegida
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ============================================
// GUARD DE NAVEGACIÓN - PROTECCIÓN DE RUTAS
// ============================================
// Este guard verifica si el usuario tiene un token válido
// antes de permitir acceso a rutas protegidas.
//
// Para proteger una ruta, agrega: meta: { requiresAuth: true }
// en la definición de la ruta arriba.
// ============================================
router.beforeEach((to, from, next) => {
  // Verificar si hay token en localStorage
  // El token se guarda con la clave 'token' en login.js
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Si la ruta requiere autenticación y no hay token, redirige al login
    console.log('Ruta protegida, redirigiendo al login...')
    next({ name: 'Login' })
  } else if (to.name === 'Login' && isAuthenticated) {
    // Si ya está autenticado y va al login, redirige a applications
    console.log('Ya autenticado, redirigiendo a applications...')
    next({ name: 'Applications' })
  } else {
    // Permitir navegación normal
    next()
  }
})

export default router
