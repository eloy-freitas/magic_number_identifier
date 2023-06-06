import sys
import json as js
import pandas as pd

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

def find_file_sign(header, path):
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

def search_headers(dataset, path, header=None):
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
    
    if header:
        qtd_files = find_file_sign(header, path)
        dataset.loc[dataset['Hex'] == header, ['Found']] = qtd_files

        print(dataset.loc[dataset['Hex'] == header].to_string(index=False))
    else:
        for row in dataset.itertuples():
            hex_str = row[3]
            
            qtd_files = find_file_sign(hex_str, path)

            dataset.loc[dataset['Hex'] == hex_str, ['Found']] = qtd_files

            if qtd_files > 0:
                print(dataset.loc[dataset['Hex'] == hex_str].to_string(index=False))


def run(path, file_sigs_path, header=None):
    dataset = read_dataset(file_sigs_path)
    search_headers(dataset, path, header)


if __name__ == '__main__':
    sig = None
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            sig = sys.argv[2]
        except:
            pass
        
    run(path, 'test.json', header=sig)
    