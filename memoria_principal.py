import math
from utils import kb_para_bytes


class MemoriaPrincipal:
    def __init__(self):
        self.tamanho_endereco = 0
        self.quantidade_total_palavras = 0
        self.quantidade_total_blocos = 0
        self.tamanho_bloco = 0
        self.armazenamento = {}

    def set_quantidade_total_palavras(self, tamanho_mp_kb):
        self.quantidade_total_palavras = int(kb_para_bytes(tamanho_mp_kb) / 4)
        return self

    # Tamanho do endereço / tamanho da palavra em bytes (4)
    def set_tamanho_endereco(self):
        self.tamanho_endereco = int(math.log2(self.quantidade_total_palavras))
        return self

    def set_quantidade_total_blocos(self, qtde_palavras_bloco):
        self.quantidade_total_blocos = int(
            self.quantidade_total_palavras / qtde_palavras_bloco)
        return self

    # Quantidade total de palavras * tamanho de cada palavra em bytes
    def set_tamanho_bloco(self, qtde_palavras_bloco):
        self.tamanho_bloco = int(qtde_palavras_bloco * 4)
        return self

    def __str__(self) -> str:
        return (
            f'Quantidade total de palavras / linhas na MP: {self.quantidade_total_palavras}\n'
            f'Quantidade total de blocos na MP: {self.quantidade_total_blocos}\n'
            f'Tamanho do bloco da MP: {self.tamanho_bloco} bytes\n'
            f'Tamanho do Endereço da MP: {self.tamanho_endereco}\n'
        )
