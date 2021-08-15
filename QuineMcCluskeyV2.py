import datetime
# # # # # # # # # # # # # # # # # # # # #
# MÉTODO DE QUINE-MCCLUSKEY P/ 1 SAÍDA  #
# Créditos                              #
# Nome: João Victor Franco Fernandes    #
# E-mail: joao.fernandes@unesp.br       #
# Data: 12/08/2021                      #
# # # # # # # # # # # # # # # # # # # # #
# UNESP - Câmpus de Ilha Solteira       #
# Professor: Alexandre C.R. da Silva    #
# E-mail: alexandre.cr.silva@unesp.br   #
# # # # # # # # # # # # # # # # # # # # #
# Agradecimento especial para o         #
# Pedro Augusto Mendonça Nunes e para o #
# Guilherme Martins pela grande ajuda   #
# no desenvolvimento de todo o código!  #
# # # # # # # # # # # # # # # # # # # # #

# ÚLTIMO UPDATE: 2021/08/12 - 19:22
#   ~> Correção do bug onde o mintermo 0 não era considerado nos loopings de filtragem
#   ~> Acréscimos de comentários para auxílio no entendimento do código
#   ~> Corrigido erro da entrada do exercício não mostrar os don't care
#   ~> Melhoria na interface para o usuário, tornando mais claro as instruções
#   ~> Melhoria na saída de dados, tornando mais didático o que o usuário deve fazer com as respostas!
#   ~> Adição de créditos ao material


import collections
from re import search

line_limit = 128    # 2^7 --> EXPANSÃO DO CÓDIGO

def binTOstr(numbers):          # Essa função tem como finalidade transformar o código binário de cada valor da tabela
    qtd = len(numbers)          # verdade em algo legível (Exemplo: 1101 = ABC'D)
    word = []
    for x in range(0, len(numbers)):
        if numbers[x] == '1':
            word.append(str(chr(65+x)))
        if numbers[x] == '0':
            word.append(str(chr(65 + x))+"'")
    palavra_full = ''.join([str(item) for item in word])
    return palavra_full


def output_function(tabela_vdd, output):        # Essa função coleta os valores "legíveis" da função "binTOstr" e
    resposta = []                               # "junta", transformando em uma função de saída!
    for x in range(0, len(tabela_vdd)):
        if str(x) in output:
            retornin = binTOstr(tabela_vdd[x])
            resposta.append(retornin+"+")
    palavra_full2 = ''.join([str(item) for item in resposta])
    palavra_full2 = palavra_full2[:-1]
    return palavra_full2


def tabela_verdade(entradas):                   # Essa função determina a tabela verdade do meu problema.
    tabela_vdd = []
    num_casas = (entradas * entradas)
    for x in range(0, num_casas):
        tabela_vdd.append(str(bin(x).replace("0b", "")))
        while len(tabela_vdd[x]) < entradas:
            tabela_vdd[x] = "0"+tabela_vdd[x]
    return tabela_vdd


def tabela_nivel1(entradas, mintermos, tabela_vdd):         # Essa função cria as tabelas iniciais para QuineMcCluskey
    grupo0_binario = []
    grupo0_mintermo = []
    for y in range(0, entradas+1):
        grupo0_binario.append([])
        grupo0_mintermo.append([])

    casa_tabela_vdd = 0

    for x in tabela_vdd:
        termos = collections.Counter(x)
        contador_de_1s = 0
        while contador_de_1s <= entradas:
            if (termos['1'] == contador_de_1s) and (str(casa_tabela_vdd) in mintermos):
                grupo0_binario[contador_de_1s].append(x)
                grupo0_mintermo[contador_de_1s].append("m"+str(casa_tabela_vdd))
            contador_de_1s = contador_de_1s + 1
        casa_tabela_vdd = casa_tabela_vdd + 1
    return grupo0_binario, grupo0_mintermo


