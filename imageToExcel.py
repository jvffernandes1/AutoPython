import PIL.Image                                            # Biblioteca responsável por modificar as imagens
import xlsxwriter                                           # Bilbioteca responsável por modificar excel
import colormap

# Parâmetros inciais ---------------------------------------------------------------------------------------------------
name = "jv"

img_url = "imgs/"+name+".png"                               # Caminho da imagem que será usada
xls_file = xlsxwriter.Workbook('imgs/'+name+'.xlsx')        # Caminho de saída do Excel

# Variáveis globais ----------------------------------------------------------------------------------------------------
line_vector = []                                            # Vetor para a linha da imagem
big_line_vector = []                                        # Vetor para o conjunto de linhas da imagem

img = PIL.Image.open(img_url)                               # Abre a imagem escolhida
img_w, img_h = img.size                                     # Captura o tamanho da imagem escolhida
img_rgb = img.convert("RGB")                                # Converte a imagem escolhida para o formato RGB

if img_w * img_h > 65490:
    print("Imagem grande demais, por favor se limite a imagens onde altura * largura <= 65.490 (255x255)!!! ")
    print(img_h*img_w)
    exit()

print("OK")

for x in range(0, img_h):                                   #
    for y in range(0, img_w):                               # Conjunto de comandos que transforma cada pixel de nossa
        img_rgb_list = list(img_rgb.getpixel((y, x)))
        img_hex = colormap.rgb2hex(img_rgb_list[0], img_rgb_list[1], img_rgb_list[2])
        line_vector.append(img_hex)                         # imagem em um vetor com números, para que seja passado
    big_line_vector.append(line_vector)                     # para o excel.
    line_vector = []                                        #

print("OK")

xls_sheet = xls_file.add_worksheet(name)                    # Cria a planilha dentro do arquivo do excel

for x in range(0, img_h):
    for y in range(0, img_w):
        cell_format_color = xls_file.add_format({'bg_color': big_line_vector[x][y]})
        xls_sheet.write(x, y, ' ', cell_format_color)

xls_sheet.set_column(0, img_w, 2.14)                        # Ajusta a largura das células para virarem quadrados
xls_file.close()
