import pandas as pd
import algoritmos_ruda as alg
import time
import matplotlib.pyplot as plt
from pathlib import Path

def testa_velocidade_coloracoes(funcs: list, min_vertices=1, max_vertices=25, repeticoes=10, probabilidades=[10, 25, 50, 75], filepath: Path= None) -> pd.DataFrame:
    dados = [min_vertices]
    cols = ['tipo_grafo']
    for func in funcs:
        for i in probabilidades:
            grafos = [alg.Grafo.gerar_grafo_generico(1, i) for _ in range(repeticoes)]
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

    for i in range(min_vertices + 1, max_vertices + 1):
        dados = [i]
        for func in funcs:
            for j in probabilidades:
                grafos = [alg.Grafo.gerar_grafo_generico(i, j) for _ in range(repeticoes)]
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
        if filepath != None: df.to_csv(filepath, index=False)
    
    return df

def testa_precisao_coloracoes(funcs: list, min_vertice=1, max_vertice=25, repeticoes=10, probabilidades=[10, 25, 50, 75], filepath: Path= None):
    dados = [min_vertice]
    cols = ['tipo_grafo']
    for i in probabilidades:
        grafos = [alg.Grafo.gerar_grafo_generico(min_vertice, i) for _ in range(repeticoes)]
        for func in funcs:
            media = 0
            for j in range(repeticoes):
                num_cromatico, _ = func(grafos[j])
                grafos[j].reset_coloracao_vertices()
                media += num_cromatico
            dados.append(media / repeticoes)
            cols.append(func.__name__ + '_' + str(i) + '%')

    df = pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])

    for i in range(min_vertice + 1, max_vertice + 1):
        dados = [i]
        for j in probabilidades:
            grafos = [alg.Grafo.gerar_grafo_generico(i, j) for _ in range(repeticoes)]
            for func in funcs:
                media = 0
                for k in range(repeticoes):
                    num_cromatico, _ = func(grafos[k])
                    grafos[k].reset_coloracao_vertices()
                    media += num_cromatico
                dados.append(media / repeticoes)
                print(f'grafo com {i} vértices e {j}% de arestas avaliado para {func.__name__}')
        df = pd.concat([df, pd.DataFrame([pd.Series(dados, index=cols)], columns=cols, index=[1])], ignore_index=True)
        if filepath != None: df.to_csv(filepath, index=False)
    
    return df

def graficos_tempo_geral(fig, df):
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.25)
    cor1 = "#DFA000"
    cor2 = "#2DB5C7"
    cor3 = "#A81D6F"
    lw = 2.0

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(df['tipo_grafo'], df['busca_backtraking_10%'], lw=lw, color=cor1, label='Backtraking')
    ax1.plot(df['tipo_grafo'], df['busca_BTSL_10%'], lw=lw, color=cor2, label='BTSL')
    ax1.plot(df['tipo_grafo'], df['busca_BTDSATUR_10%'], lw=lw, color=cor3, label='BTDSATUR')
    ax1.set_title('10% de Densidade de Arestas')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(df['tipo_grafo'], df['busca_backtraking_25%'], lw=lw, color=cor1, label='Backtraking')
    ax2.plot(df['tipo_grafo'], df['busca_BTSL_25%'], lw=lw, color=cor2, label='BTSL')
    ax2.plot(df['tipo_grafo'], df['busca_BTDSATUR_25%'], lw=lw, color=cor3, label='BTDSATUR')
    ax2.set_title('25% de Densidade de Arestas')

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(df['tipo_grafo'], df['busca_backtraking_average'], lw=lw, color=cor1, label='Backtraking')
    ax3.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=lw, color=cor2, label='BTSL')
    ax3.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=lw, color=cor3, label='BTDSATUR')
    ax3.set_title('Média Geral')

    ax4 = fig.add_subplot(gs[1, 0])
    ax4.plot(df['tipo_grafo'], df['busca_backtraking_50%'], lw=lw, color=cor1, label='Backtraking')
    ax4.plot(df['tipo_grafo'], df['busca_BTSL_50%'], lw=lw, color=cor2, label='BTSL')
    ax4.plot(df['tipo_grafo'], df['busca_BTDSATUR_50%'], lw=lw, color=cor3, label='BTDSATUR')
    ax4.set_title('50% de Densidade de Arestas')

    ax5 = fig.add_subplot(gs[1, 1])
    ax5.plot(df['tipo_grafo'], df['busca_backtraking_75%'], lw=lw, color=cor1, label='Backtraking')
    ax5.plot(df['tipo_grafo'], df['busca_BTSL_75%'], lw=lw, color=cor2, label='BTSL')
    ax5.plot(df['tipo_grafo'], df['busca_BTDSATUR_75%'], lw=lw, color=cor3, label='BTDSATUR')
    ax5.set_title('75% de Densidade de Arestas')

    ax6 = fig.add_subplot(gs[1, 2])
    ax6.plot(df['tipo_grafo'], df['busca_backtraking_average'] / df['busca_backtraking_average'], lw=lw, color=cor1, label='Backtraking')
    ax6.plot(df['tipo_grafo'], df['busca_BTSL_average'] / df['busca_backtraking_average'], lw=lw, color=cor2, label='BTSL')
    ax6.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'] / df['busca_backtraking_average'], lw=lw, color=cor3, label='BTDSATUR')
    ax6.set_title('Relação com backtracking')

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
    #     ax.plot(df['tipo_grafo'], df['busca_backtraking_average'], lw=1.0, color='r', label='Backtraking-Average', linestyle='--', alpha=0.6)
    #     ax.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL-Average', linestyle='-', alpha=0.5)
    #     ax.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=1.0, color='b', label='BTDSATUR-Average', linestyle='--', alpha=0.4)
        ax.legend()
        ax.set_ylabel('Tempo Médio\n de Execução', rotation=0, loc='top', labelpad=-50)
        ax.set_xlabel('Número de Vértices', loc='right')

    return fig

