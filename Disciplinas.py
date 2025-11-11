"""Disciplinas FGV EMAp 2025.2"""

class Disciplina:
    disciplinas_prova = []
    def __init__(self, nome:str, horario:str, dias:list[str], periodos:list[int], curso:list=[1, 0]):
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
        self.tem_prova = True
        self.cor = None

        Disciplina.disciplinas_prova.append(self)



    def __repr__(self):
        return f"{self.nome}"
    
    @classmethod
    def __coloracao__(self):
        return {i : i.cor for i in Disciplina.disciplinas_prova if i.cor is not None}
    
    @classmethod
    def grafo_restricoes_basicas(self):
        """define um dicionário com as restricoes de disciplinas que não podem ocorrer num mesmo dia"""
        restricoes = {}
        for i in Disciplina.disciplinas_prova:
            restricoes[i] = set([])
            for j in Disciplina.disciplinas_prova:
                if j != i:
                    mesmo_periodo = (set(i.periodos) & set(j.periodos))
                    mesmo_curso = (set(i.curso) & set(j.curso))
                    if mesmo_periodo and mesmo_curso:
                        restricoes[i].add(j)
        return restricoes
    
    @classmethod
    def restrições_adicionais(self, schedules_atípicos):
        '''adiciona restrições necessárias para cada aluno puxando disciplinas atípicas'''
        grafo = Disciplina.grafo_restricoes_basicas()
        for schedule in schedules_atípicos:
            for i in schedule:
                for j in schedule:
                    if i in Disciplina.disciplinas_prova and j in Disciplina.disciplinas_prova and i != j:
                        grafo[i].add(j)
        return grafo

################################################################################
# Setup Inicial
################################################################################
semestre = 2

if semestre == 2: #seta as disciplinas de semestres ímpares
    CUV = Disciplina("Cálculo em uma Variável", "9h20", ["seg", "qua", "sex"], [1])
    LP = Disciplina("Linguagens de Programação", "7h30", ["seg", "qua", "sex"], [2])
    CVV = Disciplina("Cálculo em Várias Variáveis", "9h20", ["seg", "qua", "sex"], [2])
    AL = Disciplina("Algebra Linear", "11h10", ["seg", "qua", "sex"], [2])
    AEDV = Disciplina("Análise Exploratória de Dados e Visualização", "9h20", ["ter", "qui"], [2], [1])
    MFF = Disciplina("Modelagem de Fenômenos Físicos", "9h20", ["ter", "qui"], [2], [0])
    MD = Disciplina("Matemática Discreta", "11h10", ["ter", "qui"], [2])
    PAA = Disciplina("Projeto e Análise de Algoritmos", "7h30", ["seg", "qua"], [4], [1])
    CR = Disciplina("Ciência de Redes", "9h20", ["seg", "qua"], [4, 6], [1])
    MI = Disciplina("Modelagem Informacional", "11h10", ["seg", "qua"], [4], [1])
    IE = Disciplina("Inferência Estatística", "9h20", ["ter", "sex"], [4])
    OCD = Disciplina("Otimização para Ciência de Dados", "11h10", ["ter", "qui"], [4], [1])
    HM = Disciplina("História da Matemática", "11h10", ["seg", "qua"], [], [0])
    AR = Disciplina("Análise na Reta", "14h20", ["seg", "qua", "sex"], [4], [0])
    AC = Disciplina("Algebra e Criptografia", "7h30", ["ter", "qui"], [4, 8], [0])
    ES = Disciplina("Engenharia de Software", "7h30", ["ter", "qui"], [6], [1])
    AP = Disciplina("Aprendizado Profundo", "9h20", ["ter", "qui"], [6], [1])
    ST = Disciplina("Séries Temporais", "11h10", ["ter", "qui"], [6], [1])
    PE = Disciplina("Processos Estocásticos", "9h20", ["seg", "qua"], [6], [0])
    EDP = Disciplina("Equações Diferenciais Parciais", "9h20", ["ter", "qui"], [6], [0])
    IAN = Disciplina("Introdução à Análise Numérica", "11h10", ["ter", "qui"], [6], [0])
    EMD = Disciplina("Ética na Manipulação de Dados", "11h10", ["ter", "qui"], [8], [1])
    OC = Disciplina("Otimização Contínua", "11h10", ["seg", "qua"], [8], [0])

nr_dias = 7

requerimentos_profs = {AR: 1, AL : 2} #chave é a disciplina, valor é o dia. 

solucoes_desejadas = 5

alunos_puxando = { # set com listas de todas as disciplinas que o aluno com schedule incomum está puxando
(AL, AR, MD, LP, CVV, AEDV, EMD),
(AL, AR, MD, LP, CVV, MFF),
(AC, AL, MD, LP, CVV, AEDV)
}

materias_dificeis = {MD, AL}

################################################################################
# Criação do Grafo
################################################################################

grafo = Disciplina.restrições_adicionais(alunos_puxando)

if __name__ == "__main__":
    for d in grafo:
        print(d, ': ',grafo[d])
