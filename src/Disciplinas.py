"""Disciplinas FGV EMAp 2025.2"""
import pandas as pd
from itertools import combinations
import os
import copy
import unicodedata
import random
from difflib import SequenceMatcher

class Disciplina:
    disciplinas = []
    def __init__(self, nome:str, horario:str, dias:list[str], periodos:list[int], curso:list=[1, 0], tem_prova=True, pre_requerimento_data=None, eh_dificil = False):
        """
        Classe Disciplina

        Parameters
        ----------
        nome : str
            Nome da Disciplina
        periodos : list
            Períodos em que a disciplina é ministrada. Vazio se for eletiva.
        curso : list
            Lista dos cursos que fazem a disciplina. 1=CD, 0=MAp
        horario : str
            horário em que a disciplina é ministrada.
        dias : list
            Lista de dias em que a disciplina é ministrada

        Returns
        -------
        None.

        """
            
        self.nome = nome
        self.periodos = periodos
        self.curso = curso
        self.horario = horario
        self.dias = dias
        self.tem_prova = tem_prova
        self.eh_dificil = eh_dificil
        self.cor = pre_requerimento_data
        self.saturacao = 0
        self.pode_mudar = True if pre_requerimento_data == None else False

        Disciplina.disciplinas.append(self)

    def get_cor(self):
        return self.cor
    
    def set_cor(self, cor):
        self.cor = cor

    def get_dificil(self):
        return self.eh_dificil

    @classmethod
    def set_dias_horarios(self):
        return {(dia, materia.horario) for materia in self.disciplinas_prova() for dia in materia.dias}
    
    @classmethod
    def blocos_iniciais(self):
        set_blocos = set([])
        # aqui definimos conjuntos de matérias que acontecem nos mesmos dias e horários, como ponto de partida
        for dia_e_horario in Disciplina.set_dias_horarios():
            bloco = set([materia for materia in self.disciplinas_prova() if dia_e_horario[0] in materia.dias and dia_e_horario[1] == materia.horario])
            set_blocos.add(tuple(bloco))
        return [t1 for t1 in set_blocos if not any(set(t1).issubset(set(t2)) for t2 in set_blocos if t1 != t2)]

    @classmethod
    def blocos_validos(self):
        vistos = set()
        nova_lista = []

        for tupla in self.blocos_iniciais():
            elementos_unicos = []
            for item in tupla:
                # Se o item ainda não foi visto, adicionamos à lista temporária
                if item not in vistos:
                    elementos_unicos.append(item)
                    vistos.add(item)
            
            # Opcional: Só adiciona a tupla se ela não estiver vazia
            # Se quiser manter tuplas vazias (ex: ()), remova o 'if elements_unicos'
            if elementos_unicos: 
                nova_lista.append(tuple(elementos_unicos))

        return nova_lista

    @classmethod
    def disciplinas_prova(self):
        return [d for d in self.disciplinas if d.tem_prova]

    def __repr__(self):
        return f"{self.nome}"
    
    def encontrar_equivalente(self, lista: list):
        for i in lista:
            if i.nome == self.nome:
                return i
        return False



class Restricoes:
    def __init__(self, lista_disciplinas: list[Disciplina], lista_restricoes_adicionais: list[tuple]):
        self.lista_disciplinas = lista_disciplinas
        self.lista_restricoes = lista_restricoes_adicionais
 
    def restricoes_basicas(self):
        """define um dicionário com as restricoes de disciplinas que não podem ocorrer num mesmo dia"""
        restricoes = set()
        for i, j in combinations(self.lista_disciplinas, 2):
            mesmo_periodo = (set(i.periodos) & set(j.periodos))
            mesmo_curso = (set(i.curso) & set(j.curso))
            if mesmo_periodo and mesmo_curso:
                restricoes.add((i, j))
        return restricoes

    def restrições_adicionais(self):
        '''adiciona restrições necessárias para cada aluno puxando disciplinas atípicas'''
        restricoes_adicionais = set()
        for schedule in self.lista_restricoes:
            for i, j in combinations(schedule, 2):
                i = i.encontrar_equivalente(self.lista_disciplinas)
                j = j.encontrar_equivalente(self.lista_disciplinas)
                if i and j and i.nome != j.nome:
                    restricoes_adicionais.add((i, j))
        return restricoes_adicionais
    
    def restricoes(self):
        return self.restricoes_basicas() | self.restrições_adicionais()

