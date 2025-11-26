<template>
  <BaseLayout>
    <!-- Aquí se encuentra el titulo de la página -->
    <template #section-title>
      Aplicaciones
    </template>
    <!-- Aquí está el contenido de la página - contenido de login.html -->
    <template #content>
      <!-- Contenedor con sidebar + contenido -->
      <div class="info-estudiantes">
        <!-- Sidebar izquierda -->
        <div id="menu-interna">
          <ul id="navmenu-v">
            <li>
              <h2><a href="#" @click.prevent>Comunidad</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Licenciatura</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Docencia</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Investigación</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Posgrado</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Extensión</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Servicios</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Nosotros</a></h2>
            </li>
            <li>
              <h2><a href="#" @click.prevent>Eventos</a></h2>
            </li>
          </ul>
        </div>

        <!-- Contenido principal -->
        <div id="info-contenido h2">
          <div id="apps-container">
            <!-- Columna izquierda -->
            <div class="apps">
              <h3>Académico</h3>
              <ul>
                <li>
                  <a href="#" @click.prevent>Registro de Ayudantes 2026-2</a>
                  <p>Consulta requisitos para ser contratado como ayudante</p>
                </li>
              </ul>
              
              <h3>Correo @ciencias</h3>
              <ul>
                <li>
                  <a href="#" @click.prevent>Cambio de contraseña</a>
                  <p>Actualiza la contraseña de tu correo</p>
                </li>
                <li>
                  <a href="#" @click.prevent>Cambio de nombre</a>
                  <p>Actualiza el nombre de usuario de tu correo</p>
                </li>
              </ul>
              
              <h3>Datos Personales</h3>
              <ul>
                <li>
                  <a href="#" @click.prevent>Contacto</a>
                  <p>Actualiza tus datos de contacto</p>
                </li>
                <li>
                  <a href="#" @click.prevent>Datos Médicos</a>
                  <p>Actualiza tus datos médicos</p>
                </li>
                <li>
                  <a href="#" @click.prevent>Domicilio</a>
                  <p>Actualiza los datos de tu domicilio</p>
                </li>
                <li>
                  <a href="#" @click.prevent>Género e Identidad</a>
                  <p>Actualiza tu(s) pronombre(s) o nombre social</p>
                </li>
              </ul>
              
              <h3>Directorio</h3>
              <ul>
                <li>
                  <a href="#" @click.prevent>Directorio</a>
                  <p>Búsqueda en el directorio</p>
                </li>
              </ul>
            </div>

            <!-- Columna derecha -->
            <div class="apps-alt">
              <h3>Estudiante</h3>
              <ul>
                <li>
                  <a href="#" @click.prevent>Historial</a>
                  <p>Consulta tu Historial Académico</p>
                </li>
                <li>
                  <a href="#" @click.prevent>Horario</a>
                  <p>Consulta tu Horario</p>
                </li>
                <li>
                  <a href="#" @click.prevent>Inscripción</a>
                  <p>Consulta tu Inscripción</p>
                </li>
              </ul>
              
              <h3>Mi cuenta</h3>
              <ul>
                <li>
                  <a href="#" @click.prevent>Preferencias</a>
                  <p>Actualiza tu contraseña y cuenta de correo</p>
                </li>
              </ul>
              
              <h3>Votaciones</h3>
              <ul>
                <li>
                  <a href="/voting">Formulario</a>
                  <p>Ingresa para participar en la votación activa</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </template>
  </BaseLayout>
</template>

<script setup>
import BaseLayout from './BaseLayout.vue'
import '../scripts/login.js'
</script>

<style src="../styles/login.css"></style>