def grafico_tempo_BTDSATUR_BTSL(fig, df):
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.25)
    cor1 = "#DFA000"
    cor2 = "#2DB5C7"
    lw = 2.0

    ax7 = fig.add_subplot(gs[0, 0])
    ax7.plot(df['tipo_grafo'], df['busca_BTSL_10%'], lw=lw, color=cor1, label='BTSL')
    ax7.plot(df['tipo_grafo'], df['busca_BTDSATUR_10%'], lw=lw, color=cor2, label='BTDSATUR')
    ax7.set_title('10% de Densidade de Arestas')

    ax8 = fig.add_subplot(gs[0, 1])
    ax8.plot(df['tipo_grafo'], df['busca_BTSL_25%'], lw=lw, color=cor1, label='BTSL')
    ax8.plot(df['tipo_grafo'], df['busca_BTDSATUR_25%'], lw=lw, color=cor2, label='BTDSATUR')
    ax8.set_title('25% de Densidade de Arestas')

    ax9 = fig.add_subplot(gs[0, 2])
    ax9.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=lw, color=cor1, label='BTSL')
    ax9.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=lw, color=cor2, label='BTDSATUR')
    ax9.set_title('Média Geral')

    ax10 = fig.add_subplot(gs[1, 0])
    ax10.plot(df['tipo_grafo'], df['busca_BTSL_50%'], lw=lw, color=cor1, label='BTSL')
    ax10.plot(df['tipo_grafo'], df['busca_BTDSATUR_50%'], lw=lw, color=cor2, label='BTDSATUR')
    ax10.set_title('50% de Densidade de Arestas')

    ax11 = fig.add_subplot(gs[1, 1])
    ax11.plot(df['tipo_grafo'], df['busca_BTSL_75%'], lw=lw, color=cor1, label='BTSL')
    ax11.plot(df['tipo_grafo'], df['busca_BTDSATUR_75%'], lw=lw, color=cor2, label='BTDSATUR')
    ax11.set_title('75% de Densidade de Arestas')

    ax12 = fig.add_subplot(gs[1, 2])
    ax12.plot(df['tipo_grafo'], df['busca_BTSL_average'] / df['busca_BTSL_average'], lw=lw, color=cor1, label='BTSL')
    ax12.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'] / df['busca_BTSL_average'], lw=lw, color=cor2, label='BTDSATUR')
    ax12.set_title('Relação dos Algorítmos')

    for ax in [ax11, ax12, ax7, ax8, ax9, ax10]:
    #     ax.plot(df['tipo_grafo'], df['busca_backtraking_average'], lw=1.0, color='r', label='Backtraking-Average', linestyle='--', alpha=0.6)
    #     ax.plot(df['tipo_grafo'], df['busca_BTSL_average'], lw=1.0, color='g', label='BTSL-Average', linestyle='-', alpha=0.5)
    #     ax.plot(df['tipo_grafo'], df['busca_BTDSATUR_average'], lw=1.0, color='b', label='BTDSATUR-Average', linestyle='--', alpha=0.4)
        ax.legend()
        ax.set_ylabel('Tempo Médio\n de Execução', rotation=0, loc='top', labelpad=-50)
        ax.set_xlabel('Número de Vértices', loc='right')
    
    return fig

