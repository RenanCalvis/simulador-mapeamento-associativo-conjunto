import math
from utils import gerar_palavra_aleatoria, kb_para_bytes

class MemoriaPrincipal:
    # Inicializa atributos da memória principal
    def __init__(self):
        self.tamanho_endereco = 0
        self.quantidade_palavras_por_bloco = 0
        self.quantidade_total_palavras = 0
        self.quantidade_total_blocos = 0
        self.tamanho_bloco = 0
        
        self.dados_bloco = {} # Dicionário para armazenar os dados dos blocos da memória principal

    # Define a quantidade total de palavras na memória principal com base no tamanho em KB
    # Como informado nas observações para o trabalho, assume que cada palavra tem 4 bytes
    def set_quantidade_total_palavras(self, tamanho_mp_kb):
        self.quantidade_total_palavras = int(kb_para_bytes(tamanho_mp_kb) / 4)
        return self

    # Define a quantidade de palavras por bloco
    def set_quantidades_palavras_por_bloco(self, qtde_palavras_bloco):
        self.quantidade_palavras_por_bloco = qtde_palavras_bloco
        return self

    # Calcula o tamanho do endereço em bits com base na quantidade total de palavras
    def set_tamanho_endereco(self):
        self.tamanho_endereco = int(math.log2(self.quantidade_total_palavras))
        return self

    # Calcula a quantidade total de blocos na memória principal
    def set_quantidade_total_blocos(self):
        self.quantidade_total_blocos = int(
            self.quantidade_total_palavras / self.quantidade_palavras_por_bloco)
        
    # Inicializa os dados de cada bloco na memória principal
        for i in range(self.quantidade_total_blocos):
            self.dados_bloco[i] = [gerar_palavra_aleatoria(4) for j in range(self.quantidade_palavras_por_bloco)]
        return self

    # Calcula o tamanho do bloco em bytes
    def set_tamanho_bloco(self):
        self.tamanho_bloco = int(self.quantidade_palavras_por_bloco * 4)
        return self

    # Retorna uma string com as informações da memória principal formatadas
    def __str__(self) -> str:
        return (
            f'Informações da Memoria Principal:\n\n'
            f'Quantidade total de palavras / linhas na MP: {self.quantidade_total_palavras}\n'
            f'Quantidade de palavras por bloco: {self.quantidade_palavras_por_bloco}\n'
            f'Quantidade total de blocos na MP: {self.quantidade_total_blocos}\n'
            f'Tamanho do bloco da MP: {self.tamanho_bloco} bytes\n'
            f'Tamanho do Endereço da MP: {self.tamanho_endereco}\n'
        )