def tabela_niveln(entradas, grupo0_binario, grupo0_mintermo):       # Essa função cria as tabelas "n" para QMcK
    grupon_binario = []
    grupon_mintermo = []

    for abacate in range(0, entradas):
        grupon_binario.append([])
        grupon_mintermo.append([])
        for modernoin in range(0, entradas):
            grupon_binario[abacate].append([])
            grupon_mintermo[abacate].append([])

    grupon_binario[0] = grupo0_binario.copy()
    grupon_mintermo[0] = grupo0_mintermo.copy()

    for x in range(0, entradas):                                # Grupo X
        for y in range(0, len(grupon_binario[x])-1):            # Iteração Y
            z = 0
            while z < (len(grupon_binario[x][y])):              # Termos comparados
                w = 0
                while w < len(grupon_binario[x][y+1]):          # Termos para comparar
                    igual = 0
                    diferente = 0
                    for k in range(0, entradas):                # Digito do termo
                        if grupon_binario[x][y][z][k] == grupon_binario[x][y+1][w][k]:
                            igual = igual + 1
                        else:
                            diferente = k

                    palavra_pronta = []
                    if igual == (entradas-1):
                        for celtinha in range(0, entradas):
                            if celtinha != diferente:
                                palavra_pronta.append(grupon_binario[x][y][z][celtinha])
                            if celtinha == diferente:
                                palavra_pronta.append("X")
                        palavra_full = ''.join([str(item) for item in palavra_pronta])
                        if palavra_full not in grupon_binario[x+1][y]:
                            grupon_binario[x+1][y].append(palavra_full)
                            grupon_mintermo[x+1][y].append(grupon_mintermo[x][y][z]+"&"+grupon_mintermo[x][y+1][w]+"&")

                            # Perceba que a junção com o caractere "&" tem uso mais a frente, para que o código possa
                            # diferenciar mintermos em uma função (Exemplo: Saber a diferença de M1 para M11)

                    w = w + 1
                z = z + 1
    return grupon_binario, grupon_mintermo


def super_filtro(binario, mintermo, qtd_entradas):      # Essa função filtra os termos para a função "implicante_primo"
    vetor_contador = []

    for x in range(0, qtd_entradas*qtd_entradas):
        vetor_contador.append([0])

    for a in range(0, qtd_entradas):
        for b in range(0, qtd_entradas+1):
            for c in range(0, qtd_entradas*qtd_entradas):
                try:
                    print(mintermo[a][b][c])            # NÃO EXCLUIR, ESSENCIAL PARA FUNCIONAMENTO
                    mintermo[a][b][c] = mintermo[a][b][c].replace("&&", "&")
                    for d in range(0, qtd_entradas*qtd_entradas):
                        if search("m"+str(d)+"&", mintermo[a][b][c]):
                            vetor_contador[d][0] = vetor_contador[d][0]+1
                    if mintermo[a][b][c][-1:] == "&":
                        mintermo[a][b][c] = mintermo[a][b][c][:-1]
                except IndexError:
                    pass
    return mintermo, vetor_contador


