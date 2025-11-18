from Disciplinas import grafo, nr_dias, requerimentos_profs, Disciplina, AEDV, OCD, MD, AL

################################################################################
# Setup Algoritmo Guloso
################################################################################

def pode_colorir(disciplina: Disciplina, dia: int, grafo: dict, coloracao: dict) -> bool:
    """
    checa se pode designar esse dia para a disciplina
    """
    for vizinho in grafo[disciplina]:
        if vizinho in coloracao and coloracao[vizinho] == dia:
            return False
    return True

def requerimentos_razoaveis(requerimento: dict, grafo:dict) -> bool:
    for materia in requerimento:
        for vizinho in grafo[materia]:
            if vizinho in requerimento and requerimento[vizinho] == requerimento[materia]:
                return False
    return True

def ordem_de_ruindade(grafo, calendario):
    ruindade = 0
    for dia in calendario:
        if (dia - 1) not in calendario:
            continue
        for materia in calendario[dia]:
            if not materia.eh_dificil:
                continue
            for vizinho in grafo[materia]:
                if vizinho in calendario[dia - 1]:
                    ruindade += 1
    return ruindade

def primeiro_disponivel(cores_usadas, cores_disponiveis):
    """Return smallest non-negative integer not in the given set of colors.
    """
    cores = [cor for cor in cores_disponiveis if cor not in cores_usadas]
    return cores[0] if cores else False

# def coloracao_gulosa(grafo, cores):
#     """Find the greedy coloring of G in the given order.
#     The return value is a dictionary mapping vertices to their colors.

#     https://en.wikipedia.org/wiki/Greedy_coloring
#     """
#     coloracao = {d: d.cor for d in grafo if d.cor is not None}
#     for vertice in grafo:
#         if vertice in coloracao:
#             continue
#         used_neighbour_colors = {coloracao[nbr]
#                                  for nbr in grafo[vertice]
#                                  if nbr in coloracao}
#         pd = primeiro_disponivel(used_neighbour_colors, cores)
#         if not pd:
#             print("Coloração Falhou!")
#             return 0
#         coloracao[vertice] = pd
#     return coloracao

def coloracao_gulosa(grafo, cores):
    coloracao_inicial = {d: d.cor for d in grafo.elementos}
    for vertice in grafo.elementos:
        if vertice.cor is not None:
            continue
        used_neighbour_colors = {nbr.cor
                                for nbr in grafo.dict_format()[vertice]
                                if nbr.cor is not None}
        pd = primeiro_disponivel(used_neighbour_colors, cores)
        if not pd:
            print("Coloração Falhou!")
            return 0
        vertice.cor = pd
        coloracao = grafo.coloracao()
        #reseta as cores iniciais
    for d in grafo.elementos:
        d.cor = coloracao_inicial[d]
    return coloracao
################################################################################
# Test Driver
################################################################################

coloracao = coloracao_gulosa(grafo, [1, 2, 3, 4, 5, 6, 7])
print((coloracao))

