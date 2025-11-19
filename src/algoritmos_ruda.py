""" 
O problema da coloração de grafos é NP-Completo, logo, não há solução em tempo polinomial para a solução exata desse problema.
Entretanto, existem algumas heurísticas podem restringir o escopo do problema, de modo a acelerar o processo. 
Nesse projeto, serão avaliados os seguintes algoritmos:
- Backtracking;
- Guloso sequencial; 
- DSATUR;
- Variações
"""

import random
import copy

class Vertice():
    def __init__(self, label):
        self.label = label
        self.grau = 0
        self.saturacao = 0
        self.cor = None
        self.vizinhos = []
    
    def __str__(self):
        return str(self.label)
    
    def __repr__(self):
        return str(self.label)
    
    def __eq__(self, value):
        if not isinstance(value, Vertice):
            return NotImplemented
        if self.label != value.label:
            return False
        if self.cor != value.cor:
            return False
        if self.grau != value.grau:
            return False
        if self.saturacao != value.saturacao:
            return False
        if len(self.vizinhos) != len(value.vizinhos):
            return False
        return True
        # TODO: avaliar o estado de igualdade dos vizinhos (problema de recurssão infinita)
    
    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

    def set_grau(self, grau):
        self.grau = grau

    def get_grau(self):
        return self.grau

    def set_cor(self, cor):
        self.cor = cor

    def get_cor(self):
        return self.cor
    
    def set_saturacao(self, sat):
        self.saturacao = sat
    
    def get_saturacao(self):
        return self.saturacao
    
    def set_vizinhos(self, vizinhos):
        if isinstance(vizinhos, list):
            for vizinho in vizinhos:
                if not isinstance(vizinho, Vertice):
                    print('Vizinhos devem ser uma lista de vértices')
                    return
            self.vizinhos = vizinhos
        else:
            print('Vizinhos devem ser uma lista de vértices')

    def add_vizinho(self, vizinho):
        if isinstance(vizinho, Vertice):
            self.vizinhos.append(vizinho)
        else:
            print('Não é um vizinho válido')
        
    def remove_vizinho(self, vizinho):
        if vizinho in self.vizinhos:
            self.vizinhos.remove(vizinho)
        else:
            print('Não é um vizinho válido')

    def satura_vizinhos(self, soma_saturacao):
        for vizinho in self.vizinhos:
            vizinho.set_saturacao(vizinho.get_saturacao() + soma_saturacao)

    def get_vizinhos(self):
        return self.vizinhos
    
class Grafo():
    def __init__(self, vertices: list[Vertice], arestas: list[tuple[Vertice, Vertice]]):
        self.vertices = []
        self.arestas = {v.get_label(): [] for v in vertices}
        num_vertices = len(vertices)
        for _ in range(num_vertices):
            if vertices == []:
                break
            v = vertices.pop(0)
            for u in vertices:
                if arestas == []:
                    break

                for aresta in arestas:
                    if (v, u) == aresta or (u, v) == aresta:
                        if not u in self.arestas[v.get_label()]:
                            self.arestas[v.get_label()].append(u)
                            self.arestas[u.get_label()].append(v)

                            v.set_grau(v.get_grau() + 1)
                            u.set_grau(u.get_grau() + 1)
                            v.add_vizinho(u)
                            u.add_vizinho(v)

                            aresta[0].set_grau(aresta[0].get_grau() + 1)
                            aresta[1].set_grau(aresta[1].get_grau() + 1)
                            aresta[0].add_vizinho(aresta[1])
                            aresta[1].add_vizinho(aresta[0])

                        arestas.remove(aresta)
            self.vertices.append(v)
                        
    def gerar_grafo_generico(num_vertices, probabilidade):
        vertices = [Vertice(i) for i in range(num_vertices)]
        arestas = []
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.randint(0, 100) < probabilidade:
                    arestas.append((vertices[i], vertices[j]))

        return Grafo(vertices, arestas)
    
    def __str__(self):
        vertices = f'Vértices:\n{[v.__str__() for v in self.vertices]}\n\n'
        arestas = 'Arestas:\n'
        for vertice, vizinhos in self.arestas.items():
            arestas += f'{vertice}: {vizinhos}'+'\n'
        return vertices + arestas
    
    def set_vertices(self, vertices):
        self.vertices = vertices

    def get_vertices(self):
        return self.vertices
    
    def sort_vertices_grau(self):
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                v = self.vertices[i]
                u = self.vertices[j]
                if u.get_grau() > v.get_grau():
                    temp = v
                    self.vertices[i] = u
                    self.vertices[j] = temp

    def sort_vertices_saturacao(self):
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                v = self.vertices[i]
                u = self.vertices[j]
                if u.get_saturacao() > v.get_saturacao():
                    temp = v
                    self.vertices[i] = u
                    self.vertices[j] = v

    def reset_coloracao_vertices(self):
        for v in self.vertices:
            v.set_cor(None)
            v.set_saturacao(0)
        
        return self

    def get_arestas(self):
        return self.arestas       
    
