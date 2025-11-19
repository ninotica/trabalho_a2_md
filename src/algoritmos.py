""" 
O problema da coloração de grafos é NP-Completo, logo, não há solução em tempo polinomial para a solução exata desse problema.
Entretanto, existem algumas heurísticas podem restringir o escopo do problema, de modo a acelerar o processo. 
Nesse projeto, serão avaliados os seguintes algoritmos:
- Backtracking;
- Guloso sequencial; 
- DSATUR;
- Variações
"""

import copy
from Disciplinas import Disciplina, Grafo, grafo
   
def busca_backtraking(grafo: Grafo, cores: dict[int: list[Disciplina]] = None, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada=None):
    num_vertices = len(grafo.get_vertices())
    if num_cores_encontrado == None: num_cores_encontrado = num_vertices + 1
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    if num_coloridos == 0:
        for v in grafo.get_vertices():
            if v.get_cor() != None: num_coloridos += 1

    
    max_cor = -1
    for cor in [vert.get_cor() for vert in grafo.get_vertices()]:
        if cor != None:
            if cor > max_cor: 
                if cor + 1 >= num_cores_encontrado:
                    return (num_cores_encontrado, coloracao_encontrada)
                max_cor = cor

    if num_coloridos == num_vertices:
        return (max_cor + 1, cores) # já se sabe que max_cor + 1 < num_cores_encontrado devido ao loop anterior
    
    v = None
    for vertice in grafo.get_vertices():
        if vertice.get_cor() == None:
            v = vertice
            break

    blocked_colors = []

    for u in grafo.get_vizinhos(v):
        if u.get_cor() != None:
            blocked_colors.append(u.get_cor())

    # sozinho = False
    for i in range(max_cor + 2):
        if i >= num_vertices: break
        # if sozinho and cores[i] == []:
        #     continue
        if i in blocked_colors:
            continue
        v.set_cor(i)
        cores[i].append(v)
        num_cores, coloracao = busca_backtraking(grafo, cores, num_coloridos + 1, num_cores_encontrado, coloracao_encontrada)
        if num_cores < num_cores_encontrado:
            num_cores_encontrado = num_cores
            coloracao_encontrada = copy.deepcopy(coloracao)
        cores[i].pop()
        v.set_cor(None)

        # if sozinho == False and cores[i] == []:
        #     sozinho = True
    
    return (num_cores_encontrado, coloracao_encontrada)

def busca_BTSL(grafo: Grafo, cores: dict[int: list[Disciplina]] = None, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada=None):
    grafo.sort_vertices_grau()
    return busca_backtraking(grafo, cores, num_coloridos, num_cores_encontrado, coloracao_encontrada)

def busca_BTDSATUR(grafo: Grafo, cores: dict[int: list[Disciplina]] = None, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada=None):
    num_vertices = len(grafo.get_vertices())
    if num_coloridos == 0:
        for v in grafo.get_vertices():
            if v.get_cor() != None: num_coloridos += 1

    if num_cores_encontrado == None: num_cores_encontrado = num_vertices + 1
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    
    max_cor = -1
    for v in grafo.get_vertices():
        cor = v.get_cor()
        if cor != None:
            if cor > max_cor:
                if cor + 1 >= num_cores_encontrado:
                    return (num_cores_encontrado, coloracao_encontrada)
                max_cor = cor

    if num_coloridos == num_vertices:
        return (max_cor + 1, cores) # já se sabe que max_cor + 1 < num_cores_encontrado devido ao loop anterior

    v = None
    for u in grafo.get_vertices():
        if u.get_cor() == None:
            if v == None:
                v = u
            elif grafo.get_saturacao(u) > grafo.get_saturacao(v):
                v = u
            elif grafo.get_saturacao(u) == grafo.get_saturacao(v) and grafo.get_grau(u) > grafo.get_grau(v):
                v = u
        
    blocked_colors = []

    for u in grafo.get_vizinhos(v):
        if u.get_cor() != None:
            blocked_colors.append(u.get_cor())

    # sozinho = False
    for i in range(max_cor + 2):
        if i >= num_vertices: break
        # if sozinho and cores[i] == []:
        #     continue
        if i in blocked_colors:
            continue
        v.set_cor(i)
        cores[i].append(v)
        num_cores, coloracao = busca_BTDSATUR(grafo, cores, num_coloridos + 1, num_cores_encontrado, coloracao_encontrada)
        if num_cores < num_cores_encontrado:
            num_cores_encontrado = num_cores
            coloracao_encontrada = copy.deepcopy(coloracao)
        cores[i].pop()
        v.set_cor(None)

        # if sozinho == False and cores[i] == []:
        #     sozinho = True
    
    return (num_cores_encontrado, coloracao_encontrada)

