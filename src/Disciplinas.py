"""Disciplinas FGV EMAp 2025.2"""
import pandas as pd
from itertools import combinations
import os
import algoritmos

class Disciplina:
    disciplinas = []
    def __init__(self, nome:str, horario:str, dias:list[str], periodos:list[int], curso:list=[1, 0], tem_prova=True, pre_requerimento_data=None):
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
        self.tem_prova = tem_prova
        self.eh_dificil = False
        self.cor = pre_requerimento_data

        Disciplina.disciplinas.append(self)

    @classmethod
    def disciplinas_prova(self):
        return [d for d in Disciplina.disciplinas if d.tem_prova]

    def __repr__(self):
        return f"{self.nome}"
    
    def to_Vertice(self):
        return algoritmos.Vertice(self.nome)

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
    
    def to_Vertice(self):
        restricoes = self.restricoes()
        vertices = [v.to_Vertice() for v in Disciplina.disciplinas_prova()]
        restricoes_vert = []
        for (v, u) in restricoes:
            for vertice in vertices:
                if v.nome == vertice.get_label():
                    v = vertice
                    break
            for vertice in vertices:
                if u.nome == vertice.get_label():
                    u = vertice
                    break
            
            restricoes_vert.append((v, u))

        return restricoes_vert

class Grafo:
    def __init__(self, vertices, arestas):
        self.elementos = vertices
        self.restricoes = arestas
    
    def dict_format(self):
        dicionario = {}
        for i in self.elementos:
            dicionario[i] = set()
            for j in self.elementos:
                if (i, j) in self.restricoes or (j, i) in self.restricoes:
                    dicionario[i].add(j)
        return dicionario
    
    def coloracao(self):
        return {i:i.cor for i in self.elementos}
    
    def calendario(self):
        cores = {i.cor for i in self.elementos if i.cor is not None}
        calendario = {}
        for i in cores:
            calendario[i] = [d for d in self.elementos if d.cor == i]
            return calendario
    
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
            pre_requerimento_data=data_prof_pediu
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

solucoes_desejadas = 5

requerimentos_profs = {AR: 1, AL : 2} #chave é a disciplina, valor é o dia. 

alunos_puxando = { # set com listas de todas as disciplinas que o aluno com schedule incomum está puxando
(AL, AR, MD, LP, CVV, AEDV, EMD),
(AL, AR, MD, LP, CVV, MFF),
(AC, AL, MD, LP, CVV, AEDV),
}

materias_dificeis = {MD, AL}

################################################################################
# Criação do Grafo
################################################################################
restricoes = Restricoes(Disciplina.disciplinas_prova(), alunos_puxando)
grafo = Grafo(Disciplina.disciplinas_prova(), restricoes.restricoes())
drafo = grafo.dict_format()
for d in drafo:
    print("*", d, ":", drafo[d])

grafo_ruda = algoritmos.Grafo([v.to_Vertice() for v in Disciplina.disciplinas_prova()], restricoes.to_Vertice())
print(grafo_ruda)