class Grafo:
    def __init__(self, arestas: Restricoes):
        self.elementos = arestas.lista_disciplinas
        self.restricoes = arestas.restricoes()
        self.restricoes_basicas = arestas.restricoes_basicas()
    
    def dict_format(self, basico=False):
        if not basico:
            restricoes = self.restricoes
        else:
            restricoes = self.restricoes_basicas
        dicionario = {}
        for i in self.elementos:
            dicionario[i] = set()
            for j in self.elementos:
                if (i, j) in restricoes or (j, i) in restricoes:
                    dicionario[i].add(j)
        return dicionario
    
    def get_vertices(self):
        return self.elementos
    
    def disciplinas_dia_fixo(self):
        return [d for d in self.elementos if not d.pode_mudar]

    def disciplinas_mutaveis(self):
        return [d for d in self.elementos if d.pode_mudar]

    def salvar_coloracao(self):
        return {i:i.cor for i in self.elementos if i.cor is not None}
    
    def restaurar_coloracao(self, coloracao:dict[Disciplina: int]):
        for v in coloracao:
            if v in self.get_vertices():
                v.set_cor(coloracao[v])
            else: v.set_cor(None)
        return self
    
    def restaurar_calendario(self, calendario:dict[int: list[Disciplina]]):
        for cor in calendario.keys():
            for c in calendario[cor]:
                for v in self.disciplinas_mutaveis:
                    if v.nome == c.nome:
                        v.set_cor(cor)
            
    
    def votar_coloracao_inicial(self):
        for v in self.disciplinas_mutaveis():
            v.set_cor(None)

    def calendario(self):
        cores = self.salvar_coloracao()
        calendario = {}
        for i in cores.values():
            if i not in calendario:
                calendario[i] = [d for d in self.elementos if d.cor == i]
        return dict(sorted(calendario.items()))
    
    def colorir_blocos_iniciais(self, blocos):
        i = 0
        cores_blocos = {}
        for bloco in blocos:
            for materia in bloco:
                if materia in self.disciplinas_dia_fixo():
                    cores_blocos[bloco] = materia.get_cor()
        for bloco in blocos:
            if bloco not in cores_blocos:
                while i in cores_blocos.values():
                    i += 1
                cores_blocos[bloco] = i
            for disciplina in bloco:
                if disciplina in self.disciplinas_mutaveis():
                    disciplina.set_cor(cores_blocos[bloco])
        
        while self.coloracao_invalida():
            i=0
            for k, j in self.coloracao_invalida():
                if k.pode_mudar:
                    while i in [c.get_cor() for c in self.get_vizinhos(k)]:
                        i+=1
                    k.set_cor(i)
                elif j.pode_mudar:
                    while i in [c.get_cor() for c in self.get_vizinhos(j)]:
                        i+=1
                    j.set_cor(i)
        return self.calendario()
    
    def pode_colorir(self, disciplina: Disciplina, dia: int) -> bool:
        """
        checa se pode designar esse dia para a disciplina
        """
        for vizinho in grafo.get_vizinhos(disciplina):
            if vizinho.get_cor() == dia:
                return False
        return True

    def reduzir_calendario(self, nr_dias_alvo = 7, max_loops = 10000):
        dict_cores = dict(sorted(self.calendario().items(), key=lambda item: len(item[1])))
        nr_loops = 0
        
        while len(self.calendario()) > nr_dias_alvo and nr_loops < max_loops - 1:
            for bloco in dict_cores.values():
                for materia in bloco:
                    if materia in self.disciplinas_mutaveis():
                        i = 0
                        while i in [c.get_cor() for c in self.get_vizinhos(materia)]:
                            i+=1
                        if i < nr_dias_alvo:
                            materia.set_cor(i)
                        nr_loops += 1
        return self.calendario()
    
    def requerimentos_razoaveis(self) -> bool:
        for materia in self.disciplinas_dia_fixo():
            for vizinho in self.get_vizinhos(materia):
                if vizinho in self.disciplinas_dia_fixo() and vizinho.get_cor() == materia.get_cor():
                    return False
        return True

    def coloracao_invalida(self) -> bool:
        duplas_invalidas = []
        for materia in self.get_vertices():
            for vizinho in self.get_vizinhos(materia):
                if vizinho.get_cor() != None and vizinho.get_cor() == materia.get_cor():
                    duplas_invalidas.append((vizinho, materia))
        return duplas_invalidas
    
    def sort_vertices_grau(self):
        for i in range(len(self.elementos)):
            for j in range(i + 1, len(self.elementos)):
                v = self.elementos[i]
                u = self.elementos[j]
                if self.get_grau(u) > self.get_grau(v):
                    temp = v
                    self.elementos[i] = u
                    self.elementos[j] = temp
    
    def get_grau(self, vertice):
        return len(self.dict_format()[vertice])
    
    def get_vizinhos(self, vertice):
        if vertice not in self.get_vertices():
            return []
        return self.dict_format()[vertice]
    
    def get_saturacao(self, vertice):
        saturacao = 0
        for vizinho in self.get_vizinhos(vertice):
            if vizinho.cor is not None:
                saturacao +=1
        return saturacao
    
    def pares_ruins(self):
        pares_ruins = []
        for dia in self.calendario():
            if (dia - 1) not in self.calendario():
                continue
            for materia in self.calendario()[dia]:
                if not materia.get_dificil():
                    continue
                for vizinho in grafo.dict_format(basico=True)[materia]:
                    if vizinho in self.calendario()[dia - 1]:
                        pares_ruins.append((vizinho, materia))
        return pares_ruins
    
    def ordem_ruindade(self):
        return len(self.pares_ruins())
    
    def ruindade_menor_igual(self, vertice, cor_nova):
        cor_atual = vertice.get_cor()
        k = self.ordem_ruindade()
        vertice.set_cor(cor_nova)
        j = self.ordem_ruindade()
        vertice.set_cor(cor_atual)
        return k >= j

    def busca_local_ruindade(self, max_iteracoes_inocuas = 100, nr_dias_max = 7):
        contador = 0 #conta a quantidade de iterações sem melhora
        while self.ordem_ruindade() > 0:
            pares = self.pares_ruins() #lista de pares de materias, onde uma é difícil e a outra antecede
            if not pares:
                break
            random.shuffle(pares)
            melhoria_global = False
            for vizinho, materia in pares:
                ruindade_previa = self.ordem_ruindade()
                mudou_cor = False
                dias_tentativa = list(range(nr_dias_max))
                random.shuffle(dias_tentativa)
                if vizinho.pode_mudar:
                    cor_original = vizinho.get_cor
                    for i in dias_tentativa:
                        if i == cor_original: continue
                        # Checa validade (Hard) e se melhora/mantém a ruindade (Soft)
                        if self.pode_colorir(vizinho, i) and self.ruindade_menor_igual(vizinho, i):
                            vizinho.set_cor(i)
                            mudou_cor = True
                            break # Conseguiu mover, para de procurar cor para este vértice               
                if not mudou_cor and materia.pode_mudar:
                    cor_original = materia.get_cor()
                    for i in dias_tentativa:
                        if i == cor_original: continue
                        
                        if self.pode_colorir(materia, i) and self.ruindade_menor_igual(materia, i):
                            materia.set_cor(i)
                            mudou_cor = True
                            break
                if self.ordem_ruindade() < ruindade_previa:
                    contador = 0
                    melhoria_global = True
                    break
            if not melhoria_global:
                contador += 1
            #se ultrapassa um certo numero de iterações sem melhorar, acaba o loop
            if contador > max_iteracoes_inocuas:
                break            
        return self.calendario(), self.ordem_ruindade()     

    def busca_BTDSATUR(self, cores: dict[int: list[Disciplina]] = {}, num_coloridos: int = 0, num_cores_encontrado=None, coloracao_encontrada={}):
        num_vertices = len(self.get_vertices())
        if num_coloridos == 0:
            for v in self.get_vertices():
                if not v.pode_mudar: 
                    num_coloridos += 1
            if coloracao_encontrada == {} and num_coloridos != 0: 
                coloracao_encontrada = {i: [] for i in range(len(self.get_vertices()))}
                for cor, vertices in self.calendario().items():
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
                cores = {i: [] for i in range(len(self.get_vertices()))}
                for u in self.get_vertices():
                    if not u.pode_mudar and not u in cores[cor]:
                        cores[u.cor].append(u)

        if num_cores_encontrado == None: num_cores_encontrado = num_vertices + 1
        if cores == {}: cores = {i: [] for i in range(len(self.get_vertices()))}
        
        max_cor = -1
        for v in self.get_vertices():
            cor = v.get_cor()
            if cor != None:
                if cor > max_cor:
                    if cor + 1 >= num_cores_encontrado:
                        return (num_cores_encontrado, coloracao_encontrada)
                    max_cor = cor

        if num_coloridos == num_vertices:
            return (max_cor + 1, cores) # já se sabe que max_cor + 1 < num_cores_encontrado devido ao loop anterior

        v = None
        for u in self.get_vertices():
            if u.get_cor() == None and u.pode_mudar:
                if v == None:
                    v = u
                elif self.get_saturacao(u) > self.get_saturacao(v):
                    v = u
                elif self.get_saturacao(u) == self.get_saturacao(v) and self.get_grau(u) > self.get_grau(v):
                    v = u
            
        blocked_colors = []

        for u in self.get_vizinhos(v):
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
            num_cores, coloracao = self.busca_BTDSATUR(cores, num_coloridos + 1, num_cores_encontrado, coloracao_encontrada)
            if num_cores < num_cores_encontrado:
                num_cores_encontrado = num_cores
                coloracao_encontrada = copy.deepcopy(coloracao)
            cores[i].pop()
            v.set_cor(None)

            disc_copiadas = [d for l in coloracao.values() for d in l ]

            for d in grafo.get_vertices():
                for d2 in disc_copiadas:
                    if d.nome == d2.nome:
                        d.set_cor(d2.cor)


            # if sozinho == False and cores[i] == []:
            #     sozinho = True
        return (num_cores_encontrado, coloracao_encontrada)

    def __str__(self):
        string = ""
        dic = self.dict_format()
        for i in dic:
            string.join(str(i) + " " + str(dic[i]))
        return string

