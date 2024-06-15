import math
from utils import kb_para_bytes

class MemoriaCache:
    def __init__(self):
        self.tamanho_MC = 0
        self.tamanho_endereco_conjunto = 0
        self.quantidade_palavras_bloco = 0
        self.armazenamento = {}

    def set_tamanho(self, tamanho):  # Tamanho do endereço
        self.tamanho = kb_para_bytes(tamanho)
        return self

    def set_quantidade_palavras_bloco(self, qtde_palavras):
        # quantidade de palavras por bloco x número de bytes de uma palavras de 32 bits
        self.quantidade_palavras_bloco = qtde_palavras * 4
        return self

    def set_numero_de_conjuntos(self, qtde_linhas):
        self.tamanho_endereco_conjunto = math.log2(
            self.tamanho / (self.quantidade_palavras_bloco * qtde_linhas))
        return self

    def set_numero_unidades_enderecaveis_memoria(self):  # valor de s
        self.unidades_endenrecaveis = math.log2(
            self.tamanho) - self.quantidade_palavras
