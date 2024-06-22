import os
import random

def kb_para_bytes(dado):
    return dado * 1024


def ler_entrada(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        size_MP_kb = int(file.readline().strip())
        words_per_block = int(file.readline().strip())
        size_cache_kb = int(file.readline().strip())
        lines_per_set = int(file.readline().strip())
    return size_MP_kb, words_per_block, size_cache_kb, lines_per_set


def ler_enderecos(nome_arquivo):
    enderecos = []
    with open(nome_arquivo, 'r') as file:
        for linha in file:
            enderecos.append(linha.strip())
    return enderecos


def dividir_endereco(endereco: str, tag: int, d: int, w: int):
    tag_bits = endereco[:tag]
    d_bits = endereco[tag:tag + d]
    w_bits = endereco[tag + d: tag + d + w]

    return tag_bits, d_bits, w_bits



def gerar_palavra_aleatoria(tamanho):
    return ''.join(random.choice('01') for _ in range(tamanho))

