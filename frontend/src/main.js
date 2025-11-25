import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Importa estilos globales si los tienes
// import './styles/global.css' // Archivo no existe aún

// Crea la aplicación Vue
const app = createApp(App)

// Usa el router
app.use(router)

// Monta la aplicación en el div con id="app"
app.mount('#app')
