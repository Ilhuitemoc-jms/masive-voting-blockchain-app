<template>
  <BaseLayout>
    <!-- Aquí se encuentra el titulo de la página -->
    <template #section-title>
      Votación Encriptada
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
        <div id="info-contenido">
          <h1>
            Papeleta Digital
          </h1>
          <p> 
            Desde esta página puedes emitir tu voto encriptado para la votación actual. Para ello es necesario inicializar tu extensión ganache. Recuerda que tu voto se emite con tecnología ethereum (local, servidor de la facultad) sobre cadenas de datos. En ningun momento se pide verificar datos o emitir comprobantes, si alguien te pide estos datos podrías ser victima de un fraude, comunicate al consejo estudiantil.
          </p>

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
