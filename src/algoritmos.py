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
import random
from collections import deque

def busca_BTDSATUR(grafo: Grafo, cores: dict[int: list[Disciplina]] = {}, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada={}):
    coloracao_inicial = grafo.salvar_coloracao()
    num_vertices = len(grafo.get_vertices())
    if num_coloridos == 0:
        for v in grafo.get_vertices():
            if not v.pode_mudar: 
                num_coloridos += 1
        if coloracao_encontrada == {} and num_coloridos != 0: 
            coloracao_encontrada = {i: [] for i in range(len(grafo.get_vertices()))}
            for cor, vertices in grafo.calendario().items():
                for u in vertices:
                    if u.pode_mudar or (u.cor == cor):    
                        coloracao_encontrada[cor].append(u)
                    else: 
                        coloracao_encontrada = {}

            coloracao_num_vertices = 0
            for cor, vertices in coloracao_encontrada.items():
                if len(vertices) > 0:
                    coloracao_num_vertices += len(vertices)
                    if num_cores_encontrado == None or cor > num_cores_encontrado: 
                        num_cores_encontrado = cor

            if coloracao_num_vertices != num_vertices: 
                coloracao_encontrada = {}
                num_cores_encontrado = num_vertices + 1
            else:
                num_cores_encontrado += 1
        
        if cores == {} and num_coloridos != 0: 
            cores = {i: [] for i in range(len(grafo.get_vertices()))}
            for u in grafo.get_vertices():
                if not u.pode_mudar and not u in cores[cor]:
                    cores[u.cor].append(u)

    if num_cores_encontrado == None: num_cores_encontrado = num_vertices + 1
    if cores == {}: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    
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
        if u.get_cor() == None and u.pode_mudar:
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
    grafo.restaurar_coloracao(coloracao_inicial)
    return (num_cores_encontrado, coloracao_encontrada)
   
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



if __name__ == '__main_':

    print(grafo)

    print(busca_BTDSATUR(grafo))
    num_vertices = len(grafo.get_vertices())
    cores = {i: [] for i in range(num_vertices)}

    print('\nBusca com um algorítmo guloso sequencial:')
    num_cores, coloracao = busca_gulosa_seq(grafo, copy.deepcopy(cores))
    coloracao = limpar_coloracao(coloracao)
    print(f'Número de cores necessário: {num_cores}')
    print(f'Coloração:\n{coloracao}')

    print('\nBusca com um algorítmo DSATUR:')
    num_cores, coloracao = busca_DSATUR(grafo, copy.deepcopy(cores))
    coloracao = limpar_coloracao(coloracao)
    print(f'Número de cores necessário: {num_cores}')
    print(f'Coloração:\n{coloracao}')


    print('\nBusca com um algorítmo de backtracking:')
    num_cores, coloracao = busca_backtraking(grafo, copy.deepcopy(cores), 0, num_cores, encher_coloracao(coloracao, len(grafo.get_vertices())))
    coloracao = limpar_coloracao(coloracao)
    print(f'Número de cores necessário: {num_cores}')
    print(f'Coloração:\n{coloracao}')


    print(grafo.salvar_coloracao())

if __name__ == '__main__':
    num, col = busca_BTDSATUR(grafo)

    print(num, col)