def busca_gulosa_seq(grafo: Grafo, cores: dict[int: list[Disciplina]] = None, num_coloridos: int = 0):
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    grafo.sort_vertices_grau()
    num_vertices = len(grafo.get_vertices())
    if num_coloridos == 0:
        for v in grafo.get_vertices():
            if v.get_cor() != None: num_coloridos += 1

    v = None
    for vert in grafo.get_vertices():
        if vert.get_cor() == None:
            v = vert
            break
    
    disponivel = list(range(num_vertices))
    for u in grafo.get_vizinhos(v):
        if u.get_cor() in disponivel:
            disponivel.remove(u.get_cor())
    
    v.set_cor(disponivel[0])
    cores[disponivel[0]].append(v)

    if num_coloridos + 1 == num_vertices:
        qtd_cor = 0
        for cor in cores.values():
            if len(cor) > 0:
                qtd_cor += 1

        return (qtd_cor, cores)
    
    return busca_gulosa_seq(grafo, cores, num_coloridos + 1)

def busca_DSATUR(grafo: Grafo, cores: dict[int: list[Disciplina]] = None):
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    num_vertices = len(grafo.get_vertices())
    grafo.sort_vertices_grau()
    v = grafo.get_vertices()[0]
    v.set_cor(0)
    cores[0].append(v)

    for _ in range(1, num_vertices):
        u = None
        for w in grafo.get_vertices():
            if w.get_cor() == None:
                if u == None:
                    u = w
                elif grafo.get_saturacao(u) < grafo.get_saturacao(w):
                    u = w
                elif grafo.get_saturacao(u) == grafo.get_saturacao(w):
                    if grafo.get_grau(u) < grafo.get_grau(w):
                        u = w

        disponivel = list(range(num_vertices))
        for w in grafo.get_vizinhos(u):
            if w.get_cor() in disponivel:
                disponivel.remove(w.get_cor())

        u.set_cor(disponivel[0])
        cores[disponivel[0]].append(u)


    qtd_cor = 0
    for cor in cores.values():
        if len(cor) == 0:
            break
        qtd_cor += 1

    return (qtd_cor, cores)
    
def limpar_coloracao(coloracao):
    nova_coloracao = {}
    for cor, vertices in coloracao.items():
        if len(vertices) > 0:
            nova_coloracao[cor] = vertices

    return nova_coloracao

def encher_coloracao(coloracao, tam_grafo):
    tam_coloracao = len(coloracao.keys())
    for i in range(tam_coloracao, tam_grafo):
        coloracao[i] = []
    return coloracao

if __name__ == '__main__':

    print(grafo)

    print(busca_BTDSATUR(grafo))
    num_vertices = len(grafo.get_vertices())
    cores = {i: [] for i in range(num_vertices)}

    print('\nBusca com um algorítmo guloso sequencial:')
    num_cores, coloracao = busca_gulosa_seq(grafo, copy.deepcopy(cores))
    coloracao = limpar_coloracao(coloracao)
    print(f'Número de cores necessário: {num_cores}')
    print(f'Coloração:\n{coloracao}')
    for v in grafo.get_vertices():
        v.set_cor(None)

    print('\nBusca com um algorítmo DSATUR:')
    num_cores, coloracao = busca_DSATUR(grafo, copy.deepcopy(cores))
    coloracao = limpar_coloracao(coloracao)
    print(f'Número de cores necessário: {num_cores}')
    print(f'Coloração:\n{coloracao}')
    for v in grafo.get_vertices():
        v.set_cor(None)

    print('\nBusca com um algorítmo de backtracking:')
    num_cores, coloracao = busca_backtraking(grafo, copy.deepcopy(cores), 0, num_cores, encher_coloracao(coloracao, len(grafo.get_vertices())))
    coloracao = limpar_coloracao(coloracao)
    print(f'Número de cores necessário: {num_cores}')
    print(f'Coloração:\n{coloracao}')
    for v in grafo.get_vertices():
        v.set_cor(None)
