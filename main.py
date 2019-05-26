# -*- coding: utf-8 -*-

import statistics
import math
import os
import view
from time import sleep 
from functools import reduce


DECIMAL_SIGNIFICANCE = 2


def leave():
    exit()


def round_decimal(n, decimals=DECIMAL_SIGNIFICANCE):
    if n > 0:
        return round_up(n, decimals=decimals)
    else:
        return round_down(n, decimals=decimals)


def round_up(n, decimals=2):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=2):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def quantiles(dist, *, n=4, method='exclusive'):
    if hasattr(dist, 'inv_cdf'):
        return [dist.inv_cdf(i / n) for i in range(1, n)]
    data = sorted(dist)
    ld = len(data)
    if method == 'exclusive':
        m = ld + 1
        result = []
        for i in range(1, n):
            j = i * m // n                              
            j = 1 if j < 1 else ld-1 if j > ld-1 else j 
            delta = i*m - j*n                           
            interpolated = (data[j-1] * (n - delta) + data[j] * delta) / n
            result.append(interpolated)
        return result


def read_file(filename, separator):
    global DECIMAL_SIGNIFICANCE

    with open(filename, 'r+') as f:
        file_string = f.read()
    file_lines = file_string.split('\n')
    col_names = file_lines[0].split(separator)
    col_matrix = [[float(_x) for _x in x.split(separator)] for x in file_lines[1:-1]]
    col_1 = [x[0] for x in col_matrix]
    col_2 = [x[1] for x in col_matrix]

    num_str = file_lines[1].split(separator)[0]
    if num_str.find('.'):
        decimal_str = num_str.split('.')[1]
        if len(decimal_str.replace('0', '')) == 0:
            DECIMAL_SIGNIFICANCE = 0
        else:
            DECIMAL_SIGNIFICANCE = len(decimal_str)
    else:
        DECIMAL_SIGNIFICANCE = 0

    return col_names, col_matrix, col_1, col_2


def frequency_table(col_names, col_1, col_2):
    def get_faixas(col, _min, d, n):
        faixas = []
        freq_acumulada = 0
        freq_relativa_acumulada = 0
        for i in range(1, n+1):
            min_faixa = round_decimal(_min + (i-1) * d)
            max_faixa = round_decimal(_min + i*d)
            pm = round_decimal(statistics.mean([min_faixa, max_faixa]))
            
            if i == n:
                itens_faixa = [x for x in col if min_faixa <= x <= max_faixa]
                freq = len(itens_faixa)
                freq_relativa = round(1 - freq_relativa_acumulada, 2)
                freq_relativa_acumulada = 1
            else:
                itens_faixa = [x for x in col if min_faixa <= x < max_faixa]
                freq = len(itens_faixa)
                freq_relativa = round(freq / len(col), 2)
                freq_relativa_acumulada += freq_relativa
            
            freq_acumulada += freq
            
            faixas.append({
                'min': min_faixa, 
                'max': max_faixa, 
                'pm': pm, 
                'freq': freq, 
                'freq_acum': freq_acumulada,
                'freq_rel': freq_relativa,
                'freq_rel_acum': freq_relativa_acumulada,
                'itens': itens_faixa
                })

        return faixas
            
    col_len = len(col_1)
    n_faixas = math.ceil(math.log2(col_len))

    min_1 = min(col_1)
    min_2 = min(col_2)

    A_1 = max(col_1) - min_1
    A_2 = max(col_2) - min_2

    d_1 = round_decimal(A_1 / n_faixas)
    d_2 = round_decimal(A_2 / n_faixas)

    faixas_1 = get_faixas(col_1, min_1, d_1, n_faixas)
    faixas_2 = get_faixas(col_2, min_2, d_2, n_faixas)

    view.print_freq_table(faixas_1, col_names[0])
    view.print_freq_table(faixas_2, col_names[1])

    return faixas_1, faixas_2

def grouped_stats(table):
    total_freq = table[-1]['freq_acum']

    def moda(table, total_freq):
        max_freq_index = 0 
        max_freq = 0
        for i in range(len(table)):
            if table[i]['freq'] > max_freq:
                max_freq = table[i]['freq']
                max_freq_index = i

        if max_freq_index == 0 or max_freq_index + 1 >= len(table):
            return '* Nao existe uma moda para esse conjunto de intervalos'

        lmin = table[max_freq_index]['min']
        d = table[max_freq_index]['max'] - table[max_freq_index]['min']
        fa = table[max_freq_index-1]['freq']
        fd = table[max_freq_index+1]['freq']

        return round(lmin + d * (fa / (fa + fd)), 3)
        
    def media(table, total_freq):
        return round(sum([x['pm'] * x['freq'] for x in table]) / total_freq, 3)

    def desvio_padrao(table, total_freq, _media):
        return round(math.sqrt(sum([(x['pm'] - _media) ** 2 for x in table]) / total_freq), 3)
    
    return moda(table, total_freq), media(table, total_freq), desvio_padrao(table, total_freq, media(table, total_freq))


