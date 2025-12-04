/**
 * Módulo de autenticación para la aplicación de votación
 * Usa JWT para autenticación con el backend
 */
import axiosInstance from '../axiosConfig'

/**
 * Realiza el login del usuario contra el backend
 * @param {string} no_cuenta - Número de cuenta del usuario
 * @param {string} clave_elector - Clave de elector del usuario
 * @returns {Promise<Object>} - Objeto con success, token y user_id o error
 */
export async function loginUsuario(no_cuenta, clave_elector) {
  try {
    // Preparar datos para el backend
    // El backend espera: no_cuenta y clave_elector
    const data = {
      no_cuenta: no_cuenta,
      clave_elector: clave_elector
    }

    // Realizar petición POST al endpoint de login
    const response = await axiosInstance.post('login/', data)

    // Verificar respuesta exitosa
    if (response.data.success) {
      // Guardar token y datos en localStorage
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user_id', response.data.user_id)
      
      return {
        success: true,
        token: response.data.token,
        user_id: response.data.user_id
      }
    } else {
      return {
        success: false,
        error: response.data.error || 'Error en el inicio de sesión'
      }
    }
  } catch (error) {
    console.error('Error en login:', error)
    
    // Manejar errores de la respuesta
    let errorMessage = 'Error en el inicio de sesión. Por favor, intente de nuevo.'
    
    if (error.response && error.response.data) {
      errorMessage = error.response.data.error || 
                     error.response.data.message || 
                     errorMessage
      
      // Si hay errores de validación específicos
      if (error.response.data.errors) {
        const errors = error.response.data.errors
        const errorList = Object.values(errors).flat()
        errorMessage = errorList.join('. ')
      }
    }
    
    return {
      success: false,
      error: errorMessage
    }
  }
}

/**
 * Cierra la sesión del usuario
 */
export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  window.location.href = '/'
}

/**
 * Verifica si el usuario está autenticado
 * @returns {boolean} - true si hay token válido
 */
export function isAuthenticated() {
  const token = localStorage.getItem('token')
  return !!token
}

/**
 * Obtiene el token actual
 * @returns {string|null} - Token JWT o null
 */
export function getToken() {
  return localStorage.getItem('token')
}

/**
 * Obtiene el user_id actual
 * @returns {string|null} - user_id o null
 */
export function getUserId() {
  return localStorage.getItem('user_id')
}
