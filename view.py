# -*- coding: utf-8 -*-

import os
import statistics
from table import tabulate
from sys import exit


def clear(): 
    if os.name == 'nt': 
        os.system('cls')  
    else: 
        os.system('clear')


def hold():
    input('> Pressione ENTER para continuar... ')


def sepbar():
    print('*'*50)


def center(_str):
    print('{:^50}'.format(_str))


def bcenter(_str):
    print('*{:^48}*'.format(_str))


def bcentertitle(_str):
    sepbar()
    bcenter('')
    bcenter(_str)
    bcenter('')
    sepbar()
    print()


def error(message):
    sepbar()
    bcenter('ERRO')
    bcenter('')
    bcenter(message)
    sepbar()
    print()
    input('> Pressione ENTER para fechar o programa... ')
    clear()
    exit(0)


def header(mode=''):
    clear()
    sepbar()
    bcenter('TRABALHO DE PROBABILIDADE E ESTATISTICA I')
    bcenter('Feito por Leonardo Amorim')
    if mode != '':
        bcenter('')
        bcenter(mode)
    sepbar()
    print()


def welcome():
    header()
    hold()
    clear()


def get_file_read(_str):
    header(mode='Leitura do Arquivo')
    print('* O arquivo deve estar no mesmo diretorio do script')
    print()
    _ = input('> ' + _str)
    clear()
    return _


def get_file_creation(_str):
    header(mode='Criacao do Arquivo')
    print('* Esse arquivo ainda nao existe, cria-lo-emos agora!')
    print('* O arquivo tera 2 colunas com nomes de sua preferencia, com N itens numericos de comprimento.')
    print()
    _ = input('> ' + _str)
    clear()
    return _


def success_message(_str):
    header(mode='Sucesso!')
    bcentertitle(_str)
    hold()
    clear()


def print_file(col_matrix, col_names):
    header(mode='Exibindo dados do arquivo')
    print(tabulate(col_matrix, headers=col_names))
    print()
    hold()
    clear()


def print_freq_table(faixas, col_name):
    header(mode='Exibindo tabela de frequencia')
    bcentertitle('Tabela de frequencia de "{}"'.format(col_name))
    
    headers = ['Faixa ({})'.format(col_name), 'Ponto Medio', 'Frequencia', 'Frequencia Acumulada', 
    'Frequencia Relativa', 'Frequencia Relativa Acumulada']
    formatted_faixas = []
    for faixa in faixas:
        formatted_faixas.append([
            '{:.2f} |--- {:.2f}'.format(faixa['min'], faixa['max']),
            faixa['pm'],
            faixa['freq'],
            faixa['freq_acum'],
            faixa['freq_rel'],
            faixa['freq_rel_acum']
        ])
    
    print(tabulate(formatted_faixas, headers=headers))
    print()
    hold()
    clear()


def print_stats(col, mean, mode, stdev, col_name):
    header(mode='Dados estatisticos do conjunto {}'.format(col_name))

    bcentertitle('Usando todos os valores')
    try:
        print('* Moda = {:.3f}'.format(statistics.mode(col)))
    except:
        print('* Nao existe uma moda para esse conjunto')
    print('* Media = {:.3f}'.format(statistics.mean(col)))
    print('* Desvio Padrao = {:.3f}'.format(statistics.stdev(col)))
    print()

    bcentertitle('Usando valores agrupados')
    if type(mode) == type(1.50):
        print('* Moda = {:.3f}'.format(mode))
    else:
        print('* Nao existe uma moda para esse conjunto de intervalos')
    print('* Media = {:.3f}'.format(mean))
    print('* Desvio Padrao = {:.3f}'.format(stdev))
    print()

    hold()
    clear()


def print_outliers(outliers_inf, outliers_sup, col_name):
    header(mode='Exibindo outliers do conjunto {}'.format(col_name))

    bcentertitle('Outliers abaixo do limite inferior')
    if len(outliers_inf) > 0:
        print('* ', outliers_inf)
    else:
        print('* Nao existem outliers abaixo do limite inferior para esse conjunto')
    print()

    bcentertitle('Outliers acima do limite superior')
    if len(outliers_sup) > 0:
        print('* ', outliers_sup)
    else:
        print('* Nao existem outliers acima do limite superior para esse conjunto')
    print()
    
    hold()
    clear()


def print_advanced_stats(corr, a, b):
    header(mode='Exibindo estatisticas avancadas')

    sepbar()
    bcenter('Correlacao de Pearson = {:.5f}'.format(corr))
    bcenter('')
    bcenter('Coeficiente Angular (A) = {:.5f}'.format(a))
    bcenter('Peso/altura da reta (B) = {:.5f}'.format(b))
    bcenter('')
    bcenter('f(x) = {:.5f}x + {:.5f}'.format(a, b))
    sepbar()

    print()
    hold()
    

def get_end():
    header(mode='Fim')
    _ = input('> Para recomecar, pressione ENTER. Para sair, digite "q" e pressione ENTER... ')
    clear()
    return _
    