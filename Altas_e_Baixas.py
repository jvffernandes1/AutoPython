#!pip install python-telegram-bot
#!pip install Unidecode

import telegram
import requests
import unidecode

from bs4 import BeautifulSoup as bs
from PIL import Image, ImageDraw, ImageFont

# CORES DO CÓDIGO ( MARKETING, ALTERAR AQUI!!!! ) ---------------------------------------------------------------------

bg_sq_altas = "#213f3f"     # Cor de fundo do quadrado para o "Altas do dia"
bg_sq_baixas = "#213f3f"    # Cor de fundo do quadrado para o "Baixas do dia"
telegram_bot_token = ""     # Coloque aqui o TOKEN do seu bot no telegram!

# CONSTANTES DO CÓDIGO -------------------------------------------------------------------------------------------------
server_path = ""                                                                              # path padrão do servidor
server_ip = ""                                                                                # ip padrão do servidor
server_links = ""                                                                             # linktree da API

raw_altas = server_path + "res/raw_imgs/Altas.jpg"                  # Raw Altas
raw_baixas = server_path + "res/raw_imgs/Baixas.jpg"                # Raw Baixas
raw_volume = server_path + "res/raw_imgs/Volume.jpg"                # RAW Volume

font_use = server_path + "res/Montserrat-Medium.ttf"                # Font Basis
font_black = server_path + "res/Montserrat-Medium.ttf"              # Font Black

path_altas = server_path + "res/rdy_imgs/Altas.jpg"                 # Path Altas diárias
path_baixas = server_path + "res/rdy_imgs/Baixas.jpg"               # Path Baixas diárias
path_volume = server_path + "res/rdy_imgs/Volume.jpg"               # Path Volume diário

path_morning = server_path + "res/rdy_imgs/morning_call.jpg"        # Path Morning Call

st_font = "https://economia.uol.com.br/cotacoes/bolsas/"            # Primeira fonte de informações
nd_font = "https://statusinvest.com.br/acoes/"                      # Segunda fonte de informações


# FUNÇÕES GLOBAIS ------------------------------------------------------------------------------------------------------
altas_name = []                                                     # Nome da ação em ALTA
altas_tick = []                                                     # TICK da ação em ALTA
altas_dif = []                                                      # Diferença da ação em ALTA
altas_value = []                                                    # Valor da ação em ALTA

baixas_name = []                                                    # Nome da ação em BAIXA
baixas_tick = []                                                    # TICK da ação em BAIXA
baixas_dif = []                                                     # Diferença da ação em BAIXA
baixas_value = []                                                   # Valor da ação em BAIXA

volume_name = []                                                    # Nome da ação em VOLUME
volume_tick = []                                                    # TICK da ação de VOLUME
volume_dif = []                                                     # Diferença da ação em VOLUME
volume_value = []                                                   # Valor da ação em VOLUME


# FUNÇÃO QUE ENVIA AS IMAGENS PRODUZIDAS PARA O CHAT NO TELEGRAM -------------------------------------------------------
def clear_title(titulo):
    while len(titulo) > 28:
        titulo = " ".join(titulo.split(" ")[0:-1])
    return titulo


def telegram_send_altas_baixas():
    bot = telegram.Bot(token=telegram_bot_token)
    bot.send_message(chat_id=-321365751, text="Boa tarde, aqui vai o resumo de Altas e Baixas!")
    bot.send_photo(chat_id='-321365751', photo=open(path_altas, 'rb'))
    bot.send_photo(chat_id='-321365751', photo=open(path_baixas, 'rb'))
    # bot.send_photo(chat_id='-321365751', photo=open(path_volume, 'rb'))
    bot.send_message(chat_id=-321365751, text="Acesse o servidor aqui (com a conta da Liga): "+server_links)


def telegram_send_morning():
    bot = telegram.Bot(token=telegram_bot_token)
    bot.send_message(chat_id=-321365751, text="Boa tarde, aqui vai o Morning Call!")
    bot.send_photo(chat_id='-321365751', photo=open(path_morning, 'rb'))
    bot.send_message(chat_id=-321365751, text="Acesse o servidor aqui: " + " #MANUTENÇÃO#")  # server_links)


def get_altas():
    page = requests.get(st_font)
    soup = bs(page.content, 'html.parser')
    results = soup.find_all('tr', {'class': 'dadosRankings'})

    for x in range(5):
        ticker = results[x].text.partition(".SA")
        altas_tick.append(unidecode.unidecode(ticker[0]))

        dif = results[x].text.partition(".SA")
        dif2 = dif[2].partition("R")
        altas_dif.append(unidecode.unidecode(dif2[0]))

        value = results[x].text.partition("%")
        altas_value.append(unidecode.unidecode(value[2]))

    for y in range(5):
        googled = requests.get(nd_font+altas_tick[y])
        goog_soup = bs(googled.content, 'html.parser')
        goog_result = goog_soup.find('span', {'class': 'd-block fw-600 text-main-green-dark'})
        altas_name.append(unidecode.unidecode(goog_result.text))

    print(altas_name)
    print(altas_tick)
    print(altas_dif)
    print(altas_value)


