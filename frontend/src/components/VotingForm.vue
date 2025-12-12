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
            La <strong>Universidad Nacional Autonoma de México</strong> a través de la Junta de Gobierno y en virtud del <strong> Artículo 6 en su fracción I de la Ley Orgánica</strong>,
            inicia formalmente el procedimiento para nombrar a la persona titular de la Rectoría de la Universidad para el periodo <strong> 2023-2027.</strong><br>
            <br>Esta página estará habilitado desde los portales propietarios de todas las Facultades, Institutos, Posgrados, ENES y Organismos que integran a la Universidad.
            <h3>
              <strong> Instrucciones: </strong>
            </h3>
            <ul style="margin-left: 40px;">
               <li>En las siguientes líneas encontrarás a los candidatos por la rectoría de la Universidad, porfavor selecciona el de tu preferencia dando click encima de el botón <strong> "Votar por: *CANDIDATO*"</strong></li>
              <br>  <li>Medita correctamente tu opción antes de enviarla ya que solo se podrá acceder a este sitio una única vez. </li>
              <br>  <li>Una vez emitido tú botón aparecerá la imagen de tu candidato seleccionado en verde con la leyenda <br> <strong>Voto registrado correctamente para:</strong></li>
            </ul>
            
          </p>

          <p style="text-align: center;"> <strong> Disponible desde las 8:00 horas hasta las 20:00 horas del día 1ero de noviembre del 2023. </strong></p>

          <!-- Vista de voto exitoso -->
          <div v-if="votoExitoso && candidatoVotado" class="voto-exitoso-container">
            <div class="voto-exitoso-card">
              <div class="candidato-imagen-container-exitoso">
                <img 
                  :src="candidatoVotado.imagen" 
                  :alt="`Candidato ${candidatoVotado.numero}`"
                  class="candidato-imagen-exitoso"
                />
              </div>
              <div class="mensaje-exitoso">
                <span class="icono-check">🗳️</span>
                <p class="texto-confirmacion">Voto registrado correctamente para:</p>
                <p class="nombre-candidato">{{ candidatoVotado.nombre }}</p>
              </div>
            </div>
          </div>

          <!-- Vista normal: selección de candidatos -->
          <template v-else>
            <!-- Mensaje de error (solo errores, éxito se muestra arriba) -->
            <div v-if="mensaje && tipoMensaje === 'error'" class="mensaje-estado error">
              {{ mensaje }}
            </div>

            <!-- Sección de candidatos -->
            <div class="candidatos-container">
              <div v-for="(candidato, index) in candidatos" :key="index" class="candidato-card">
                <div class="candidato-imagen-container">
                  <!-- Estilo particular para la imagen 18 para que encaje con todas las demas -->
                  <img :src="candidato.imagen" :alt="`Candidato ${candidato.numero}`" class="candidato-imagen" 
                  :style="candidato.numero === 18 ? { 
                        width: '88px', 
                        height: '118px',
                      } : {}"/>
                </div>
                <button class="btn-votar" :disabled="enviandoVoto" @click="emitirVoto(candidato.numero)" >
                  <template v-if="enviandoVoto">
                    Enviando voto...
                  </template>
                  <template v-else>
                    Votar por:<br>
                    {{ candidato.nombre || `Candidato ${candidato.numero}` }}
                  </template>
                </button>
              </div>
            </div>
          </template>

          <p>Desde esta página puedes emitir tu voto para la votación para Rector. Para ello es necesario inicializar tu wallet-unam para la red local de la universidad <br>
            <br>Recuerda que tu voto se emite con encriptación AES-256 y firma electronica Ed25519, además de procesarse en la Red Local (local, nodo UNAM) sobre cadenas de datos. <br>
            En ningun momento se pide verificar datos o emitir comprobantes, si alguien te pide esta información podrías ser victima de un fraude, comunicate con nosotros al departamento de seguridad informatica de la Universidad a tráves de este <a href="https://www.seguridad.unam.mx/incidentes">Link</a> 
            o escribenos una un correo a <a href="csi.incidentes@unam.mx">csi.incidentes@unam.mx</a> <br>
          </p>

          <p style="text-align: center;"> 
            Proceso con validez institucional, respaldado en la normativa de la Universidad Nacional Autonoma de Méxio, <strong> Artículo 6, fracción I de la Ley Orgánica; artículo 16 del Reglamento Interior de la Junta de Gobierno; artículo 9 del Reglamento Interior de la Junta de Gobierno; artículo 9 de la Ley Orgánica; y artículo 30 del Estatuto General.</strong>
          </p>

        </div>
      </div>
    </template>
  </BaseLayout>
</template>

<script setup>
import { ref } from 'vue'
import BaseLayout from './BaseLayout.vue'
import axiosInstance from '../axiosConfig.js'
import '../scripts/login.js'