def grafico_num_cores(fig, df):
    gs = fig3.add_gridspec(2, 2, hspace=0.35, wspace=0.25)
    cor1 = "#DFA000"
    cor2 = "#2DB5C7"
    lw = 2.0

    ax13 = fig3.add_subplot(gs[0,0])
    ax13.plot(df['tipo_grafo'], df['busca_gulosa_seq_10%'] - df['busca_BTDSATUR_10%'], lw=lw, color=cor1, label='Smallest Last')
    ax13.plot(df['tipo_grafo'], df['busca_DSATUR_10%'] - df['busca_BTDSATUR_10%'], lw=lw, color=cor2, label='DSATUR')
    ax13.set_title("10% de Densidade de Arestas")

    ax14 = fig3.add_subplot(gs[0,1])
    ax14.plot(df['tipo_grafo'], df['busca_gulosa_seq_25%'] - df['busca_BTDSATUR_25%'], lw=lw, color=cor1, label='Smallest Last')
    ax14.plot(df['tipo_grafo'], df['busca_DSATUR_25%'] - df['busca_BTDSATUR_25%'], lw=lw, color=cor2, label='DSATUR')
    ax14.set_title('25% de Densidade de Arestas')

    ax15 = fig3.add_subplot(gs[1,0])
    ax15.plot(df['tipo_grafo'], df['busca_gulosa_seq_50%'] - df['busca_BTDSATUR_50%'], lw=lw, color=cor1, label='Smallest Last')
    ax15.plot(df['tipo_grafo'], df['busca_DSATUR_50%'] - df['busca_BTDSATUR_50%'], lw=lw, color=cor2, label='DSATUR')
    ax15.set_title("50% de Densidade de Arestas")

    ax16 = fig3.add_subplot(gs[1,1])
    ax16.plot(df['tipo_grafo'], df['busca_gulosa_seq_75%'] - df['busca_BTDSATUR_75%'], lw=lw, color=cor1, label='Smallest Last')
    ax16.plot(df['tipo_grafo'], df['busca_DSATUR_75%'] - df['busca_BTDSATUR_75%'], lw=lw, color=cor2, label='DSATUR')
    ax16.set_title("75% de Densidade de Arestas")

    for ax in [ax13, ax14, ax15, ax16]:
        ax.legend()
        # for spine in ax.spines.values():
        #     spine.set_visible(False)
        # ax.spines['bottom'].set_visible(True)
        # ax.spines['left'].set_visible(True)
        ax.set_ylabel('Número Médio de\n Cores Extras', rotation=0, loc='top', labelpad=-50)
        ax.set_xlabel('Número de Vértices', loc='right')

    return fig

if __name__ == '__main__':
    funcs = [alg.busca_backtraking, alg.busca_BTSL, alg.busca_BTDSATUR]
    # df = testa_velocidade_coloracoes(funcs, 1, 15, 100, filepath=Path('trabalho_a2_md\data\BT-geral.csv'))
    # df = testa_velocidade_coloracoes(funcs, 1, 15, 100)
    df = pd.read_csv(Path('trabalho_a2_md\data\BT-geral.csv'))

    fig1 = plt.figure(figsize=(16, 9))
    fig1 = graficos_tempo_geral(fig1, df)

    funcs.remove(alg.busca_backtraking)
    # filepath = Path('trabalho_a2_md\data\BTSL-BTDSATUR.csv')
    # df = testa_velocidade_coloracoes(funcs, 40, 100, 100, filepath=filepath)
    # df = testa_velocidade_coloracoes(funcs, 1, 30, 100)
    df = pd.read_csv(Path('trabalho_a2_md\data\BTSL-BTDSATUR.csv'))

    fig2 = plt.figure(figsize=(16, 9))
    fig2 = grafico_tempo_BTDSATUR_BTSL(fig2, df)

    funcs = [alg.busca_gulosa_seq, alg.busca_DSATUR, alg.busca_BTDSATUR]
    filepath = Path('trabalho_a2_md\data\precisao-geral.csv')
    # df = testa_precisao_coloracoes(funcs, max_vertice=50, repeticoes=100, filepath=filepath)
    df = pd.read_csv(filepath)
    # df = testa_precisao_coloracoes(funcs, 1, 10)

    fig3 = plt.figure(figsize=(16,9))
    fig3 = grafico_num_cores(fig3, df)
        
    fig1.suptitle('Tempo Médio de Execução Dado o Número de Vértices e Densidade de Arestas')
    fig2.suptitle('Tempo Médio de Execução Dado o Número de Vértices e Densidade de Arestas')
    fig3.suptitle('Comparação do Número Médio de Cores Usado Pelos Algorítmos')

    root = Path(__file__).parent.parent
    fig1.savefig(root / 'figures' / 'COMPARACAO-BT-GERAL.png', dpi=200)
    fig2.savefig(root / 'figures' / 'COMPARACAO-BTSL-BTDSATUR.png', dpi=200)
    fig3.savefig(root / 'figures' / 'COMPARACAO-NUM-CROMATICO.png', dpi=200)

    # plt.show()
