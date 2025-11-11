from Disciplinas import grafo, nr_dias, requerimentos_profs, Disciplina, AEDV, OCD, MD, AL, materias_dificeis

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

def calendario_from_coloracao(coloracao: dict) -> dict:
    calendario = {}
    for disciplina in coloracao:
        if coloracao[disciplina] not in calendario:
            calendario[coloracao[disciplina]] = {disciplina}
        else:
            calendario[coloracao[disciplina]].add(disciplina)
    return calendario

def ordem_de_ruindade(grafo, calendario, materias_dificeis):
    ruindade = 0
    for dia in calendario:
        if (dia - 1) not in calendario:
            continue
        for materia in calendario[dia]:
            if materia not in materias_dificeis:
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

def coloracao_gulosa(grafo, cores, pre_requisitos={}):
    """Find the greedy coloring of G in the given order.
    The return value is a dictionary mapping vertices to their colors.

    https://en.wikipedia.org/wiki/Greedy_coloring
    """
    coloracao = pre_requisitos
    for vertice in grafo:
        if vertice in coloracao:
            continue
        used_neighbour_colors = {coloracao[nbr]
                                 for nbr in grafo[vertice]
                                 if nbr in coloracao}
        pd = primeiro_disponivel(used_neighbour_colors, cores)
        if not pd:
            print("Coloração Falhou!")
            return 0
        coloracao[vertice] = pd
    return coloracao

# def s

def coloracao_DSatur(grafo, cores, pre_requisitos={}):
    """https://en.wikipedia.org/wiki/DSatur"""
    proximo_vertice = list(grafo)[0]

################################################################################
# Test Driver
################################################################################

coloracao = coloracao_gulosa(grafo, [1, 2, 3, 4, 5, 6, 7], requerimentos_profs )
print(calendario_from_coloracao(coloracao))