def limpar_nome(texto):
    # Normaliza, remove acentos (encode ascii), volta pra string e troca espaço por _
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower().replace(' ', '_')

def nomes_parecidos_o_bastante(a: str, b: str, limiar=0.8):
    a = limpar_nome(a)
    b = limpar_nome(b)
    similaridade = SequenceMatcher(None, a, b).ratio()
    return similaridade > limiar

def carregar_disciplinas_do_arquivo(caminho_arquivo: str):

    """
    Carrega as disciplinas de um arquivo .csv ou .xlsx e as cria
    no escopo global usando a coluna 'nome_variavel'.
    
    O arquivo deve ter as colunas: 
    'nome', 'horario', 'dias', 'periodos', 'cursos', 'nome_variavel', 'tem_prova', 'eh_dificil', e 'data_prof_pediu'
    """
    try:
        if caminho_arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo, encoding='latin-1', delimiter=";")
        elif caminho_arquivo.endswith('.xlsx'):
            df = pd.read_excel(caminho_arquivo, encoding='latin-1', delimiter=";")
        else:
            raise ValueError("Formato de arquivo não suportado (.csv ou .xlsx).")
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em '{caminho_arquivo}'")
        return
    except Exception as e:
        print(f"ERRO ao ler o arquivo: {e}")
        return

    # Limpa a lista de disciplinas existente para evitar duplicatas
    Disciplina.disciplinas = []
    
    print(f"Carregando disciplinas de '{caminho_arquivo}'")

    for _, row in df.iterrows():
        # Trata valores NaN (células vazias) do Excel
        nome = row['nome']
        horario = str(row['horario'])
        nome_variavel = str(row['nome_variavel']).strip()
        tem_prova = bool(row['tem_prova'])
        eh_dificil = bool(row['eh_dificil'])

        if pd.notna(row['data_prof_pediu']):
            data_prof_pediu = int(row['data_prof_pediu'])
        else:
            data_prof_pediu = None

        # Processa dias: "seg,qua,sex" -> ["seg", "qua", "sex"]
        dias_list = []
        if pd.notna(row['dias']):
            dias_list = [dia.strip() for dia in str(row['dias']).split(',')]

        # Processa periodos: "4,6" -> [4, 6] ou "" -> []
        periodos_list = []
        if pd.notna(row['periodos']) and str(row['periodos']).strip():
            try:
                periodos_list = [int(p.strip()) for p in str(row['periodos']).split(',')]
            except ValueError:
                print(f"  Aviso: Valor de 'periodos' inválido para '{nome}'. Usando [].")
                
        # Processa cursos: "CD" -> [1], "MAp" -> [0], "CD,MAp" ou "" -> [1, 0]
        curso_arg = [1, 0] # Default
        if pd.notna(row['cursos']):
            cursos_str = str(row['cursos']).lower().strip()
            if cursos_str == 'cd':
                curso_arg = [1]
            elif cursos_str == 'map':
                curso_arg = [0]
            # Nota: "cd,map" ou "" já caem no default [1, 0]
            
        if not nome or not nome_variavel or nome_variavel == 'nan':
            print(f"  Aviso: Pulando linha por falta de 'nome' ou 'nome_variavel'.")
            continue

        # Cria a instância da Disciplina
        nova_disciplina = Disciplina(
            nome=nome,
            horario=horario,
            dias=dias_list,
            periodos=periodos_list,
            curso=curso_arg,
            tem_prova=tem_prova,
            pre_requerimento_data=data_prof_pediu,
            eh_dificil=eh_dificil
        )
        
        # *** A MÁGICA ***
        # Injeta a variável no escopo global do script
        # ex: globals()['AR'] = nova_disciplina
        globals()[nome_variavel] = nova_disciplina

    print(f"Carregadas {len(Disciplina.disciplinas)} disciplinas.")

