def jump():
    print("---------------------------------------------------------------")


def somatoria():
    somando = 0
    end_somatoria = False
    while not end_somatoria:
        new_somando = int(input("Digite a potência para irmos somando (0 para encerrar): "))
        if new_somando == 0:
            end_somatoria = True
        else:
            somando = somando + new_somando
            print("Até agora temos " + somando + " W neste circuito terminal!")
    jump()
    print("Potência total: " + somando)
    return somando


def ip_calc(num_circ, method_fase, method_fact, method_rend):
    pot = float(input("Somatória da potência do circuito " + str(num_circ + 1) + ": "))
    p = pot / (method_fact * method_fase * method_rend)
    print("pi["+str(num_circ+1)+"] = "+str(pot)+"/("+str(method_fact)+" * "+str(method_fase)+" * "+str(method_rend)+") = "+str(p))
    return p


method = 0
p_i = []
p_i_linha = []

method_type = input("PVC ou EXT? ")
method_ref = input("Referência (A1,B1,etc.): ")
method_temp = float(input("Temperatura ambiente: "))
method_fact = float(input("Fator de potência: "))
method_rend = float(input("Rendimento: "))
method_fase = int(input("Tensão (220 para 2 fases, 127 para 1 fase): "))
method_ctm = int(input("Quantidade de circuitos terminais: "))
method_maxe = float(input("Queda máxima de tensão: "))
# method_isol = input("Isolação: ")
jump()

while method < 1 or method > 2:
    print("Por favor selecione o critério:")
    print("1 - Critério da capacidade de condução de corrente.")
    print("2 - Critério da Queda de Tensão trecho a trecho.")
    method = int(input("Selecione: "))

    if method == 1:
        jump()
        print('Critério 1 selecionado: Capacidade de condução de corrente!')
        jump()
        for num_circ in range(0, method_ctm):
            p_i.append(ip_calc(num_circ, method_fase, method_fact, method_rend))
        FCT = float(input("Digite o FCT para " + method_type + " na temperatura de " + str(method_temp) + "º Celsius: "))
        FCA = float(input("Digite o FCA para " + method_ref + " para " + str(method_ctm) + " circuitos terminais: "))
        for num_circ in range(0, method_ctm):
            p_i_linha.append(p_i[num_circ] / (FCT * FCA))
            print("pi'["+str(num_circ+1)+"] = "+str(p_i[num_circ])+" / ("+str(FCT)+" * "+str(FCA)+") = "+str(p_i_linha[num_circ]))
        print("Procurar o dimensionamento ideal na tabela " + method_type + " em " + method_ref + "para os seguintes valores de PI':")
        print(p_i_linha)

    elif method == 2:
        jump()
        print('Critério 2 selecionado: Queda de tensão trecho a trecho!')
        jump()
    else:
        jump()
        print("Nenhum método válido selecionado!!!")
        jump()
