import math
from utils import dividir_endereco, kb_para_bytes


class MemoriaCache:
    # Inicializa os atributos da memória cache
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

    # Configura o tamanho total da memória cache em bytes
    def set_tamanho_bytes(self, tamanho_bytes):
        self.tamanho_bytes = int(kb_para_bytes(tamanho_bytes))
        return self

    # Configura o tamanho das linhas (ou blocos) da memória cache
    def set_tamanho_linhas(self, tamanho_bloco_MP):
        self.tamanho_linhas = int(tamanho_bloco_MP)
        return self

    # Calcula o número total de linhas na memória cache com base no tamanho total e tamanho das linhas
    def set_total_linhas(self):
        self.total_linhas = int(self.tamanho_bytes / self.tamanho_linhas)
        return self

    # Configura o número de linhas por conjunto na memória cache
    def set_num_linhas_conjunto(self, num_linhas_conjunto):
        self.num_linhas_conjunto = int(num_linhas_conjunto)
        return self

     # Calcula o número total de conjuntos na memória cache com base no número de linhas por conjunto
    def set_num_conjuntos(self):
        self.num_conjuntos = int(self.total_linhas / self.num_linhas_conjunto)
        for i in range(self.num_conjuntos):
            # Inicializa cada conjunto com linhas vazias
            self.conjuntos[i] = {
                'Linhas': [{'Tag': None, 'Dados': None, 'Frequencia': 0}
                           for _ in range(self.num_linhas_conjunto)]
            }
        return self

    # Configura o valor de W com base na quantidade de palavras por bloco
    def set_w(self, quantidade_palavras_bloco):
        self.w = int(math.log2(quantidade_palavras_bloco))
        return self

    # Configura o valor de S com base na quantidade total de blocos na memória principal
    def set_s(self, quantidade_total_blocos_MP):
        self.s = int(math.log2(quantidade_total_blocos_MP))
        return self

    # Configura o valor de D com base no número de conjuntos
    def set_d(self):
        self.d = int(math.log2(self.num_conjuntos))
        return self

    # Configura o tamanho da TAG com base nos valores de S e D
    def set_tamanho_tag(self):
        self.tag = int(self.s - self.d)
        return self

    # Adiciona um endereço à memória cache e aplica a política de substituição LFU se necessário
    def adicionar_endereco(self, endereco: str, memoria_principal):
        self.endereco = endereco

        tag_bits, d_bits, w_bits = dividir_endereco(
            endereco, self.tag, self.d, self.w)
        conjunto_index = int(d_bits, 2)
        tag_str = tag_bits

        try:
            # Verifica se houve acerto (hit)
            for linha in self.conjuntos[conjunto_index]['Linhas']:
                if linha['Tag'] == tag_str and linha['Dados'] is not None:
                    linha['Frequencia'] += 1
                    self.acertos += 1
                    self.imprimir_conjunto_anterior_e_posterior(
                        conjunto_index, self.conjuntos[conjunto_index]['Linhas'].index(linha))
                    return conjunto_index

            # Se não houve acerto (miss)
            self.falhas += 1

            # Simula a busca na memória principal
            bloco_index = int(endereco[:self.s], 2)
            bloco = memoria_principal.dados_bloco[bloco_index]

            # Encontra a primeira linha vazia no conjunto e adiciona o bloco
            for i, linha in enumerate(self.conjuntos[conjunto_index]['Linhas']):
                if linha['Dados'] is None:
                    linha['Tag'] = tag_str
                    linha['Dados'] = bloco
                    linha['Frequencia'] = 1
                    self.imprimir_conjunto_anterior_e_posterior(conjunto_index, i)
                    return conjunto_index

            # Se não há linhas vazias, aplica política de substituição (LFU)
            min_freq = float('inf')
            linha_substituida = None
            linha_substituida_index = -1
            for i, linha in enumerate(self.conjuntos[conjunto_index]['Linhas']):
                if linha['Frequencia'] < min_freq:
                    min_freq = linha['Frequencia']
                    linha_substituida = linha
                    linha_substituida_index = i

            print(
                f"Linha substituída: Tag={linha_substituida['Tag']}, Dados={linha_substituida['Dados']}")

            # Substitui a linha menos frequentemente utilizada
            linha_substituida['Tag'] = tag_str
            linha_substituida['Dados'] = bloco
            linha_substituida['Frequencia'] = 1
            self.total_linhas_substituidas += 1

            self.imprimir_conjunto_anterior_e_posterior(
                conjunto_index, linha_substituida_index)
            return conjunto_index  # Retorna o índice do conjunto acessado

        except KeyError:
            print(f"\nErro: O conjunto {conjunto_index} não existe na cache. Verifique o endereço fornecido.")
            return None
        except IndexError:
            print(f"\nErro: Índice fora do intervalo no conjunto {conjunto_index}.")
            return None


    # Imprime o conjunto anterior, o conjunto atual com a linha acessada e suas duas linhas vizinhas existentes no conjunto, e o conjunto posterior ao conjunto atual
    def imprimir_conjunto_anterior_e_posterior(self, conjunto_index, linha_index):
        try:
            conjuntos_keys = list(self.conjuntos.keys())
            index_atual = conjuntos_keys.index(conjunto_index)

            if index_atual == 0:
                conjunto_anterior = conjuntos_keys[-1]
                conjunto_posterior = conjuntos_keys[index_atual + 1]
            elif index_atual == len(conjuntos_keys) - 1:
                conjunto_anterior = conjuntos_keys[index_atual - 1]
                conjunto_posterior = conjuntos_keys[0]
            else:
                conjunto_anterior = conjuntos_keys[index_atual - 1]
                conjunto_posterior = conjuntos_keys[index_atual + 1]

            print(f"\nConjunto anterior ao conjunto {conjunto_index}:\n")
            self.imprimir_conjunto(conjunto_anterior)

            print(
                f"\nConjunto atual {conjunto_index} (incluindo linha atual e vizinhas):\n")
            self.imprimir_linha_atual_e_vizinhas(conjunto_index, linha_index)

            print(f"\nConjunto posterior ao conjunto {conjunto_index}:\n")
            self.imprimir_conjunto(conjunto_posterior)
            print("-" * 100)

        except IndexError:
            print(f"\nErro: Índice de conjunto {conjunto_index} fora do intervalo ao tentar acessar conjunto anterior ou posterior.")
        except KeyError:
            print(f"\nErro: Conjunto {conjunto_index} não encontrado na cache.")

    # Imprime as linhas de um conjunto específico da cache
    def imprimir_conjunto(self, conjunto_index):
        conjunto = self.conjuntos[conjunto_index]
        print(f"Conjunto {conjunto_index}:")
        for i, linha in enumerate(conjunto['Linhas']):
            dados_str = ' '.join(linha['Dados']) if linha['Dados'] else 'vazia'
            print(
                f"Linha {i + 1}: {dados_str}, Tag: {linha['Tag'] if linha['Tag'] else 'vazia'}, Frequencia: {linha['Frequencia']}")


    # Imprime a linha atual de um conjunto específico da cache, juntamente com suas linhas vizinhas
    def imprimir_linha_atual_e_vizinhas(self, conjunto_index, linha_index):
        try:
            conjunto = self.conjuntos[conjunto_index]
            print(f"Conjunto {conjunto_index}:")

            # Define o intervalo de linhas a serem impressas
            num_linhas = len(conjunto['Linhas'])

            # Calcula os índices das linhas vizinhas
            inicio = max(0, linha_index - 2)
            fim = min(num_linhas, linha_index + 3)

            # Imprime as linhas anteriores à linha atual
            for i in range(inicio, linha_index):
                linha = conjunto['Linhas'][i]
                dados_str = ' '.join(linha['Dados']) if linha['Dados'] else 'vazia'
                print(
                    f"Linha {i + 1}: {dados_str}, Tag: {linha['Tag'] if linha['Tag'] else 'vazia'}, Frequencia: {linha['Frequencia']}")

            # Imprime a linha atual
            linha_atual = conjunto['Linhas'][linha_index]
            dados_str = ' '.join(
                linha_atual['Dados']) if linha_atual['Dados'] else 'vazia'
            print(
                f"--> Linha {linha_index + 1}: {dados_str}, Tag: {linha_atual['Tag'] if linha_atual['Tag'] else 'vazia'}, Frequencia: {linha_atual['Frequencia']}")

            # Imprime as linhas posteriores à linha atual
            for i in range(linha_index + 1, fim):
                linha = conjunto['Linhas'][i]
                dados_str = ' '.join(linha['Dados']) if linha['Dados'] else 'vazia'
                print(
                    f"Linha {i + 1}: {dados_str}, Tag: {linha['Tag'] if linha['Tag'] else 'vazia'}, Frequencia: {linha['Frequencia']}")

        except IndexError:
            print(f"\nErro: Índice de linha {linha_index} fora do intervalo no conjunto {conjunto_index}.")
        except KeyError:
            print(f"\nErro: Conjunto {conjunto_index} não encontrado na cache.")

    # Retorna o estado atual da cache como um dicionário de conjuntos e suas linhas
    def obter_estado_cache(self):
        estado_cache = {}
        for conjunto_index, conjunto_info in self.conjuntos.items():
            estado_cache[f'Conjunto {conjunto_index}'] = conjunto_info['Linhas']
        return estado_cache

    # Retorna uma string com as informações dos bits do endereço armazenados na cache
    def informacoes_bits_endereco(self):
        return (f'\nInformações do endereço:\n\n'
                f'Valor de W: {self.w}\n'
                f'Valor de S: {self.s}\n'
                f'Valor de D: {self.d}\n'
                f'Tamanho da TAG: {self.tag}\n')

    # Retorna uma string com todas as informações da memória cache formatadas
    def __str__(self):
        return (
            f'Informações da Mémoria Cache:\n\n'
            f'Tamanho da cache em bytes: {self.tamanho_bytes}\n'
            f'Total de linhas da cache: {self.total_linhas}\n'
            f'Tamanho das linhas da cache: {self.tamanho_linhas} bytes\n'
            f'Número de linhas por conjunto da cache: {self.num_linhas_conjunto}\n'
            f'Número de conjuntos da cache: {self.num_conjuntos}\n'
            f'Número de acertos: {self.acertos}\n'
            f'Número de falhas: {self.falhas}\n'
            f'Total de linhas substituidas devido ao LFU: {self.total_linhas_substituidas}\n'
        )
