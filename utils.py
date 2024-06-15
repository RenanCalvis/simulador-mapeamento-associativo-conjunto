import os


def kb_para_bytes(dado):
    return dado * 1024


def ler_entrada(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        size_MP_kb = int(file.readline().strip())
        words_per_block = int(file.readline().strip())
        size_cache_kb = int(file.readline().strip())
        lines_per_set = int(file.readline().strip())
    return size_MP_kb, words_per_block, size_cache_kb, lines_per_set

# def listar_arquivos_pasta(pasta):
#     return [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]