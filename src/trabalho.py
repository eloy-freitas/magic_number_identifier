import json as js
import pandas as pd

def treat_dataset(dataset):
    str_to_hex = lambda x: hex(int(f"0x{x.replace(' ', '')}", 16))

    dataset['HeaderFormatted'] = dataset['Header'].map(str_to_hex)
    
    dataset['FilesFound'] = 0

    return dataset
    

def read_dataset(path):
    with open(path, 'r') as file:
        data = js.load(file)
    dataset = pd.DataFrame(data)

    return dataset

def find_file_sign(header, path):
    count = 0
    with open(path, 'rb') as file:
        while content := file.read(8).hex():
            hex_string = hex(int(content, 16))
            if hex_string == header:
                count += 1
    
    return count


def run(file_path, file_sigs_path):
    tbl_sigs:pd.DataFrame = read_dataset(file_sigs_path)

    tbl_sigs = treat_dataset(tbl_sigs)

    for row in tbl_sigs.itertuples():
        hex_str = row[7]
        header = row[2]
        file_desc = row[1]
        qtd_files = find_file_sign(hex_str, file_path)
        
        print(f"File description: {file_desc}, Header: {header}, Files found:{qtd_files}")
        




if __name__ == '__main__':
    run('./imagem.img', 'file_sigs.json')