def get_outliers(col):
    qs = quantiles(col)
    q1 = qs[0]
    q3 = qs[2]
    I = q3 - q1
    linf = q1 - 1.5*I
    lsup = q3 + 1.5*I

    outliers_inf = []
    outliers_sup = []

    for item in col:
        if item < linf:
            outliers_inf.append(item)
        elif item > lsup:
            outliers_sup.append(item)

    return outliers_inf, outliers_sup


def pearson_correlation(x, y):
    xmean = statistics.mean(x)
    ymean = statistics.mean(y)

    numerator = 0
    for i in range(len(x)):
        numerator += (x[i] - xmean) * (y[i] - ymean)

    denominator = math.sqrt(sum([(_x - xmean) ** 2 for _x in x])) * math.sqrt(sum([(_y - ymean) ** 2 for _y in y]))

    return numerator / denominator


def ols(x, y):
    xmean = statistics.mean(x)
    ymean = statistics.mean(y)

    numerator = 0
    for i in range(len(x)):
        numerator += (x[i] - xmean) * (y[i] - ymean)

    denominator = sum([(_x - xmean) ** 2 for _x in x])

    a = numerator / denominator
    b = ymean - a*xmean
    return a, b


while True:

    #########
    # INPUT #
    #########

    view.welcome()
    filename = view.get_file_read('Por favor insira o nome do arquivo de texto contendo os dados (com a extensao): ')

    if filename.strip() == '':
        view.error('Nome de arquivo vazio')

    if not os.path.isfile(filename):
        col1_name = view.get_file_creation('Insira o nome da primeira coluna: ')
        col2_name = view.get_file_creation('Insira o nome da segunda coluna: ')
        print()
        sep = view.get_file_creation(('Insira o(s) caractere(s) separador(es) desejado (ex: virgula, '
                                      'ponto e virgula, dois pontos, etc): '))
        print()
        col_1 = [float(x) for x in view.get_file_creation(('Insira os valores numericos da coluna "' + col1_name + '", '
                                                        'separados pelo(s) caractere(s) escolhido(s): ' )).split(sep)]
        col_2 = [float(x) for x in view.get_file_creation(('Insira os valores numericos da coluna "' + col2_name + '", '
                                                        'separados pelo(s) caractere(s) escolhido(s): ' )).split(sep)]
        print()
        if(len(col_1) != len(col_2)):
            view.error('As duas colunas devem ter o mesmo comprimento')
        else:
            with open(filename, 'w+') as f:
                f.write(col1_name + sep + col2_name + '\n')
                for i in range(len(col_1)):
                    f.write(str(col_1[i]) + sep + str(col_2[i]) + '\n')

            view.success_message('Arquivo criado com sucesso!')

    try:
        sep
    except NameError:
        sep = view.get_file_read(('Insira o(s) caractere(s) separador(es) usados na criacao do arquivo'
                                '(ex: virgula, ponto e virgula, dois pontos, etc): '))

    col_names, col_matrix, col_1, col_2 = read_file(filename, sep)

    view.print_file(col_matrix, col_names)

    ########################
    # TABELA DE FREQUENCIA #
    ########################

    faixas_1, faixas_2 = frequency_table(col_names, col_1, col_2)

    ##############################
    # MODA, MEDIA, DESVIO PADRAO #
    ##############################

    gmoda1, gmedia1, gstdev1 = grouped_stats(faixas_1)
    view.print_stats(col_1, gmedia1, gmoda1, gstdev1, col_names[0])

    gmoda2, gmedia2, gstdev2 = grouped_stats(faixas_2)
    view.print_stats(col_2, gmedia1, gmoda2, gstdev2, col_names[1])

    ############
    # OUTLIERS #
    ############

    outliers_inf_1, outliers_sup_1 = get_outliers(col_1)
    outliers_inf_2, outliers_sup_2 = get_outliers(col_2)

    view.print_outliers(outliers_inf_1, outliers_sup_1, col_names[0])
    view.print_outliers(outliers_inf_2, outliers_sup_2, col_names[1])

    #################
    # PEARSON E OLS #
    #################

    pc = pearson_correlation(col_1, col_2)
    a, b = ols(col_1, col_2)

    view.print_advanced_stats(pc, a, b)

    if 'quit' in view.get_end().lower():
        break

