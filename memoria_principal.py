import math
from utils import gerar_palavra_aleatoria, kb_para_bytes


class MemoriaPrincipal:
    def __init__(self):
        self.tamanho_endereco = 0
        self.quantidade_palavras_por_bloco = 0
        self.quantidade_total_palavras = 0
        self.quantidade_total_blocos = 0
        self.tamanho_bloco = 0
        # Dicionário para armazenar os dados dos blocos da memória principal
        self.dados_bloco = {}

    def set_quantidade_total_palavras(self, tamanho_mp_kb):
        self.quantidade_total_palavras = int(kb_para_bytes(tamanho_mp_kb) / 4)
        return self

    def set_quantidades_palavras_por_bloco(self, qtde_palavras_bloco):
        self.quantidade_palavras_por_bloco = qtde_palavras_bloco
        return self

    def set_tamanho_endereco(self):
        self.tamanho_endereco = int(math.log2(self.quantidade_total_palavras))
        return self

    def set_quantidade_total_blocos(self):
        self.quantidade_total_blocos = int(
            self.quantidade_total_palavras / self.quantidade_palavras_por_bloco)
        # Inicializa os dados de cada bloco na memória principal
        for i in range(self.quantidade_total_blocos):
            # Cada bloco terá `self.quantidade_palavras_por_bloco` palavras aleatórias de 4 bits cada
            self.dados_bloco[i] = [gerar_palavra_aleatoria(
                4) for j in range(self.quantidade_palavras_por_bloco)]

        return self
        # Calcula o tamanho do bloco em bytes

    def set_tamanho_bloco(self):
        self.tamanho_bloco = int(self.quantidade_palavras_por_bloco * 4)
        return self

    def __str__(self) -> str:
        return (
            f'Informações da Memoria Principal:\n'
            f'Quantidade total de palavras / linhas na MP: {self.quantidade_total_palavras}\n'
            f'Quantidade de palavras por bloco: {self.quantidade_palavras_por_bloco}\n'
            f'Quantidade total de blocos na MP: {self.quantidade_total_blocos}\n'
            f'Tamanho do bloco da MP: {self.tamanho_bloco} bytes\n'
            f'Tamanho do Endereço da MP: {self.tamanho_endereco}\n'
        )
