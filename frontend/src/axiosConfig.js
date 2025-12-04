import axios from 'axios'

// URL base del backend - cambiar en producción
const BASE_URL = 'http://localhost:8000/'

// Crear instancia de axios
const axiosInstance = axios.create({
  baseURL: `${BASE_URL}api/`,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar el token JWT a todas las peticiones
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar respuestas y errores
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Token expirado o inválido
      if (error.response.status === 401) {
        const errorMsg = error.response.data?.error || error.response.data?.message || ''
        if (errorMsg.includes('expirado') || errorMsg.includes('expired') || errorMsg.includes('inválido') || errorMsg.includes('Invalid')) {
          // Limpiar datos de sesión
          localStorage.removeItem('token')
          localStorage.removeItem('user_id')
          // Redirigir al login después de 1 segundo
          setTimeout(() => { 
            window.location.href = '/' 
          }, 1000)
        }
      }
    }
    return Promise.reject(error)
  }
)

// ============================================
// CONFIGURACIÓN DE EXPIRACIÓN DEL TOKEN
// ============================================
// La expiración del token se configura en DOS lugares:
//
// 1. BACKEND (auth.py) - Línea JWT_EXP_DELTA_SECONDS
//    Archivo: backend/auth.py
//    Variable: JWT_EXP_DELTA_SECONDS = 600  (10 minutos en segundos)
//    Esto determina cuánto tiempo es válido el token JWT
//
// 2. FRONTEND (este archivo) - Interceptor de respuesta
//    El interceptor detecta cuando el token expira (401)
//    y redirige al login automáticamente
// ============================================

export default axiosInstance
