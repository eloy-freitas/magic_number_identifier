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
    columns = [
        "File description",
        "Header",
        "Found"
    ]

    result_set = pd.DataFrame(columns=columns)
    
    if header:
        dataset = dataset.query(f"Hex == '{header}'")
        qtd_files = find_file_sign(header, file_path)
        print(dataset)
        print(f"Found:{qtd_files}")

    else:
        for row in dataset.itertuples():
            file_desc = row[1]
            header = row[2]
            hex_str = row[3]
            
            qtd_files = find_file_sign(hex_str, file_path)

            result = {
                "File description": [file_desc],
                "Header": [header], 
                "Found": [qtd_files]
            }

            result = pd.DataFrame(result)

            if qtd_files > 0:
                print(result)

            result_set = pd.concat([result_set, result])


def run(file_path, file_sigs_path, header=None):
    dataset = read_dataset(file_sigs_path)
    
    search_headers(dataset, file_path, header)


if __name__ == '__main__':
    if len(sys.argv) > 0:
        sig = sys.argv[1]
    
    run('./imagem.img', 'test.json', header=sig)
    