# Importacion de modulos para operaciones asincronas y peticiones HTTP
import asyncio
import aiohttp
import random
from datetime import datetime

# URL base de la API del sistema de votaciones
API_URL = 'http://localhost:8000/api'

# Catalogo de candidatos disponibles para el proceso electoral
CANDIDATOS = [
    {'numero': 1, 'nombre': 'Laura Susana Acosta Torres'},
    {'numero': 2, 'nombre': 'Sergio Manuel Alcocer Martínez de Castro'},
    {'numero': 3, 'nombre': 'Luis Agustín Álvarez Icaza Longoria'},
    {'numero': 4, 'nombre': 'Raúl Juan Contreras Bustamante'},
    {'numero': 5, 'nombre': 'Jorge Alfredo Cuéllar Ordaz'},
    {'numero': 6, 'nombre': 'Patricia Dolores Dávila Aranda'},
    {'numero': 7, 'nombre': 'Germán Fajardo Dolci'},
    {'numero': 8, 'nombre': 'Patricia Dolores Dávila Aranda'},
    {'numero': 9, 'nombre': 'Germán Fajardo Dolci'},
    {'numero': 10, 'nombre': 'Leonardo Lomelí Vanegas'},
    {'numero': 11, 'nombre': 'María Esperanza Martínez Romero'},
    {'numero': 12, 'nombre': 'Daniel Trejo Medina'},
    {'numero': 13, 'nombre': 'Imanol Ordorika Sacristán'},
    {'numero': 14, 'nombre': 'Guadalupe Valencia García'},
    {'numero': 15, 'nombre': 'Ambrosio Francisco Javier Velasco Gómez'},
    {'numero': 16, 'nombre': 'Luz del Carmen Alicia Vilchis Esquivel'},
    {'numero': 17, 'nombre': 'Domingo Alberto Vital Díaz'}
]

# Valores estaticos que se mantienen constantes para todos los votos
DATOS_ESTATICOS = {
    'precinct_medst': '0498 PEPPERWOOD',
    'precinct_cvr': '0498-00 WHITE | 0498-99 PLATINUM',
    'office': 'US PRESIDENT',
    'district': 'FEDERAL',
    'magnitude': '1',
    'party': None,
    'party_detailed': 'WRITEIN',
    'state': 'ARIZONA',
    'county': 'MARICOPA'
}

# Parametros de configuracion para el proceso de generacion masiva
CONFIG = {
    'VOTOS_POR_SEGUNDO': 5000,
    'DURACION_SEGUNDOS': 60,
    'CONCURRENCIA': 4000,
    'CVR_ID_INICIAL': 2599
}

# Variable global que almacena el token JWT de autenticacion
token_autenticacion = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjkyYTMyNzMyMWUwZDJmYTMxOWRjMjllIiwibm9fY3VlbnRhIjoiMzE3MDk5MDkwIiwiZXhwIjoxNzc0NTgwODc0LCJpYXQiOjE3NzM5ODA4NzR9.w47Vsw6FkdK3lszZcNq-nQf7uaGsgi_rLJzSnNwnRmI"
SPINNER_CHARS = ['◜', '◠', '◝', '◞', '◡', '◟']

async def autenticar(session):
    """
    Funcion asincrona que realiza la autenticacion en el sistema
    Parametro session: sesion de aiohttp reutilizable para todas las peticiones
    Retorna el token de autenticacion obtenido del servidor
    """
    global token_autenticacion
    
    # Datos de credenciales para el proceso de autenticacion
    credenciales = {
            "no_cuenta": "",
            "clave_elector": "MRSNIL00113009H700"
        }
    print(credenciales)
    try:
        # Peticion POST al endpoint de autenticacion
        async with session.post(f'{API_URL}/auth/login/', json=credenciales) as response:
            # Extraccion del token desde la respuesta JSON
            data = await response.json()
            token_autenticacion = data['token']
            print('Autenticacion exitosa', token_autenticacion)
            return token_autenticacion
    except Exception as e:
        print(f'Error en autenticacion: {e}')
        raise


