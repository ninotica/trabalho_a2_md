import pandas as pd
import algoritmos
import time
import matplotlib.pyplot as plt
from pathlib import Path

def testa_velocidade_coloracoes(funcs: list, max_vertices=25, repeticoes=10, probabilidades=[10, 25, 50, 75]) -> pd.DataFrame:
    dados = [1]
    cols = ['tipo_grafo']
    for func in funcs:
        for i in probabilidades:
            grafos = [algoritmos.Grafo.gerar_grafo_generico(1, i) for _ in range(repeticoes)]
            start = time.time()
            for grafo in grafos:
                func(grafo)
            dados.append((time.time() - start) / repeticoes)
            cols.append(func.__name__ + '_' + str(i) + '%')
        average = 0
        for i in range(len(probabilidades)):
            average += dados[-i -1]
        dados.append(average / len(probabilidades))
        cols.append(func.__name__ + '_average')

    df = pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])

    for i in range(2, max_vertices + 1):
        dados = [i]
        for func in funcs:
            for j in probabilidades:
                grafos = [algoritmos.Grafo.gerar_grafo_generico(i, j) for _ in range(repeticoes)]
                start = time.time()
                for grafo in grafos:
                    func(grafo)
                dados.append((time.time() - start) / repeticoes)
            average = 0
            for j in range(len(probabilidades)):
                average += dados[-j -1]
            dados.append(average / len(probabilidades))
            print(f'grafo com {i} vértices avaliado para {func.__name__}')
        df = pd.concat([df, pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])], ignore_index=True)
    
    return df

def testa_precisao_coloracoes(funcs: list, max_vertices=25):
    # TODO: consertar isso aqui
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

