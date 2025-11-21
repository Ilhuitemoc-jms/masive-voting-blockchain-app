<template>
    <div id="contenedor">
      <!-- Header Section -->
      <div id="contenedor-sombras-encabezado">
        <div id="encabezado">
          <div class="header-content">
            <div class="logo-section">
              <img src="https://ext.same-assets.com/3488092952/858534190.png" alt="UNAM Logo" class="unam-logo">
              <div class="header-text">
                <div class="universidad-title">Universidad Nacional</div>
                <div class="universidad-subtitle">Autónoma de México</div>
              </div>
            </div>
            <div class="header-image">
              <img src="https://ext.same-assets.com/3488092952/1045554895.jpeg" alt="Campus">
            </div>
          </div>
        </div>
  
        <div id="navegacion">
          <a href="http://www.fciencias.unam.mx/contacto">
            <img src="https://ext.same-assets.com/3488092952/3251913114.png" alt="" class="nav-icon">
            Contacto
          </a>
          <span class="separator">|</span>
          <a href="http://www.fciencias.unam.mx/meta/SiteMap">
            <img src="https://ext.same-assets.com/3488092952/294742603.png" alt="" class="nav-icon">
            Mapa del sitio
          </a>
          <span class="separator">|</span>
          <a href="http://www.fciencias.unam.mx/directorio/busqueda">
            <img src="https://ext.same-assets.com/3488092952/1885359173.png" alt="" class="nav-icon">
            Directorio
          </a>
          <span class="separator">|</span>
          <a href="http://mail.ciencias.unam.mx" target="_blank">
            <img src="https://ext.same-assets.com/3488092952/258262300.png" alt="" class="nav-icon">
            Correo
          </a>
        </div>
      </div>
  
      <!-- Main Content -->
      <div id="contenido">
        <div id="topinterna">
          <span class="titulo-seccion">Acceso a Servicios en Línea</span>
          <div class="facultad-badge">
            <span class="facultad-text">Facultad de<br>Ciencias</span>
            <img src="https://ext.same-assets.com/3488092952/2258409634.png" alt="Escudo" class="escudo">
          </div>
        </div>
  
        <div class="info-estudiantes2">
          <form @submit.prevent="handleSubmit">
            <fieldset>
              <legend>Acceder</legend>
  
              <table class="form-table">
                <tr>
                  <td class="label-col">Nombre de Usuario:</td>
                  <td>
                    <input
                      v-model="username"
                      type="text"
                      class="form-control"
                      required
                    >
                  </td>
                </tr>
                <tr>
                  <td class="label-col">Contraseña:</td>
                  <td>
                    <input
                      v-model="password"
                      type="password"
                      class="form-control"
                      required
                    >
                  </td>
                </tr>
                <tr>
                  <td></td>
                  <td>
                    <button type="submit" class="btn-acceder">Acceder</button>
                    &nbsp;&nbsp;
                    <a href="#" @click.prevent="forgotPassword" class="forgot-link">Olvidé mi contraseña</a>
                  </td>
                </tr>
              </table>
            </fieldset>
          </form>
        </div>
      </div>
  
      <!-- Footer -->
      <div id="contenedor-sombras-pie">
        <div id="pie-banners">
          <div id="ciencias-en">
            Ciencias en:
            <a href="https://www.facebook.com/pages/Facultad-de-Ciencias/214278861928417">
              <img src="https://ext.same-assets.com/3488092952/3324920221.png" alt="Facebook" class="social-icon">
              Facebook
            </a>
            <a href="http://twitter.com/#!/fciencias">
              <img src="https://ext.same-assets.com/3488092952/148237705.png" alt="Twitter" class="social-icon">
              Twitter
            </a>
            <a href="http://www.youtube.com/user/unamciencias">
              <img src="https://ext.same-assets.com/3488092952/1059289793.jpeg" alt="Youtube" class="social-icon">
              Youtube
            </a>
          </div>
        </div>
      </div>
  
      <div id="pie-derechos">
        <p>
          Hecho en México, todos los derechos reservados 2011-2016. Esta página puede ser reproducida con fines no lucrativos,
          siempre y cuando no se mutile, se cite la fuente completa y su dirección electrónica. De otra forma requiere permiso
          previo por escrito de la Institución.
        </p>
        <p class="administrado">
          Sitio web administrado por la Coordinación de los Servicios de Cómputo de la Facultad de Ciencias. ¿Dudas?, ¿comentarios?.
          <a href="mailto:webmaster@ciencias.unam.mx">Escribenos</a>.
          <a href="http://www.fciencias.unam.mx/Privacidad.pdf">Aviso de privacidad</a>.
        </p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const username = ref('')
  const password = ref('')
  
  const handleSubmit = () => {
    if (!username.value) {
      alert('Tiene que ingresar un valor para Nombre de Usuario.')
      return
    }
  
    if (!password.value) {
      alert('Tiene que ingresar un valor para Contraseña.')
      return
    }
  
    // Aquí conectarás con tu backend
    console.log('Login attempt:', {
      username: username.value,
      password: '***hidden***'
    })
  
    alert(`Datos capturados:\nUsuario: ${username.value}\n\nConecta aquí tu backend.`)
  }
  
  const forgotPassword = () => {
    alert('Redirigir a recuperación de contraseña')
  }
  </script>
  
  <style scoped>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  #contenedor {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    font-family: Arial, Helvetica, sans-serif;
    background: white;
  }
  
  /* Header */
  #contenedor-sombras-encabezado {
    width: 100%;
  }
  
  #encabezado {
    background-color: #2d5d8f;
    height: 100px;
    width: 100%;
  }
  
  .header-content {
    display: flex;
    height: 100%;
    align-items: center;
    justify-content: space-between;
  }
  
  .logo-section {
    display: flex;
    align-items: center;
    padding-left: 20px;
    gap: 15px;
    z-index: 2;
  }
  
  .unam-logo {
    height: 70px;
    width: auto;
  }
  
  .header-text {
    color: #f4d03f;
  }
  
  .universidad-title {
    font-size: 22px;
    font-weight: normal;
    line-height: 1.1;
  }
  
  .universidad-subtitle {
    font-size: 18px;
    font-weight: normal;
  }
  
  .header-image {
    height: 100%;
    flex: 1;
    overflow: hidden;
    display: flex;
    justify-content: flex-end;
  }
  
  .header-image img {
    height: 100%;
    width: auto;
    object-fit: cover;
  }
  
  /* Navigation */
  #navegacion {
    background-color: #f4d03f;
    padding: 6px 20px;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
  }
  
  #navegacion a {
    color: #2d5d8f;
    text-decoration: none;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  
  #navegacion a:hover {
    text-decoration: underline;
  }
  
  .nav-icon {
    height: 14px;
    width: 14px;
  }
  
  .separator {
    color: #2d5d8f;
    margin: 0 2px;
  }
  
  /* Main Content */
  #topinterna {
    background: linear-gradient(to bottom, #4a6d8c, #5a7d9c);
    color: white;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .titulo-seccion {
    font-size: 24px;
    font-weight: normal;
  }
  
  .facultad-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: rgba(255, 255, 255, 0.15);
    padding: 5px 12px;
    border-radius: 3px;
  }
  
  .facultad-text {
    font-size: 12px;
    line-height: 1.3;
    text-align: right;
  }
  
  .escudo {
    height: 35px;
  }
  
  /* Form */
  .info-estudiantes2 {
    padding: 40px 20px;
    background: #f5f5f5;
    min-height: 300px;
  }
  
  form {
    max-width: 700px;
    margin: 0 auto;
  }
  
  fieldset {
    border: 1px solid #ccc;
    padding: 25px 30px;
    background: white;
    border-radius: 2px;
  }
  
  legend {
    padding: 0 10px;
    font-weight: bold;
    font-size: 14px;
    color: #333;
  }
  
  .form-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .form-table tr {
    height: 45px;
  }
  
  .label-col {
    text-align: right;
    padding-right: 15px;
    width: 200px;
    font-size: 13px;
    color: #333;
  }
  
  .form-control {
    width: 300px;
    padding: 5px 8px;
    border: 1px solid #ccc;
    font-size: 13px;
    font-family: Arial, Helvetica, sans-serif;
    border-radius: 2px;
  }
  
  .form-control:focus {
    outline: none;
    border-color: #2d5d8f;
  }
  
  .btn-acceder {
    background-color: #2d5d8f;
    color: white;
    border: none;
    padding: 6px 18px;
    font-size: 13px;
    cursor: pointer;
    border-radius: 2px;
    font-weight: bold;
  }
  
  .btn-acceder:hover {
    background-color: #234a6d;
  }
  
  .forgot-link {
    color: #2d5d8f;
    text-decoration: none;
    font-size: 12px;
  }
  
  .forgot-link:hover {
    text-decoration: underline;
  }
  
  /* Footer */
  #contenedor-sombras-pie {
    margin-top: 0;
  }
  
  #pie-banners {
    background: linear-gradient(to bottom, #4a6d8c, #2d5d8f);
    padding: 12px 20px;
    text-align: center;
  }
  
  #ciencias-en {
    color: white;
    font-size: 12px;
  }
  
  #ciencias-en a {
    color: white;
    text-decoration: none;
    margin: 0 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  
  #ciencias-en a:hover {
    text-decoration: underline;
  }
  
  .social-icon {
    height: 14px;
    width: 14px;
  }
  
  #pie-derechos {
    background-color: #e8f0f5;
    padding: 20px 30px;
    font-size: 10px;
    color: #555;
    text-align: center;
    line-height: 1.6;
  }
  
  #pie-derechos p {
    margin-bottom: 8px;
  }
  
  .administrado {
    margin-top: 10px;
  }
  
  #pie-derechos a {
    color: #2d5d8f;
    text-decoration: none;
  }
  
  #pie-derechos a:hover {
    text-decoration: underline;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      height: auto;
    }
  
    .header-image {
      width: 100%;
      height: 60px;
    }
  
    #topinterna {
      flex-direction: column;
      gap: 10px;
      text-align: center;
    }
  
    .form-table tr {
      display: flex;
      flex-direction: column;
      height: auto;
      margin-bottom: 15px;
    }
  
    .label-col {
      text-align: left;
      padding-right: 0;
      width: 100%;
      margin-bottom: 5px;
    }
  
    .form-control {
      width: 100%;
    }
  }
  </style>
  