def generar_datos_voto(contador):
    """
    Funcion que construye el objeto de datos de voto
    Parametro contador: identificador secuencial del voto
    Retorna diccionario con la informacion completa del voto
    """
    # Seleccion aleatoria de un candidato del catalogo
    candidato = random.choice(CANDIDATOS)
    
    # Construccion del objeto de voto con datos estaticos y dinamicos
    return {
        'cvr_id': CONFIG['CVR_ID_INICIAL'] + contador,
        **DATOS_ESTATICOS,
        'candidate': candidato['nombre'],
        'voting_hour': datetime.now().strftime('%H:%M:%S'),
        'candidato_id': candidato['numero']
    }


async def enviar_voto(session, numero_voto, semaforo):
    """
    Funcion asincrona que envia un voto individual a la API
    Parametro session: sesion HTTP reutilizable
    Parametro numero_voto: numero secuencial del voto para tracking
    Parametro semaforo: control de concurrencia mediante asyncio.Semaphore
    """
    # semaforo para control de concurrencia
    async with semaforo:
        # Generacion de datos aleatorios para este voto
        datos_voto = generar_datos_voto(numero_voto)
        
        # Headers de autenticacion con el token Bearer
        headers = {
            'Authorization': f'Bearer {token_autenticacion}',
            'Content-Type': 'application/json'
        }

        # Calculo del indice del caracter de animacion usando modulo
        spinner_index = numero_voto % len(SPINNER_CHARS)
        # Seleccion del caracter de carga correspondiente al voto actual
        loading_char = SPINNER_CHARS[spinner_index]
        
        try:
            # Peticion POST asincrona al endpoint de votos
            async with session.post(f'{API_URL}/votos/crear/', json=datos_voto, headers=headers) as response:
                # Verificacion de respuesta exitosa del servidor incluyendo procesamiento asincrono
                if response.status in [200, 201, 202]:
                    # Impresion completa en una sola linea que se sobrescribe continuamente
                    print(f'\r------- Generando registros {loading_char} ------- Voto número {numero_voto} -------', end='', flush=True)
    
        except Exception as e:
            # Impresion de error en una sola linea que se sobrescribe
            print(f'\r------- Error en generación {loading_char} ------- Voto {numero_voto}, error: {e} --------------------------', end='', flush=True)

async def generar_votos_masivos():
    """
    Funcion principal asincrona que coordina la generacion masiva de votos  
    Implementa control de concurrencia y reutilizacion de sesion HTTP
    """
    print('\n----- INICIANDO GENERACION MASIVA DE VOTOS -----\n')
    
    # Calculo del total de votos segun configuracion
    total_votos = CONFIG['VOTOS_POR_SEGUNDO'] * CONFIG['DURACION_SEGUNDOS']
    print(f'Objetivo: {total_votos:,} votos en {CONFIG["DURACION_SEGUNDOS"]} segundos')
    print(f'Tasa objetivo: {CONFIG["VOTOS_POR_SEGUNDO"]:,} votos/segundo')
    print(f'Concurrencia: {CONFIG["CONCURRENCIA"]} peticiones simultaneas\n')
    
    # Creacion de semaforo para control de concurrencia maxima
    semaforo = asyncio.Semaphore(CONFIG['CONCURRENCIA'])
    
    # Contexto de sesion HTTP reutilizable para todas las peticiones
    async with aiohttp.ClientSession() as session:
        # Autenticacion previa al inicio del proceso
        #await autenticar(session)
        
        # Registro del tiempo de inicio para metricas
        tiempo_inicio = asyncio.get_event_loop().time()
        
        # Creacion de lista de tareas asincronas para todos los votos
        tareas = [
            enviar_voto(session, i + 1, semaforo)
            for i in range(total_votos)
        ]
        
        # Ejecucion concurrente de todas las tareas
        await asyncio.gather(*tareas)
        
        # Calculo del tiempo total transcurrido
        tiempo_total = asyncio.get_event_loop().time() - tiempo_inicio
        tasa_promedio = int(total_votos / tiempo_total)
        
        # Reporte de metricas finales del proceso
        print('\n----- GENERACION COMPLETADA -----\n')
        print(f'Total enviados: {total_votos:,}')
        print(f'Tiempo total: {tiempo_total:.2f} segundos')
        print(f'Tasa promedio: {tasa_promedio:,} votos/segundo\n')


def main():
    """
    Funcion de entrada principal que ejecuta el event loop mediante asyncio.run
    """
    # Ejecucion automatica del event loop sin necesidad de gestion manual
    asyncio.run(generar_votos_masivos())

# Punto de entrada del script cuando se ejecuta directamente
if __name__ == '__main__':
    main()
