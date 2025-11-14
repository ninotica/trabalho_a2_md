import pandas as pd
import algoritmos
import time

def testa_velocidade_coloracoes(funcs: list, max_vertices=25, repeticoes=10) -> pd.DataFrame:
    dados = ['1_10%']
    cols = ['tipo_grafo']
    for func in funcs:
        grafos = [algoritmos.Grafo.gerar_grafo_generico(1, 10) for _ in range(repeticoes)]
        start = time.time()
        for grafo in grafos:
            func(grafo)
        dados.append((time.time() - start) / repeticoes)
        cols.append(func.__name__)

    df = pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])
    for i in [25, 50, 75]:
        dados = ['1_' + str(i) + '%']
        for func in funcs:
            grafos = [algoritmos.Grafo.gerar_grafo_generico(1, i) for _ in range(repeticoes)]
            start = time.time()
            for grafo in grafos:
                func(grafo)
            dados.append((time.time() - start) / repeticoes)
        df = pd.concat([df, pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])], ignore_index=True)

    for i in range(2, max_vertices + 1):
        for j in [10, 25, 50, 75]:
            dados = [str(i) + '_' + str(j) + '%']
            for func in funcs:
                grafos = [algoritmos.Grafo.gerar_grafo_generico(i, j) for _ in range(repeticoes)]
                start = time.time()
                for grafo in grafos:
                    func(grafo)
                dados.append((time.time() - start) / repeticoes)
            df = pd.concat([df, pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])], ignore_index=True)
    
    return df

def testa_precisao_coloracoes(funcs: list, max_vertices=25):
    dados = ['1_10%']
    cols = ['tipo_grafo']
    grafo = algoritmos.Grafo.gerar_grafo_generico(1, 10)
    for func in funcs:
        num_cores, _ = func(grafo)
        dados.append(num_cores)
        cols.append(func.__name__)
        grafo.reset_coloracao_vertices()

    df = pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])
    for i in [25, 50, 75]:
        dados = ['1_' + str(i) + '%']
        grafo = algoritmos.Grafo.gerar_grafo_generico(1, i)
        for func in funcs:
            num_cores, _ = func(grafo)
            dados.append(num_cores)
            grafo.reset_coloracao_vertices()
        df = pd.concat([df, pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])], ignore_index=True)

    for i in range(2, max_vertices + 1):
        for j in [10, 25, 50, 75]:
            dados = [str(i) + '_' + str(j) + '%']
            grafo = algoritmos.Grafo.gerar_grafo_generico(i, j)
            for func in funcs:
                num_cores, _ = func(grafo)
                dados.append(num_cores)
                grafo.reset_coloracao_vertices()
            df = pd.concat([df, pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])], ignore_index=True)
    
    return df

funcs = [algoritmos.busca_gulosa_seq, algoritmos.busca_DSATUR, algoritmos.busca_backtraking, algoritmos.busca_BTDSATUR]
df = testa_velocidade_coloracoes(funcs)

print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '10%'])
print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '25%'])
print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '50%'])
print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '75%'])

print('\n\n')

# df = testa_precisao_coloracoes(funcs)

# print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '10%'])
# print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '25%'])
# print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '50%'])
# print(df[df['tipo_grafo'].apply(lambda x: x.split('_')[1]) == '75%'])