def carregar_relacao_alunos(caminho_arquivo: str):
    """
    Lê um arquivo Excel com múltiplas abas e retorna um dicionário.
    Chave: Nome da aba (Disciplina)
    Valor: Lista de matrículas (primeira coluna da aba)
    """
    # sheet_name=None faz o pandas ler TODAS as abas e retornar um dicionário
    # onde a chave é o nome da aba e o valor é o DataFrame
    dados_brutos = pd.read_excel(caminho_arquivo, sheet_name=None)

    disciplinas_alunos = {}

    for disciplina, df in dados_brutos.items():
        # Verifica se a aba não está vazia
        if not df.empty:
            lista_matriculas = df.iloc[:, 0].dropna().tolist()
            
            disciplinas_alunos[disciplina] = lista_matriculas
    
    nome_disciplina = {}

    relacao_disciplinas = {}

    for nome in disciplinas_alunos.keys():
        for disciplina in Disciplina.disciplinas:
            if nomes_parecidos_o_bastante(nome, disciplina.nome):
                relacao_disciplinas[disciplina] = disciplinas_alunos[nome]
                nome_disciplina[nome] = disciplina
    
    if set(nome_disciplina.keys()) != set(disciplinas_alunos.keys()):
        print("CUIDADO: as disciplinas podem não ter sido identificadas corretamente")
    
    if len(nome_disciplina) < len(Disciplina.disciplinas):
        print(f"CUIDADO: as disciplinas {set(Disciplina.disciplinas) - set(nome_disciplina.values())} não foram carregadas corretamente")

    return relacao_disciplinas

