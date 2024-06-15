import math
from utils import kb_para_bytes

class MemoriaPrincipal:
    def __init__(self):
        self.tamanho = 0
        self.quantidade_palavras = 0
        self.unidades_endenrecaveis = 0
        self.tamanho_endereco_conjunto = 0
        self.tamanho_tag = 0
        self.armazenamento = {}

    def set_numero_de_conjuntos(self, d):  # d
        self.tamanho_endereco_conjunto = int(d)
        return self

    def set_tamanho(self, tamanho):  # Tamanho do endereço
        self.tamanho = int(math.log2(kb_para_bytes(tamanho)))
        return self

    # Calcula o tamanho de w (número de bits para identificar a palavra dentro do bloco)
    def set_quantidade_palavras_bloco(self, qtde_palavras):  # valor de w
        self.quantidade_palavras = int(math.log2(qtde_palavras))
        return self

    def set_numero_unidades_enderecaveis_memoria(self):  # valor de s
        self.unidades_endenrecaveis = int(
            self.tamanho - self.quantidade_palavras)
        return self

    def set_tamanho_tag(self):
        self.tamanho_tag = int(
            self.unidades_endenrecaveis - self.tamanho_endereco_conjunto)
        return self

    def __str__(self) -> str:
        return (f'Tamanho do Endereço da MP: {self.tamanho}\nValor de W: {self.quantidade_palavras}\nValor de S: {self.unidades_endenrecaveis}\nValor de D: {self.tamanho_endereco_conjunto}\nTamanho da TAG: {self.tamanho_tag}')
