"""Disciplinas FGV EMAp 2025.2"""

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
            Lista dos cursos que fazem a disciplina. 1=CD, 0=MAp.
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
        
        Disciplina.lista_disciplinas.append(self)

#aqui definimos cada disciplina     
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
AC = Disciplina("Algebra e Criptografia", "7h30", ["ter", "qui"], [4], [0])
ES = Disciplina("Engenharia de Software", "7h30", ["ter", "qui"], [6])
AP = Disciplina("Aprendizado Profundo", "9h20", ["ter", "qui"], [6])
ST = Disciplina("Séries Temporais", "11h10", ["ter", "qui"], [6])
PE = Disciplina("Processos Estocásticos", "9h20", ["seg", "qua"], [6], [0])
EDP = Disciplina("Equações Diferenciais Parciais", "9h20", ["ter", "qui"], [6], [0])
IAN = Disciplina("Introdução à Análise Numérica", "11h10", ["ter", "qui"], [6], [0])


set_dias_horarios = set([(dia, materia.horario) for materia in Disciplina.lista_disciplinas for dia in materia.dias])
set_blocos = set([])

#aqui definimos conjuntos de matérias que acontecem nos mesmos dias e horários, como ponto de partida
for dia_e_horario in set_dias_horarios:
    bloco = set([materia for materia in Disciplina.lista_disciplinas if dia_e_horario[0] in materia.dias and dia_e_horario[1] == materia.horario])
    set_blocos.add(tuple(bloco))

blocos_validos ={t1 for t1 in set_blocos if not any(set(t1).issubset(set(t2)) for t2 in set_blocos if t1 != t2)}

def printar_legível(set_de_blocos):
    """
    printa elemento a elemento de iteravel de iteraveis de disciplinas 
    (que sem isso ficam ilegíveis)
    """    
    lista_blocos = [[materia.nome for materia in bloco] for bloco in set_de_blocos]
    print("#"*80)
    for elemento in lista_blocos:
        print(elemento)
    print("num de elementos = ", len(lista_blocos))

#just checking
printar_legível(set_blocos)
printar_legível(blocos_validos)