import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Configurações do Selenium
chrome_driver_path = ()  # Defina o caminho para o chromedriver
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Para execução em segundo plano
service = ChromeService(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL da página que você deseja acessar
url = 'https://exemplo.com/sua_pagina'

# Navegue até a página
driver.get(url)

# Localize as tabelas na página usando diferentes métodos de localização
tables_by_tag = driver.find_elements(By.TAG_NAME, 'table')
tables_by_id = driver.find_elements(By.ID, 'id_da_tabela')
tables_by_class = driver.find_elements(By.CLASS_NAME, 'classe_da_tabela')
tables_by_xpath = driver.find_elements(By.XPATH, '//*[@id="tabela"]')
tables_by_link_text = driver.find_elements(By.LINK_TEXT, 'Texto do Link')
tables_by_css_selector = driver.find_elements(By.CSS_SELECTOR, 'seletor_css')
tables_by_name = driver.find_elements(By.NAME, 'nome_da_tabela')

# Defina o diretório para salvar as planilhas Excel
output_dir = 'pasta_para_salvar_as_planilhas'
os.makedirs(output_dir, exist_ok=True)

# Salve cada tabela em uma planilha Excel separada
for index, table in enumerate(tables_by_tag):
    table_data = []
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
        table_data.append(row_data)

    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    excel_file_path = os.path.join(output_dir, f'tabela_{index}.xlsx')
    df.to_excel(excel_file_path, index=False)

# Feche o navegador
driver.quit()

# Baixe imagens do site e salve-as em uma pasta
# Certifique-se de ter criado a pasta "IMAGENS_BAIXADAS" antes de executar o código
image_elements = driver.find_elements(By.TAG_NAME, 'img')
image_folder = 'IMAGENS_BAIXADAS'

os.makedirs(image_folder, exist_ok=True)

for index, image_element in enumerate(image_elements):
    image_url = image_element.get_attribute('src')
    if image_url:
        image_name = f'image_{index}.jpg'
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_element.screenshot_as_png)

# Feche o navegador novamente (caso você não tenha feito isso antes)
driver.quit()