def implicante_primo(mintermo, binario, qtd_entradas):      # Essa função retorna os implicantes primos do sistema
    conta_igual = 0
    conta_desigual = 0
    vetor_conta_usado = []
    vetor_implicantes_primos_binario = []
    vetor_implicantes_primos_mintermo = []

    for a in range(line_limit, -1, -1):
        for b in range(line_limit, -1, -1):
            for c in range(line_limit, -1, -1):
                try:
                    print(binario[a][b][c])             # NÃO EXCLUIR, ESSENCIAL PARA FUNCIONAMENTO
                    for d in range(a-1, -1, -1):
                        for e in range(line_limit, -1, -1):
                            for f in range(line_limit, -1, -1):
                                try:
                                    print(binario[d][e][f]+"*")         # NÃO EXCLUIR, ESSENCIAL PARA FUNCIONAMENTO
                                    for g in range(0, qtd_entradas):
                                        if binario[a][b][c][g] == binario[d][e][f][g]:
                                            conta_igual = conta_igual + 1
                                        else:
                                            conta_desigual = conta_desigual + 1
                                    if conta_desigual == 1 and conta_igual == qtd_entradas-1:
                                        print("OPA!")
                                        vetor_conta_usado.append(binario[d][e][f])
                                    elif conta_igual + conta_desigual == qtd_entradas:
                                        print("OK")
                                    else:
                                        print("ERRO?")
                                        print(conta_igual)
                                        print(conta_desigual)
                                        exit()
                                    conta_igual = 0
                                    conta_desigual = 0
                                except IndexError:
                                    pass
                except IndexError:
                    pass

    conta_igual = 0

    for a in range(line_limit, -1, -1):
        for b in range(line_limit, -1, -1):
            for c in range(line_limit, -1, -1):
                try:
                    for x in range(0, len(vetor_conta_usado)):
                        if binario[a][b][c] == vetor_conta_usado[x]:
                            conta_igual = conta_igual + 1
                    if conta_igual == 0:
                        vetor_implicantes_primos_binario.append(binario[a][b][c])
                        vetor_implicantes_primos_mintermo.append(mintermo[a][b][c])
                    conta_igual = 0
                except IndexError:
                    pass

    return vetor_implicantes_primos_binario, vetor_implicantes_primos_mintermo


def implicante_essencial(mintermo, binario, qtd_entradas, dontc):       # Essa função retorna os implicantes essenciais

    novo_min_vetor = []
    conta_apear = []
    conta_jafoi = []

    essenciais_min = []
    essenciais_bin = []

    min_faltantes = []

    for a in range(0, qtd_entradas*qtd_entradas):
        conta_apear.append(0)
        conta_jafoi.append(0)

    for a in range(0, len(mintermo)):
        novo_min_vetor.append(mintermo[a]+"&")

    for a in range(0, len(mintermo)):
        for b in range(0, qtd_entradas*qtd_entradas):
            if ("m"+str(b)+"&") in novo_min_vetor[a]:
                conta_apear[b] = conta_apear[b]+1
    for a in range(0, qtd_entradas*qtd_entradas):
        if conta_apear[a] == 0 or str(a) in dontc:
            conta_jafoi[a] = "NOP"

    for a in range(0, qtd_entradas*qtd_entradas):
        if str(a) in dontc:
            receba = conta_apear[a]
            conta_apear[a] = "X"
            conta_apear[a] = "X ("+str(receba)+")"

    for a in range(0, len(mintermo)):
        for b in range(0, qtd_entradas * qtd_entradas):
            if conta_apear[b] == 1 and (("m"+str(b)+"&") in novo_min_vetor[a]):
                essenciais_min.append(mintermo[a])
                essenciais_bin.append(binario[a])
                for c in range(0, qtd_entradas*qtd_entradas):
                    if ("m"+str(c)+"&") in novo_min_vetor[a]:
                        try:
                            conta_jafoi[c] = conta_jafoi[c] + 1
                        except TypeError:
                            pass

    for a in range(0, qtd_entradas*qtd_entradas):
        if conta_jafoi[a] == 0:
            cometa = "m"+str(a)
            min_faltantes.append(cometa)
    return essenciais_min, essenciais_bin, min_faltantes