if __name__ == '__main__':
    funcs = [algoritmos.busca_backtraking, algoritmos.busca_BTSL, algoritmos.busca_BTDSATUR]
    df = testa_velocidade_coloracoes(funcs, 15, 100)
    filepath = Path('data\BT-geral.csv')
    df.to_csv(filepath, index=False)

    print(df)
    fig1 = plt.figure(figsize=(16, 9))
    gs = fig1.add_gridspec(2, 3, hspace=0.35, wspace=0.25)

    ax1 = fig1.add_subplot(gs[0, 0])
    ax1.plot(df['tipo_grafo'], df['busca_backtraking_10%'], lw=1.0, color='r', label='Backtraking')
    ax1.plot(df['tipo_grafo'], df['busca_BTSL_10%'], lw=1.0, color='g', label='BTSL')
    ax1.plot(df['tipo_grafo'], df['busca_BTDSATUR_10%'], lw=1.0, color='b', label='BTDSATUR')
    ax1.set_title('10% de Densidade de Arestas')

    ax2 = fig1.add_subplot(gs[0, 1])
    ax2.plot(df['tipo_grafo'], df['busca_backtraking_25%'], lw=1.0, color='r', label='Backtraking')
    ax2.plot(df['tipo_grafo'], df['busca_BTSL_25%'], lw=1.0, color='g', label='BTSL')
    ax2.plot(df['tipo_grafo'], df['busca_BTDSATUR_25%'], lw=1.0, color='b', label='BTDSATUR')
    ax2.set_title('25% de Densidade de Arestas')

    ax3 = fig1.add_subplot(gs[0, 2])
    ax3.plot(df['tipo_grafo'], df['busca_backtraking_average'], lw=1.0, color='r', label='Backtraking')
    ax3.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL')
    ax3.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=1.0, color='b', label='BTDSATUR')
    ax3.set_title('Média Geral')

    ax4 = fig1.add_subplot(gs[1, 0])
    ax4.plot(df['tipo_grafo'], df['busca_backtraking_50%'], lw=1.0, color='r', label='Backtraking')
    ax4.plot(df['tipo_grafo'], df['busca_BTSL_50%'], lw=1.0, color='g', label='BTSL')
    ax4.plot(df['tipo_grafo'], df['busca_BTDSATUR_50%'], lw=1.0, color='b', label='BTDSATUR')
    ax4.set_title('50% de Densidade de Arestas')

    ax5 = fig1.add_subplot(gs[1, 1])
    ax5.plot(df['tipo_grafo'], df['busca_backtraking_75%'], lw=1.0, color='r', label='Backtraking')
    ax5.plot(df['tipo_grafo'], df['busca_BTSL_75%'], lw=1.0, color='g', label='BTSL')
    ax5.plot(df['tipo_grafo'], df['busca_BTDSATUR_75%'], lw=1.0, color='b', label='BTDSATUR')
    ax5.set_title('75% de Densidade de Arestas')

    ax6 = fig1.add_subplot(gs[1, 2])
    ax6.plot(df['tipo_grafo'], df['busca_backtraking_average'] / df['busca_backtraking_average'], lw=1.0, color='r', label='Backtraking')
    ax6.plot(df['tipo_grafo'], df['busca_BTSL_average'] / df['busca_backtraking_average'], lw=1.0, color='g', label='BTSL')
    ax6.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'] / df['busca_backtraking_average'], lw=1.0, color='b', label='BTDSATUR')
    ax6.set_title('Tempo de execução em relação ao backtracking')

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
    #     ax.plot(df['tipo_grafo'], df['busca_backtraking_average'], lw=1.0, color='r', label='Backtraking-Average', linestyle='--', alpha=0.6)
    #     ax.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL-Average', linestyle='-', alpha=0.5)
    #     ax.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=1.0, color='b', label='BTDSATUR-Average', linestyle='--', alpha=0.4)
        ax.legend()

    funcs.remove(algoritmos.busca_backtraking)
    df = testa_velocidade_coloracoes(funcs, 20, 100)  
    filepath = Path('data\BTSL-BTDSATUR.csv')
    df.to_csv(filepath, index=False)

    fig2 = plt.figure(figsize=(16, 9))
    gs = fig2.add_gridspec(2, 3, hspace=0.35, wspace=0.25)

    ax7 = fig2.add_subplot(gs[0, 0])
    ax7.plot(df['tipo_grafo'], df['busca_BTSL_10%'], lw=1.0, color='g', label='BTSL')
    ax7.plot(df['tipo_grafo'], df['busca_BTDSATUR_10%'], lw=1.0, color='b', label='BTDSATUR')
    ax7.set_title('10% de Densidade de Arestas')

    ax8 = fig2.add_subplot(gs[0, 1])
    ax8.plot(df['tipo_grafo'], df['busca_BTSL_25%'], lw=1.0, color='g', label='BTSL')
    ax8.plot(df['tipo_grafo'], df['busca_BTDSATUR_25%'], lw=1.0, color='b', label='BTDSATUR')
    ax8.set_title('25% de Densidade de Arestas')

    ax9 = fig2.add_subplot(gs[0, 2])
    ax9.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL')
    ax9.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=1.0, color='b', label='BTDSATUR')
    ax9.set_title('Média Geral')

    ax10 = fig2.add_subplot(gs[1, 0])
    ax10.plot(df['tipo_grafo'], df['busca_BTSL_50%'], lw=1.0, color='g', label='BTSL')
    ax10.plot(df['tipo_grafo'], df['busca_BTDSATUR_50%'], lw=1.0, color='b', label='BTDSATUR')
    ax10.set_title('50% de Densidade de Arestas')

    ax11 = fig2.add_subplot(gs[1, 1])
    ax11.plot(df['tipo_grafo'], df['busca_BTSL_75%'], lw=1.0, color='g', label='BTSL')
    ax11.plot(df['tipo_grafo'], df['busca_BTDSATUR_75%'], lw=1.0, color='b', label='BTDSATUR')
    ax11.set_title('75% de Densidade de Arestas')

    ax12 = fig2.add_subplot(gs[1, 2])
    ax12.plot(df['tipo_grafo'], df['busca_BTSL_average'] / df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL')
    ax12.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'] / df['busca_BTSL_average'], lw=1.0, color='b', label='BTDSATUR')
    ax12.set_title('Relação dos tempos de execução')

    for ax in [ax11, ax12, ax7, ax8, ax9, ax10]:
    #     ax.plot(df['tipo_grafo'], df['busca_backtraking_average'], lw=1.0, color='r', label='Backtraking-Average', linestyle='--', alpha=0.6)
    #     ax.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL-Average', linestyle='-', alpha=0.5)
    #     ax.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=1.0, color='b', label='BTDSATUR-Average', linestyle='--', alpha=0.4)
        ax.legend()

    fig1.suptitle('Tempo Médio de Execução Dado o Número de Vértices e Densidade de Arestas')
    fig2.suptitle('Tempo Médio de Execução Dado o Número de Vértices e Densidade de Arestas')
    plt.show()
