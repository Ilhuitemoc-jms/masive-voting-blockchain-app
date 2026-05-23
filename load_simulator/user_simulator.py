# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 17:40:58 2024

@author: yisus
"""

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)

# options.add_argument("headless")  # Ejecutar en modo headless
# options.add_argument("disable-gpu")  # Desactivar la GPU para mejor rendimiento en headless

# Configurar el navegador
driver = webdriver.Edge(options=options)

# Lista para almacenar los URLs
URLS = []
CLAVES = []

#dataframe con toda la información que se vaya recopilando
tabla_total = pd.DataFrame()

#tiempo de espera máximo para que el navegador obtenga la información que se le pide
wait = WebDriverWait(driver, 59)  # Espera hasta 59 segundos

# Construir la URL de la página actual
url_pagina = f"http://localhost:5173" #f"https://www.biva.mx/empresas/emisoras_inscritas/emisoras_inscritas?instrumento=null&tipo_valor=null&sector=null&sub_sector=null&ramo=null&sub_ramo=null&emisora_id=null&clave=null&canceladas=false&biva=false&subTab=null&page={pagina}"

# Ir a la página
driver.get(url_pagina)

