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
    meta: { requiresAuth: true }
  },
  {
    path: '/voting',
    name: 'Voting',
    component: VotingForm,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Si la ruta requiere autenticación y no hay token, redirige al login
    next('/')
  } else if (to.name === 'Login' && isAuthenticated) {
    // Si ya está autenticado y va al login, redirige a applications
    next('/applications')
  } else {
    next()
  }
})

export default router
