import math
import random
from utils import dividir_endereco, kb_para_bytes

class MemoriaCache:
    def __init__(self):
        self.tamanho_bytes = 0
        self.total_linhas = 0
        self.tamanho_linhas = 0
        self.num_linhas_conjunto = 0
        self.num_conjuntos = 0
        self.w = 0
        self.s = 0
        self.d = 0
        self.tag = 0
        self.endereco = ""

        self.conjuntos = {}  # Dicionário para armazenar os conjuntos da cache
        self.acertos = 0
        self.falhas = 0

    def set_tamanho_bytes(self, tamanho_bytes):
        self.tamanho_bytes = int(kb_para_bytes(tamanho_bytes))
        return self

    def set_tamanho_linhas(self, tamanho_bloco_MP):
        self.tamanho_linhas = int(tamanho_bloco_MP)
        return self

    def set_total_linhas(self):
        self.total_linhas = int(self.tamanho_bytes / self.tamanho_linhas)
        return self

    def set_num_linhas_conjunto(self, num_linhas_conjunto):
        self.num_linhas_conjunto = int(num_linhas_conjunto)
        return self

    def set_num_conjuntos(self):
        self.num_conjuntos = int(self.total_linhas / self.num_linhas_conjunto)
        for i in range(self.num_conjuntos):
            self.conjuntos[i] = []
        return self

    def set_w(self, quantidade_palavras_bloco):
        self.w = int(math.log2(quantidade_palavras_bloco))
        return self

    def set_s(self, quantidade_total_blocos_MP):
        self.s = int(math.log2(quantidade_total_blocos_MP))
        return self

    def set_d(self):
        self.d = int(math.log2(self.num_conjuntos))
        return self

    def set_tamanho_tag(self):
        self.tag = int(self.s - self.d)
        return self

    def adicionar_endereco(self, endereco: str, memoria_principal):
        self.endereco = endereco

        tag_bits, d_bits, w_bits = dividir_endereco(
            endereco, self.tag, self.d, self.w)
        conjunto_index = int(d_bits, 2)
        tag_str = tag_bits

        # Verifica se houve acerto (hit) ou falha (miss)
        if any(entry['tag'] == tag_str for entry in self.conjuntos[conjunto_index]):
            self.acertos += 1
        else:
            self.falhas += 1
            if len(self.conjuntos[conjunto_index]) >= self.num_linhas_conjunto:
                self.conjuntos[conjunto_index].pop(
                    0)  # Remove o bloco mais antigo
            # Simula a busca na memória principal e adiciona o bloco na cache
            # Escolhe o bloco baseado no endereço de entrada
            bloco_index = int(endereco[:self.s], 2)
            bloco = memoria_principal.dados_bloco[bloco_index]
            self.conjuntos[conjunto_index].append(
                {'tag': tag_str, 'bloco_index': bloco_index, 'bloco': bloco})

        return conjunto_index  # Retorna o índice do conjunto acessado

    def imprimir_conjunto(self, conjunto_index, memoria_principal):
        print(f"Conjunto {conjunto_index}:")
        for entry in self.conjuntos[conjunto_index]:
            d_bits = format(conjunto_index, '0' + str(self.d) + 'b')
            tag = entry['tag']
            bloco_index = entry['bloco_index']
            bloco = entry['bloco']
            print(f"D: {d_bits}, Tag: {tag}, Bloco Index: {bloco_index}, Dados: {bloco}")

    def __str__(self):
        return (
            f'Valor de W: {self.w}\n'
            f'Valor de S: {self.s}\n'
            f'Valor de D: {self.d}\n'
            f'Tamanho da TAG: {self.tag}\n'
            f'Tamanho da cache em bytes: {self.tamanho_bytes}\n'
            f'Total de linhas da cache: {self.total_linhas}\n'
            f'Tamanho das linhas da cache: {self.tamanho_linhas} bytes\n'
            f'Número de linhas por conjunto da cache: {self.num_linhas_conjunto}\n'
            f'Número de conjuntos da cache: {self.num_conjuntos}\n'
            f'Número de acertos: {self.acertos}\n'
            f'Número de falhas: {self.falhas}\n'
        )