def schedules_from_relacao_alunos(relacao_alunos):
    schedules = {}
    for materia in relacao_alunos.keys():
        for matricula in relacao_alunos[materia]:
            if matricula in schedules:
                schedules[matricula].append(materia)
            else:
                schedules[matricula] = [materia]
    for matricula in schedules:
        schedules[matricula] = tuple(schedules[matricula])
    return set(schedules.values())


################################################################################
# Driver Code
################################################################################
# Setup Inicial
nr_dias = 7

file_path = os.path.join('data', 'disciplinas.csv')
carregar_disciplinas_do_arquivo(file_path)

chamada_path = os.path.join('data', 'EMAp_20252.xlsx')
chamadas = carregar_relacao_alunos(chamada_path)
schedules = list(schedules_from_relacao_alunos(chamadas))

materias = Disciplina.disciplinas_prova()
restricoes = Restricoes(materias, schedules)
grafo = Grafo(restricoes)

# Criação do calendário

if not grafo.requerimentos_razoaveis():
    print("Os requerimentos feitos pelos professores são incoerentes, não é possível construir um calendário de provas")
else:
    grafo.busca_BTDSATUR()
    _, ordem_ruindade = grafo.busca_local_ruindade(nr_dias_max=nr_dias)
    
    calendario = grafo.calendario()

# Exibição do calendário na tela

    for i in calendario:
        print(f"Dia {i+1}:")
        print("Provas:", calendario[i])
    
    print("Número de materias difíceis com prova no dia anterior: ", ordem_ruindade)