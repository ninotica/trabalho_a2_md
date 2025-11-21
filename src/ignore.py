import unicodedata
from difflib import SequenceMatcher

def limpar_nome(texto):
    # Normaliza, remove acentos (encode ascii), volta pra string e troca espaço por _
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower().replace(' ', '_')

def nomes_parecidos_o_bastante(a: str, b: str, limiar=0.8):
    similaridade = SequenceMatcher(None, a, b).ratio()
    return similaridade > limiar

t1 = limpar_nome("Analise exploratoria de dados e")
t2 = limpar_nome("analise exploratoria de dados e visualização")

t3 = limpar_nome("Álgebra linear")
t4 = limpar_nome("algebra e criptografia")

print(nomes_parecidos_o_bastante(t1, t2))
print(nomes_parecidos_o_bastante(t3, t4))

print(t1, t2, t3, t4)