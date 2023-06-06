import sys
import json as js
import pandas as pd


def read_dataset(path):
    with open(path, 'r') as file:
        data = js.load(file)
    dataset = pd.DataFrame(data)

    return dataset

def find_file_sign(header, path):
    count = 0
    
    try:
        with open(path, 'rb') as file:
            while content := file.read(8).hex():
                hex_string = hex(int(content, 16))
                if hex_string == header:
                    count += 1
    except IOError as e:
        raise IOError(
            "Falha na leitura do arquivo"
            f"MENSAGEM: {e}"
        )
    
    return count

def search_headers(dataset, file_path, header=None):
    dataset['Found'] = 0
    
    if header:
        
        qtd_files = find_file_sign(header, file_path)
        dataset.loc[dataset['Hex'] == header, ['Found']] = qtd_files

        print(dataset.loc[dataset['Hex'] == header].to_string(index=False))
    else:
        for row in dataset.itertuples():
            hex_str = row[3]
            
            qtd_files = find_file_sign(hex_str, file_path)

            dataset.loc[dataset['Hex'] == hex_str, ['Found']] = qtd_files

            if qtd_files > 0:
                print(dataset.loc[dataset['Hex'] == hex_str].to_string(index=False))


def run(file_path, file_sigs_path, header=None):
    dataset = read_dataset(file_sigs_path)
    search_headers(dataset, file_path, header)


if __name__ == '__main__':
    sig = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            sig = sys.argv[2]
        except:
            pass
        
    run(file_path, 'test.json', header=sig)
    