def busca_backtraking(grafo: Grafo, cores: dict[int: list[Vertice]] = None, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada=None):
    num_vertices = len(grafo.get_vertices())
    if num_cores_encontrado == None: num_cores_encontrado = num_vertices + 1
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    
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

    for u in v.get_vizinhos():
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

def busca_BTSL(grafo: Grafo, cores: dict[int: list[Vertice]] = None, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada=None):
    grafo.sort_vertices_grau()
    return busca_backtraking(grafo, cores, num_coloridos, num_cores_encontrado, coloracao_encontrada)

def busca_BTDSATUR(grafo: Grafo, cores: dict[int: list[Vertice]] = None, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada=None):
    num_vertices = len(grafo.get_vertices())
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
            elif u.get_saturacao() > v.get_saturacao():
                v = u
            elif u.get_saturacao() == v.get_saturacao() and u.get_grau() > v.get_grau():
                v = u
        
    blocked_colors = []

    for u in v.get_vizinhos():
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
        v.satura_vizinhos(1)
        num_cores, coloracao = busca_BTDSATUR(grafo, cores, num_coloridos + 1, num_cores_encontrado, coloracao_encontrada)
        if num_cores < num_cores_encontrado:
            num_cores_encontrado = num_cores
            coloracao_encontrada = copy.deepcopy(coloracao)
        cores[i].pop()
        v.set_cor(None)
        v.satura_vizinhos(-1)

        # if sozinho == False and cores[i] == []:
        #     sozinho = True
    
    return (num_cores_encontrado, coloracao_encontrada)

def busca_gulosa_seq(grafo: Grafo, cores: dict[int: list[Vertice]] = None, num_coloridos: int = 0):
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    grafo.sort_vertices_grau()
    num_vertices = len(grafo.get_vertices())
    v = None
    for vert in grafo.get_vertices():
        if vert.get_cor() == None:
            v = vert
            break
    
    disponivel = list(range(num_vertices))
    for u in v.get_vizinhos():
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

def busca_DSATUR(grafo: Grafo, cores: dict[int: list[Vertice]] = None):
    if cores == None: cores = {i: [] for i in range(len(grafo.get_vertices()))}
    num_vertices = len(grafo.get_vertices())
    grafo.sort_vertices_grau()
    v = grafo.get_vertices()[0]
    v.set_cor(0)
    cores[0].append(v)
    v.satura_vizinhos(1)

    for _ in range(1, num_vertices):
        u = None
        for w in grafo.get_vertices():
            if w.get_cor() == None:
                if u == None:
                    u = w
                elif u.get_saturacao() < w.get_saturacao():
                    u = w
                elif u.get_saturacao() == w.get_saturacao():
                    if u.get_grau() < w.get_grau():
                        u = w

        disponivel = list(range(num_vertices))
        for w in u.get_vizinhos():
            if w.get_cor() in disponivel:
                disponivel.remove(w.get_cor())

        u.set_cor(disponivel[0])
        cores[disponivel[0]].append(u)

        u.satura_vizinhos(1)

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

    grafo = Grafo.gerar_grafo_generico(50, 25)

    print(grafo)

    print(busca_BTDSATUR(grafo))
    # print(busca_backtraking(grafo.reset_coloracao_vertices()))
