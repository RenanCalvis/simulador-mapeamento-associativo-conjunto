import math
from utils import kb_para_bytes


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

        self.armazenamento = {}

    def set_tamanho_bytes(self, tamanho_bytes):  # Tamanho da cache
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
        return self

    def set_w(self, quantidade_palavras_bloco):  # valor de w
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

    def __str__(self) -> str:
        return (
            f'Valor de W: {self.w}\n'
            f'Valor de S: {self.s}\n'
            f'Valor de D: {self.d}\n'
            f'Tamanho da TAG: {self.tag}\n'
            f'Tamanho da cache em bytes: {self.tamanho_bytes}\n'
            f'Total de linhas da cache: {self.total_linhas}\n'
            f'Tamanho das linhas da cache: {self.tamanho_linhas}\n'
            f'Número de linhas por conjunto da cache: {self.num_linhas_conjunto}\n'
            f'Número de conjuntos da cache: {self.num_conjuntos}\n'
        )
