import sys
import json as js
import pandas as pd
import time

FILE_NOT_FOUND_ERROR_MESSAGE = """
    Falha na leitura do arquivo"
    "MENSAGEM: {}
"""


def read_dataset(path: str):
    """
    Faz a leitura de json com assinatura de arquivos conhecidas
    e retorna um dataset

    params:
        `path` - path do arquivo (`str`)
    
    return:
        dataset com assinatura de arquivos (`pandas.Dataframe`)

    """
    try:
        with open(path, 'r') as file:
            data = js.load(file)
    except IOError as e:
        raise IOError(
            FILE_NOT_FOUND_ERROR_MESSAGE.format(e)
        )
    dataset = pd.DataFrame(data)

    return dataset


def find_file_sign(header:str, path:str):
    """
    Percorre todos os bytes de um arquivo em busca de um assinatura

    params:
        `header` - string de um número heximadecimal (ex: 0x89504e470d0a1a0a)
        `path` - path do arquivo que está sendo lido
    
    return:
        quantidade de arquivos encontrados (`int`)
    """
    count = 0
    
    try:
        with open(path, 'rb') as file:
            while content := file.read(8).hex():
                hex_string = hex(int(content, 16))
                if hex_string == header:
                    count += 1
    except IOError as e:
        raise IOError(
            FILE_NOT_FOUND_ERROR_MESSAGE.format(e)
        )
    
    return count


def search_headers(dataset:pd.DataFrame, path:str):
    """
    Faz a busca por todos cabeçalhos de arquivos contidos no dataset 
    e retorna 

    params:
        `dataset`: dataset com assinatura de arquivos
        `path`: path do arquivo alvo
        `header`: a busca é feita em cima de uma assinatura específica em vex do dataset inteiro
    
    return:
        dataset de arquivos encontrados
        
    """
    dataset['Found'] = 0
    
    for row in dataset.itertuples():
        hex_str = row[3]
        
        qtd_files = find_file_sign(hex_str, path)

        dataset.loc[dataset['Hex'] == hex_str, ['Found']] = qtd_files

        if qtd_files > 0:
                print(dataset.loc[dataset['Hex'] == hex_str].to_string(index=False))


def filter_dataset(dataset:pd.DataFrame, headers:list[str]=None):
    """
    Filtra todos so cabeçalhos conhecidos no dataset
    params:
        `dataset`: dataset com assinatura de arquivos
        `headers`: lista de assinatura de arquivos
    return:
        dataset de assinatura filtrato
    """
    if headers:
        dataset = dataset.query(f"Hex in ({headers})")

    return dataset

def run(path:str, path_dataset:str, headers:list[str]=None):
    """
    Função principal do programa

    parmas:
        `path` - path do arquivo que vai ser analisado
        `path_dataset` - arquivo com dataset de assinaturas
        `headers` - lista de assinaturas para serem filtradas na busca
    """

    start = time.time()

    dataset = read_dataset(path_dataset)
    dataset = filter_dataset(dataset, headers)
    search_headers(dataset, path)
    
    end = time.time() - start
    print("Tempo de execução: {:.2f} s".format(end))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise RuntimeError(
            "Error: É necessário path de um arquivo para análise"
        ) 
    else:
        path = sys.argv[1]
        headers = sys.argv[2:]
        
        run(path, 'file_sigs.json', headers)
    