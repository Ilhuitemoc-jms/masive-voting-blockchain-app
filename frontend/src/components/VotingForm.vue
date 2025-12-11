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
            Desde esta página puedes emitir tu voto encriptado para la votación actual. Para ello es necesario inicializar tu wallet para la red local. Recuerda que tu voto se emite con tecnología ethereum (local, servidor de la facultad) sobre cadenas de datos. En ningun momento se pide verificar datos o emitir comprobantes, si alguien te pide estos datos podrías ser victima de un fraude, comunicate al consejo estudiantil.
          </p>

          <!-- Sección de candidatos -->
          <div class="candidatos-container">
            <div 
              v-for="(candidato, index) in candidatos" 
              :key="index" 
              class="candidato-card"
            >
              <div class="candidato-imagen-container">
                <img 
                  :src="candidato.imagen" 
                  :alt="`Candidato ${candidato.numero}`"
                  class="candidato-imagen"
                />
              </div>
              <button 
                class="btn-votar"
                @click="emitirVoto(candidato.numero)"
              >
                Votar por:<br>
                {{ candidato.nombre || `Candidato ${candidato.numero}` }}
              </button>
            </div>
          </div>

        </div>
      </div>
    </template>
  </BaseLayout>
</template>

<script setup>
import { ref } from 'vue'
import BaseLayout from './BaseLayout.vue'
import '../scripts/login.js'

// Lista de candidatos con sus imágenes   
const candidatos = ref([
  { numero: 1, imagen: '/assets/Images/candidatos/1.jpg', nombre: 'Laura Susana Acosta Torres' },
  { numero: 2, imagen: '/assets/Images/candidatos/2.jpg', nombre: 'Sergio Manuel Alcocer Martínez de Castro' },
  { numero: 3, imagen: '/assets/Images/candidatos/3.jpg', nombre: 'Luis Agustín Álvarez Icaza Longoria' },
  { numero: 4, imagen: '/assets/Images/candidatos/4.jpg', nombre: 'Raúl Juan Contreras Bustamante' },
  { numero: 5, imagen: '/assets/Images/candidatos/5.jpg', nombre: 'Jorge Alfredo Cuéllar Ordaz' },
  { numero: 6, imagen: '/assets/Images/candidatos/6.jpg', nombre: 'Patricia Dolores Dávila Aranda' },
  { numero: 7, imagen: '/assets/Images/candidatos/7.jpg', nombre: 'Germán Fajardo Dolci' },
  { numero: 8, imagen: '/assets/Images/candidatos/8.jpg', nombre: 'Patricia Dolores Dávila Aranda' },
  { numero: 9, imagen: '/assets/Images/candidatos/9.jpg', nombre: 'Germán Fajardo Dolci' },
  { numero: 10, imagen: '/assets/Images/candidatos/10.jpg', nombre: 'Leonardo Lomelí Vanegas' },
  { numero: 11, imagen: '/assets/Images/candidatos/11.jpg', nombre: 'María Esperanza Martínez Romero' },
  { numero: 12, imagen: '/assets/Images/candidatos/12.jpg', nombre: 'Daniel Trejo Medina' },
  { numero: 10, imagen: '/assets/Images/candidatos/13.jpg', nombre: 'Imanol Ordorika Sacristán' },
  { numero: 11, imagen: '/assets/Images/candidatos/14.jpg', nombre: 'Guadalupe Valencia García' },
  { numero: 12, imagen: '/assets/Images/candidatos/15.jpg', nombre: 'Ambrosio Francisco Javier Velasco Gómez' },
  { numero: 10, imagen: '/assets/Images/candidatos/16.jpg', nombre: 'Luz del Carmen Alicia Vilchis Esquivel' },
  { numero: 11, imagen: '/assets/Images/candidatos/17.jpg', nombre: 'Domingo Alberto Vital Díaz' },
])

// Función para emitir voto
const emitirVoto = (numeroCandidato) => {
  const candidato = candidatos.value.find(c => c.numero === numeroCandidato)
  if (candidato) {
    console.log(`Voto emitido para: ${candidato.nombre || `Candidato ${candidato.numero}`}`)
    // Aquí puedes agregar la lógica para emitir el voto encriptado
  }
}
</script>

<style src="../styles/login.css"></style>

<style scoped>
.candidatos-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-top: 40px;
  padding: 20px 0;
}

.candidato-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.candidato-imagen-container {
  width: 50%;
  max-width: 200px;
  margin: 0 auto 15px auto;
  border: 3px solid #000;
  border-radius: 4px;
  overflow: hidden;
  background: #fff;
}

.candidato-imagen {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

.btn-votar {
  width: 100%;
  padding: 12px 20px;
  background-color: rgb(2, 44, 90);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: center;
}

.btn-votar:hover {
  background-color: rgb(2, 44, 90);
}

.btn-votar:active {
  background-color: rgb(2, 44, 90);
}


@media (max-width: 768px) {
  .candidatos-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .candidatos-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
