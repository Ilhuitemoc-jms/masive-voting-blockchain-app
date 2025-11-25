const axiosInstance = axios.create({
  baseURL: `${base_url}api/`,
  withCredentials: true
})

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      if (error.response.status === 401 && (error.response.data.message === 'Token expired' || error.response.data.message === 'Invalid token')) {
        localStorage.removeItem('token')
        document.cookie = 'auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
        setTimeout(() => { window.location.href = '/login' }, 1000)
      } else if (error.response.status === 403) {
        //setTimeout(() => {window.location.href = '/'}, 3000)
      }
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
