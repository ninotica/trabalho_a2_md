"""Disciplinas FGV EMAp 2025.2"""
import pandas as pd
from itertools import combinations
import os
import copy
import unicodedata
import random

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

class Restricoes:
    def __init__(self, lista_disciplinas: list[Disciplina], lista_restricoes_adicionais):
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
                if i in self.lista_disciplinas and j in self.lista_disciplinas:
                    restricoes_adicionais.add((i, j))
        return restricoes_adicionais
    
    def restricoes(self):
        return self.restricoes_basicas() | self.restrições_adicionais()

class Grafo:
    def __init__(self, vertices: Disciplina, arestas: Restricoes):
        self.elementos = vertices
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
        for v in self.get_vertices():
            if v in coloracao:
                v.set_cor(coloracao[v])
            else: v.set_cor(None)
        return self

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

    def MRNA_ruindade(self, max_iteracoes_inocuas = 100, nr_dias_max = 7):
        contador = 0
        while self.ordem_ruindade() > 0:
            pares = self.pares_ruins()
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
            
            if contador > max_iteracoes_inocuas:
                break            
        return self.calendario(), self.ordem_ruindade()     

    def __str__(self):
        string = ""
        dic = self.dict_format()
        for i in dic:
            string.join(str(i) + " " + str(dic[i]))
        return string

def limpar_nome(texto):
    # Normaliza, remove acentos (encode ascii), volta pra string e troca espaço por _
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower().replace(' ', '_')

def carregar_disciplinas_do_arquivo(caminho_arquivo: str):

    """
    Carrega as disciplinas de um arquivo .csv ou .xlsx e as cria
    no escopo global usando a coluna 'nome_variavel'.
    
    O arquivo deve ter as colunas: 
    'nome', 'horario', 'dias', 'periodos', 'cursos', 'nome_variavel'
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
    
    print(f"Carregando disciplinas de '{caminho_arquivo}'...")

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

################################################################################
# Setup Inicial
################################################################################
file_path = os.path.join('data', 'disciplinas_gemini.csv')
carregar_disciplinas_do_arquivo(file_path)

nr_dias = 7


#TODO: Implementar importação de arquivos do Excel da Claudinha
alunos_puxando = { # set com listas de todas as disciplinas que o aluno com schedule incomum está puxando
(AL, AR, MD, LP, CVV, AEDV, EMD),
(AL, AR, MD, LP, CVV, MFF),
(AC, AL, MD, LP, CVV, AEDV),
}

################################################################################
# Criação do Grafo
################################################################################
restricoes = Restricoes(Disciplina.disciplinas_prova(), alunos_puxando)
grafo = Grafo(Disciplina.disciplinas_prova(), restricoes)

################################################################################
# Criação do calendário
################################################################################
grafo.colorir_blocos_iniciais(Disciplina.blocos_validos())

print(grafo.reduzir_calendario())

print(grafo.MRNA_ruindade())


