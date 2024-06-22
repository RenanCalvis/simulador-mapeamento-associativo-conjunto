import math
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
        self.total_linhas_substituidas = 0

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
            # Inicializa cada conjunto com linhas vazias
            self.conjuntos[i] = {
                'Linhas': [{'Tag': None, 'Dados': None, 'Frequencia': 0}
                           for _ in range(self.num_linhas_conjunto)]
            }
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

        # Verifica se houve acerto (hit)
        for linha in self.conjuntos[conjunto_index]['Linhas']:
            if linha['Tag'] == tag_str and linha['Dados'] is not None:
                linha['Frequencia'] += 1
                self.acertos += 1
                return conjunto_index

        # Se não houve acerto (miss)
        self.falhas += 1

        # Simula a busca na memória principal
        bloco_index = int(endereco[:self.s], 2)
        bloco = memoria_principal.dados_bloco[bloco_index]

        # Encontra a primeira linha vazia no conjunto e adiciona o bloco
        for linha in self.conjuntos[conjunto_index]['Linhas']:
            if linha['Dados'] is None:
                linha['Tag'] = tag_str
                linha['Dados'] = bloco
                linha['Frequencia'] = 1
                return conjunto_index

        # Se não há linhas vazias, aplica política de substituição (LFU)
        min_freq = float('inf')
        linha_substituida = None
        for linha in self.conjuntos[conjunto_index]['Linhas']:
            if linha['Frequencia'] < min_freq:
                min_freq = linha['Frequencia']
                linha_substituida = linha

        print(
            f"Linha substituída: Tag={linha_substituida['Tag']}, Dados={linha_substituida['Dados']}")

        # Substitui a linha menos frequentemente utilizada
        linha_substituida['Tag'] = tag_str
        linha_substituida['Dados'] = bloco
        linha_substituida['Frequencia'] = 1
        self.total_linhas_substituidas += 1

        return conjunto_index  # Retorna o índice do conjunto acessado

    def imprimir_conjunto(self, conjunto_index):
        tag_bits, d_bits, w_bits = dividir_endereco(
            self.endereco, self.tag, self.d, self.w)
        print(f"Tag: {tag_bits}, D: {d_bits}, W: {w_bits}")
        print(f"Conjunto {conjunto_index}:")
        for i, entry in enumerate(self.conjuntos[conjunto_index]['Linhas']):
            dados_str = ' '.join(entry['Dados']) if entry['Dados'] else 'vazia'
            print(
                f"Linha {i + 1}: {dados_str}, Frequencia: {entry['Frequencia']}")

    def obter_estado_cache(self):
        estado_cache = {}
        for conjunto_index, conjunto_info in self.conjuntos.items():
            estado_cache[f'Conjunto {conjunto_index}'] = conjunto_info['Linhas']
        return estado_cache

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
            f'Total de linhas substituidas devido ao LFU: {self.total_linhas_substituidas}\n'
        )
