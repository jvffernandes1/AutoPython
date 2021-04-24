# Desenvolvido por: João Victor Franco Fernandes (joao.fernandes@unesp.br)
# Para utilizar o script é necessário ter o Google Chrome instalado no computador: https://www.google.com/intl/pt-BR/chrome/
# Para utilizar o script é necessário ter o chromedriver de mesma versão do Google Chrome na pasta do script: https://chromedriver.chromium.org/downloads

from selenium import webdriver
import time
import math

email = ""  # Coloque aqui seu email entre aspas
senha = ""  # Coloque aqui sua senha entre aspas
timer = 1  # Tempo de espera em segundos, se sua internet for lenta, aumente esse número.

driver = webdriver.Chrome()
# Página de login ------------------------------------------------------------------------------------------------------
driver.get('https://sistemas.unesp.br/central/#/sistemas')
driver.find_element_by_xpath('//*[@id="input_0"]').send_keys(email)
driver.find_element_by_xpath('//*[@id="input_1"]').send_keys(senha)
driver.find_element_by_xpath('//*[@id="form"]/md-card/button').click()
# Página incial do sistema ---------------------------------------------------------------------------------------------
time.sleep(timer)
driver.find_element_by_xpath('//*[@id="content"]/md-content/md-grid-list/md-grid-tile[1]/figure/a').click()
# Sisgrad --------------------------------------------------------------------------------------------------------------
time.sleep(timer)
driver.find_element_by_xpath('//*[@id="menuesq"]/li[8]/a').click()
driver.find_element_by_xpath('//*[@id="menuesq"]/li[8]/ul/li[1]/a').click()
# Mensagens recebidas --------------------------------------------------------------------------------------------------
msg_totais_txt = driver.find_element_by_xpath('//*[@id="form_mensagens"]/div/span[1]').text.split(" ")
msg_totais_int = int(msg_totais_txt[0].replace(".", ""))
pag_totais = math.ceil(msg_totais_int / 20)

for y in range(1, pag_totais+1):
    driver.get('https://sistemas.unesp.br/academico/mensagem.listar.action?emailTipo=recebidas&d-4827107-p=' + str(y))
    for x in range(1, 20):
        time.sleep(timer)
        driver.find_element_by_xpath('//*[@id="destinatario"]/tbody/tr[' + str(x) + ']/td[4]/a').click()
        time.sleep(timer)
        driver.get('https://sistemas.unesp.br/academico/mensagem.listar.action?emailTipo=recebidas&d-4827107-p='+str(y))
    time.sleep(timer)
