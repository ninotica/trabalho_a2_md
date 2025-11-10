"""Disciplinas FGV EMAp 2025.2"""
from itertools import combinations

class Disciplina:
    lista_disciplinas = []
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
        self.horario = horario
        self.dias = dias
        self.cor = None

        #aqui adicionamos numa lista com todas as disciplinas criadas
        Disciplina.lista_disciplinas.append(self)
    
    def __repr__(self):
        return f"{self.nome}"

    
    # @staticmethod
    # def set_dias_horarios():
    #     return {(dia, materia.horario) for materia in Disciplina.lista_disciplinas for dia in materia.dias}
    
    # @staticmethod
    # def blocos_validos():
    #     set_blocos = set([])
    #     # aqui definimos conjuntos de matérias que acontecem nos mesmos dias e horários, como ponto de partida
    #     for dia_e_horario in Disciplina.set_dias_horarios():
    #         bloco = set([materia for materia in Disciplina.lista_disciplinas if dia_e_horario[0] in materia.dias and dia_e_horario[1] == materia.horario])
    #         set_blocos.add(tuple(bloco))
    #     return [t1 for t1 in set_blocos if not any(set(t1).issubset(set(t2)) for t2 in set_blocos if t1 != t2)]

    #aqui definimos um dicionário com cada disciplina e as disciplinas que não podem ocorrer simultaneamente a ela
    @staticmethod
    def restricoes_basicas():
        restricoes = {}
        lista = Disciplina.lista_disciplinas
        for i in lista:
            restricoes[i] = set([])
            for j in lista:
                if j != i:
                    mesmo_periodo = (set(i.periodos) & set(j.periodos))
                    mesmo_curso = (set(i.curso) & set(j.curso))
                    if mesmo_periodo and mesmo_curso:
                        restricoes[i].add(j)
        return restricoes
   
################################################################################
# Setup Inicial
################################################################################

semestre = 2

if semestre == 2:
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

requerimentos_profs = {AR: 1, AL : 2} #chave é a disciplina, valor é o dia. 

alunos_puxando = { # set com listas de todas as disciplinas que o aluno com schedule incomum está puxando
(AL, AR, MD, LP, CVV, AEDV, EMD ),
(AL, AR, MD, LP, CVV, MFF),
(AC, AR, MD, LP, CVV, AEDV)
}
    
nr_dias = 7

restricoes = Disciplina.restricoes_basicas()

for schedule in alunos_puxando:
     for i in schedule:
          for j in schedule:
              if i != j:
                 restricoes[i].add(j)



for d in restricoes:
    print(d, ': ',restricoes[d])