// Estado para mostrar mensajes al usuario
const mensaje = ref('')
const tipoMensaje = ref('') // 'success' o 'error'
const enviandoVoto = ref(false)
const votoExitoso = ref(false)
const candidatoVotado = ref(null)

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
  { numero: 13, imagen: '/assets/Images/candidatos/13.jpg', nombre: 'Imanol Ordorika Sacristán' },
  { numero: 14, imagen: '/assets/Images/candidatos/14.jpg', nombre: 'Guadalupe Valencia García' },
  { numero: 15, imagen: '/assets/Images/candidatos/15.jpg', nombre: 'Ambrosio Francisco Javier Velasco Gómez' },
  { numero: 16, imagen: '/assets/Images/candidatos/16.jpg', nombre: 'Luz del Carmen Alicia Vilchis Esquivel' },
  { numero: 17, imagen: '/assets/Images/candidatos/17.jpg', nombre: 'Domingo Alberto Vital Díaz' },
  { numero: 18, imagen: '/assets/Images/candidatos/18.jpg', nombre: 'ANULAR VOTO' },
])

// Función para emitir voto
const emitirVoto = async (numeroCandidato) => {
  const candidato = candidatos.value.find(c => c.numero === numeroCandidato)
  if (!candidato) return

  // Evitar múltiples envíos
  if (enviandoVoto.value) return
  enviandoVoto.value = true
  mensaje.value = ''

  // Datos del voto (hardcodeados para prueba, solo cambia candidato_id)
  const datosVoto = {
    cvr_id: 2599,
    precinct_medst: "0498 PEPPERWOOD",
    precinct_cvr: "0498-00 WHITE | 0498-99 PLATINUM",
    office: "US PRESIDENT",
    district: "FEDERAL",
    candidate: candidato.nombre || `Candidato ${candidato.numero}`,
    magnitude: "1",
    party: null,
    party_detailed: "WRITEIN",
    state: "ARIZONA",
    county: "MARICOPA",
    voting_hour: new Date().toLocaleTimeString('en-GB'),
    candidato_id: numeroCandidato
  }

  try {
    console.log(`Enviando voto para: ${candidato.nombre || `Candidato ${candidato.numero}`}`)
    
    const response = await axiosInstance.post('votos/crear/', datosVoto)
    
    if (response.data.success) {
      mensaje.value = `Voto registrado correctamente para:\n${candidato.nombre}`
      tipoMensaje.value = 'success'
      votoExitoso.value = true
      candidatoVotado.value = candidato
      console.log('Voto enviado exitosamente:', response.data)
    } else {
      mensaje.value = `Error: ${response.data.error || 'No se pudo registrar el voto'}`
      tipoMensaje.value = 'error'
    }
  } catch (error) {
    console.error('Error al enviar voto:', error)
    const errorMsg = error.response?.data?.error || error.message || 'Error de conexión'
    mensaje.value = `Error: ${errorMsg}`
    tipoMensaje.value = 'error'
  } finally {
    enviandoVoto.value = false
  }
}
</script>

<style src="../styles/login.css"></style>

<style scoped>
/* ===== VISTA DE VOTO EXITOSO ===== */
.voto-exitoso-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding: 20px;
}

.voto-exitoso-card {
  display: flex;
  align-items: center;
  gap: 40px;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 2px solid #28a745;
  border-radius: 16px;
  padding: 40px 50px;
  box-shadow: 0 8px 24px rgba(40, 167, 69, 0.2);
  max-width: 700px;
}

.candidato-imagen-container-exitoso {
  flex-shrink: 0;
  width: 120px;
  border: 3px solid #28a745;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.candidato-imagen-exitoso {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

.mensaje-exitoso {
  text-align: left;
}

.icono-check {
  font-size: 48px;
  display: block;
  margin-bottom: 10px;
}

.texto-confirmacion {
  font-size: 18px;
  color: #155724;
  margin: 0 0 8px 0;
  font-weight: 500;
}

.nombre-candidato {
  font-size: 24px;
  color: #155724;
  margin: 0;
  font-weight: 700;
}

/* ===== MENSAJES DE ESTADO ===== */
.mensaje-estado {
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: 500;
  text-align: center;
}

.mensaje-estado.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.mensaje-estado.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.btn-votar:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.7;
}

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

@media (max-width: 768px) {
  .voto-exitoso-card {
    flex-direction: column;
    text-align: center;
    padding: 30px;
    gap: 25px;
  }
  
  .mensaje-exitoso {
    text-align: center;
  }
  
  .candidato-imagen-container-exitoso {
    width: 100px;
  }
}

@media (max-width: 480px) {
  .candidatos-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .voto-exitoso-card {
    padding: 25px 20px;
  }
  
  .nombre-candidato {
    font-size: 20px;
  }
  
  .candidato-imagen-container-exitoso {
    width: 90px;
  }
}
</style>
