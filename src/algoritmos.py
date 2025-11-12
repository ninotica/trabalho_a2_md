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
        return self.label
    
    def __repr__(self):
        return str(self.label)
    
    # def __eq__(self, value):
    #     if not isinstance(value, Vertice):
    #         return NotImplemented
    #     return self.label == value.label and self.grau == value.grau and self.cor == value.cor and self.vizinhos == value.vizinhos
    
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

    def get_vizinhos(self):
        return self.vizinhos
    
class Aresta():
    def __init__(self, vertice1, vertice2):
        self.aresta = set([vertice1, vertice2])
    
    def __str__(self):
        return set([v.__str__() for v in self.aresta])
    
    def __repr__(self):
        return str(set([v.__str__() for v in self.aresta]))
    
    def get_aresta(self):
        return self.aresta
    
class Grafo():
    def __init__(self, vertices: list[Vertice], arestas: list[Aresta]):
        self.vertices = copy.deepcopy(vertices)
        self.arestas = copy.deepcopy(arestas)
    
    def __str__(self):
        return f"Vértices:\n{[v.__str__() for v in self.vertices]}\n\nArestas:\n{[e.__str__() for e in self.arestas]}"
    
    def set_vertices(self, vertices):
        self.vertices = vertices

    def get_vertices(self):
        return self.vertices
    
    def sort_vertices_grau(self):
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                v = vertices[i]
                u = vertices[j]
                if u.get_grau() < v.get_grau():
                    temp = v
                    vertices[i] = u
                    vertices[j] = v

    def get_arestas(self):
        return self.arestas       
    
def busca_backtraking(grafo: Grafo, cores: dict[int: list[Vertice]], num_coloridos: int, num_cores_encontrado=None, coloracao_encontrada=None):
    num_vertices = len(grafo.get_vertices())
    if num_cores_encontrado == None: num_cores_encontrado = num_vertices + 1
    v = None
    for vertice in grafo.get_vertices():
        if vertice.get_cor() == None:
            v = vertice
            break
    
    max_cor = 0
    for cor in [vert.get_cor() for vert in grafo.get_vertices()]:
        if cor != None:
            if cor > max_cor: 
                max_cor = cor

    if num_coloridos == num_vertices:
        if max_cor + 1 < num_cores_encontrado:
            num_cores_encontrado = max_cor + 1
            coloracao_encontrada = cores

        return (num_cores_encontrado, coloracao_encontrada)

    disponivel = [True for _ in range(num_vertices)]

    for u in v.get_vizinhos():
        if u.get_cor() != None:
            disponivel[u.get_cor()] = False

    for i in range(max_cor + 2):
        if i == num_vertices: break
        if i > num_cores_encontrado:
            return (num_cores_encontrado, coloracao_encontrada)
        if disponivel[i]:
            v.set_cor(i)
            cores[i].append(v)
            num_cores, coloracao = busca_backtraking(grafo, cores, num_coloridos + 1, num_cores_encontrado, coloracao_encontrada)
            if num_cores < num_cores_encontrado:
                num_cores_encontrado = num_cores
                coloracao_encontrada = copy.deepcopy(coloracao)
            cores[i].pop()
            v.set_cor(None)
    
    return (num_cores_encontrado, coloracao_encontrada)

def busca_gulosa_seq(grafo: Grafo, cores: dict[int: list[Vertice]], num_coloridos: int=0):
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

    if num_coloridos + 1 == num_vertice:
        qtd_cor = 0
        for cor in cores.values():
            if len(cor) == 0:
                break
            qtd_cor += 1
        return (qtd_cor, cores)
    
    return busca_gulosa_seq(grafo, cores, num_coloridos + 1)

def busca_DSATUR(grafo: Grafo, cores: dict[int: list[Vertice]]):
    num_vertices = len(grafo.get_vertices())
    grafo.sort_vertices_grau()
    v = grafo.get_vertices()[0]
    for u in v.get_vizinhos():
        u.set_saturacao(u.get_saturacao() + 1)

    for u in [u2 for u2 in grafo.get_vertices() if u2 != v]:
        v2 = u
        for v3 in [v4 for v4 in grafo.get_vertices() if v4.get_cor() == None]:
            if v3.get_saturacao() > v2.get_saturacao():
                v2 = v3
        
        disponivel = list(range(num_vertices))
        for v3 in v2.get_vizinhos():
            if v3.get_cor() in disponivel:
                disponivel.remove(v3.get_cor())

        v2.set_cor(disponivel[0])
        cores[disponivel[0]].append(v2)

        for v3 in v2.get_vizinhos():
            v3.set_saturacao(v3.get_saturacao() + 1)

    qtd_cor = 0
    for cor in cores.values():
        if len(cor) == 0:
            break
        qtd_cor += 1

    return (qtd_cor, cores)

    

if __name__ == '__main__':
    num_vertice = 25
    vertices = [Vertice(i) for i in range(num_vertice)]
    arestas = []
    for i in range(num_vertice):
        for j in range(i+1, num_vertice):
            if random.randint(1, 10) > 5:
                vertices[i].add_vizinho(vertices[j])
                vertices[j].add_vizinho(vertices[i])
                arestas.append(Aresta(vertices[i], vertices[j]))
                vertices[i].set_grau(vertices[i].get_grau() + 1)
                vertices[j].set_grau(vertices[j].get_grau() + 1)

    grafo = Grafo(vertices, arestas)
    cores = {i: [] for i in range(num_vertice)}

    # grafo = inicializar_grafo(grafo)
    print(grafo)
    # for v in vertices:
    #     print([u.get_label() for u in v.get_vizinhos()])

    print('\n\nbla bla bla\n\n')
    # num_cores, coloracao = busca_backtraking(grafo, copy.deepcopy(cores), 0)
    # print(num_cores)
    # print(coloracao)
    # for v in grafo.get_vertices():
        # v.set_cor(None)

    num_cores, coloracao = busca_gulosa_seq(grafo, copy.deepcopy(cores))
    print(num_cores)
    print(coloracao)
    for v in grafo.get_vertices():
        v.set_cor(None)

    num_cores, coloracao = busca_DSATUR(grafo, copy.deepcopy(cores))
    print(num_cores)
    print(coloracao)
    for v in grafo.get_vertices():
        v.set_cor(None)

    num_cores, coloracao = busca_backtraking(grafo, copy.deepcopy(cores), 0, num_cores, coloracao)
    print(num_cores)
    print(coloracao)
    for v in grafo.get_vertices():
        v.set_cor(None)