# Essa função é responsável por gravar os cálculos realizados no txt de saída para compreensão do usuário
def grava_txt(entradas, saidas, binario, mintermo, output_tv, bin_primo, min_primo, min_essencial, bin_essencial, min_faltante, saidas_dc):

    with open('output.txt', "w+") as f:
        letras = "A"
        for x in range(1, entradas):
            letras = letras + chr(65 + x)

        f.write('Entrada do exercício: ')
        f.write('f(' + str(letras) + ') = ')
        f.write('Sm(' + str(saidas) + ')')
        f.write(' + d('+saidas_dc+')\n')
        f.write('Saída pela tabela verdade: ')
        f.write('f(' + str(letras) + ')= ')
        f.write(output_tv)
        f.write('\n\n')

        for y in range(0, entradas):
            f.write("GRUPO "+str(y)+":\n")
            f.write("{: <20} {: <100} {: <10}\n".format("NÚMEROS DE 1'S", "MINTERMOS", "REPRESENTAÇÃO BINÁRIA"))
            for x in range(0, entradas):
                try:
                    f.write("{: <20} {: <100} {: <10}\n".format(str(x+1), str(mintermo[y][x+1]), str(binario[y][x+1])))
                except IndexError:
                    f.write("{: <20} {: <100} {: <10}\n".format('NOP', 'NOP', 'NOP'))
            f.write("\n\n")

        f.write("TABELA A: Termos implicantes primos: \n")
        f.write("{: <20} {: <100} {: <10}\n".format("", "MINTERMOS", "REPRESENTAÇÃO BINÁRIA"))
        f.write("{: <20} {: <100} {: <10}\n\n\n".format("", str(min_primo), str(bin_primo)))

        f.write("\n")
        f.write("TABELA B: Termos implicantes primos ESSENCIAIS: \n")
        f.write("{: <20} {: <100} {: <10}\n".format("", "MINTERMOS", "REPRESENTAÇÃO BINÁRIA"))
        f.write("{: <20} {: <100} {: <10}\n\n\n".format("", str(min_essencial), str(bin_essencial)))

        f.write("\n")
        f.write("TABELA C: Mintermos não inclusos pelos primos essenciais: \n")
        f.write("{: <20} {: <100}\n".format("", "MINTERMOS"))
        f.write("{: <20} {: <100}\n\n\n".format("", str(min_faltante)))

        saida_final = ""

        for a in bin_essencial:
            for b in range(0, entradas):
                if a[b] == "1":
                    saida_final = saida_final + chr(65 + b)
                if a[b] == "0":
                    saida_final = saida_final + chr(65 + b) + "'"
            saida_final= saida_final + " + "

        saida_final = saida_final + "TERMOS_FALTANTES"

        f.write("\n")
        f.write("Através desses dados, temos as seguintes informações: \n")
        f.write("Sua saída final NECESSARIAMENTE precisa dos termos S = "+str(saida_final)+" onde 'TERMOS_FALTANTES'\n")
        f.write("são os mintermos não inclusos pelos primos essenciais, assim, você deve utilizar implicantes primos\n")
        f.write("que não sejam os essenciais (tabela A) para completar sua equação de saída!\n")


# Aqui é o primeiro passo do programa!
print("Seja bem-vindo ao otimizador Quine-McCluskey para 1 saída!")
inputs = int(input("Por favor, digite a quantidade de variáveis de entrada: "))
output = input("Por favor, digite os mintermos separados por vírgulas (incluindo os dont'care): ")
dontcare = input("Por favor, indique quais desses mintermos são don't care, separados por virgulas: ")
data_inicio = datetime.datetime.now()
output_formatado = output.split(',')
dontcare_formatado = dontcare.split(',')

tabela_completa = tabela_verdade(inputs)
grupinho0_binario, grupinho0_mintermo = tabela_nivel1(inputs, output_formatado, tabela_completa)
grupinhos_binario, grupinhos_mintermo = tabela_niveln(inputs, grupinho0_binario, grupinho0_mintermo)
saida_tv = output_function(tabela_completa, output_formatado)
mintermo_filtrado, vetor_contador = super_filtro(grupinhos_binario, grupinhos_mintermo, inputs)
vtr_implicante_primo_bin, vtr_implicante_primo_min = implicante_primo(mintermo_filtrado, grupinhos_binario, inputs)
impes_min, impes_bin, mintermos_faltante = implicante_essencial(vtr_implicante_primo_min, vtr_implicante_primo_bin, inputs, dontcare_formatado)
grava_txt(inputs, output, grupinhos_binario, grupinhos_mintermo, saida_tv, vtr_implicante_primo_bin, vtr_implicante_primo_min, impes_min, impes_bin, mintermos_faltante, dontcare)

# 4,8,9,10,11,12,14,15

data_fim = datetime.datetime.now()
data_delta = data_fim - data_inicio
print(data_delta)