def get_baixas():
    page = requests.get(st_font)
    soup = bs(page.content, 'html.parser')
    results = soup.find_all('tr', {'class': 'dadosRankings'})

    for x in range(5, 10):
        ticker = results[x].text.partition(".SA")
        baixas_tick.append(unidecode.unidecode(ticker[0]))

        dif = results[x].text.partition(".SA")
        dif2 = dif[2].partition("R")
        baixas_dif.append(unidecode.unidecode(dif2[0]))

        value = results[x].text.partition("%")
        baixas_value.append(unidecode.unidecode(value[2]))

    for y in range(5):
        googled = requests.get(nd_font+baixas_tick[y])
        goog_soup = bs(googled.content, 'html.parser')
        goog_result = goog_soup.find('span', {'class': 'd-block fw-600 text-main-green-dark'})
        baixas_name.append(unidecode.unidecode(goog_result.text))

    print(baixas_name)
    print(baixas_tick)
    print(baixas_dif)
    print(baixas_value)


def get_volume():
    page = requests.get(st_font)
    soup = bs(page.content, 'html.parser')
    results = soup.find_all('tr', {'class': 'dadosRankings'})

    for x in range(10, 15):
        ticker = results[x].text.partition(".SA")
        volume_tick.append(unidecode.unidecode(ticker[0]))

        dif = results[x].text.partition(".SA")
        dif2 = dif[2].partition("R")
        volume_dif.append(unidecode.unidecode(dif2[0]))

        value = results[x].text.partition("%")
        volume_value.append(unidecode.unidecode(value[2]))

    for y in range(5):
        googled = requests.get(nd_font+volume_tick[y])
        goog_soup = bs(googled.content, 'html.parser')
        goog_result = goog_soup.find('span', {'class': 'd-block fw-600 text-main-green-dark'})
        volume_name.append(unidecode.unidecode(goog_result.text))

    print(volume_name)
    print(volume_tick)
    print(volume_dif)
    print(volume_value)


def create_png(type_stock, name, tick, dif, value, sum_v):
    W, H = (1080, 1920)                                                     # Tamanho base da imagem
    if type_stock == "altas":
        final_img = Image.open(raw_altas)                                   # Abre o background
        bg_color = bg_sq_altas
    elif type_stock == "baixas":
        final_img = Image.open(raw_baixas)                                  # Abre o background
        bg_color = bg_sq_baixas
    else:
        final_img = Image.open(raw_volume)                                  # Abre o background
        bg_color = bg_sq_altas

    draw = ImageDraw.Draw(final_img)                                       # Cria um "draw" para a imagem
    sum_h = [0, 225, 450, 675, 900]                                        # Soma em "height" para cada quadrado
    dlt_v = [0, 1, 2, 3, 4]

    for sh, loop_v in zip(sum_h, dlt_v):
        shape = [(114+sum_v, 500+sh), (960+sum_v, 500+80+60+sh)]            # Gera o quadrado de bordas externo
        draw.rectangle(shape, outline="white", width=5, fill=bg_color)     # Imprime o quadrado de borda

        # Nome da empresa
        font = ImageFont.truetype(font_use, size=42)                            # Tipo e tamanho da fonte
        color = 'rgb(0, 0, 0)'                                                  # Cor do Texto
        w, h = draw.textsize(clear_title(name[loop_v]), font=font)              # Pega o tamanho do texto para centralizar
        (x, y) = (((W-w)/2)+sum_v, 505+sh)                                      # Onde o texto será "impresso"
        shape = [(115+sum_v, 500+sh), (960+sum_v, 510+h+sh)]                    # Configura retangulo branco
        draw.rectangle(shape, fill="#ffffff")                                   # Imprime retangulo
        draw.text((x, y), clear_title(name[loop_v]), fill=color, font=font)     # Imprimindo o texto

        # Ticker da empresa
        font = ImageFont.truetype(font_use, size=50)                            # Tipo e tamanho da fonte
        color = 'rgb(255, 255, 255)'                                            # Cor do Texto
        (x, y) = (125+sum_v, 575+sh)                                            # Onde o texto será "impresso"
        draw.text((x, y), tick[loop_v], fill=color, font=font)                  # Imprimindo o texto

        # Diferença de valor
        font = ImageFont.truetype(font_black, size=50)                            # Tipo e tamanho da fonte
        if float(dif[loop_v][:-1].replace(",", ".")) < 0:
            color = 'rgb(255, 0, 0)'                                            # Cor do Texto
        else:
            color = 'rgb(0, 255, 0)'                                            # Cor do Texto
        w, h = draw.textsize(dif[loop_v], font=font)                            # Pega o tamanho do texto para centralizar
        (x, y) = (((W - w) / 2)+sum_v, 575+sh)                                        # Onde o texto será "impresso"
        draw.text((x, y), dif[loop_v], fill=color, font=font)                   # Imprimindo o texto

        # Valor da ação
        font = ImageFont.truetype(font_use, size=50)                            # Tipo e tamanho da fonte
        color = 'rgb(255, 255, 255)'                                            # Cor do Texto
        w, h = draw.textsize(value[loop_v], font=font)                          # Pega o tamanho do texto para centralizar
        (x, y) = (960-w-10+sum_v, 575+sh)                                             # Onde o texto será "impresso"
        draw.text((x, y), value[loop_v], fill=color, font=font)                 # Imprimindo o texto

    if type_stock == "altas":
        # Salva a imagem
        final_img.save(path_altas)  # Salva a imagem
    elif type_stock == "baixas":
        final_img.save(path_baixas)  # Salva a imagem
    else:
        final_img.save(path_volume)  # Salva a imagem


if __name__ == '__main__':
    get_altas()
    get_baixas()
    # get_volume()
    create_png('altas', altas_name, altas_tick, altas_dif, altas_value, 0)
    create_png('baixas', baixas_name, baixas_tick, baixas_dif, baixas_value, 0)
    # create_png('movimentos', volume_name, volume_tick, volume_dif, volume_value, 0)
    telegram_send_altas_baixas()


