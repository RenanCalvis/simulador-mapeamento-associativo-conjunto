import math

class MemoriaCache:
    def __init__(self):
        self.tamanho_MC = 0
        self.tamanho_endereco_conjunto = 0
        self.quantidade_palavras_bloco = 0
        self.armazenamento = {}
        pass

    # Calcula o número de bits para identificar o conjunto na MP
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

    def set_numero_unidades_enderecaveis_memoria(self,):  # valor de s
        self.unidades_endenrecaveis = math.log2(
            self.tamanho) - self.quantidade_palavras


class MemoriaPrincipal:
    def __init__(self):
        self.tamanho = 0
        self.quantidade_palavras = 0
        self.unidades_endenrecaveis = 0
        self.tamanho_endereco_conjunto = 0
        self.tamanho_tag = 0
        self.armazenamento = {}
        pass

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

    def set_numero_unidades_enderecaveis_memoria(self,):  # valor de s
        self.unidades_endenrecaveis = int(
            self.tamanho - self.quantidade_palavras)
        return self

    def set_tamanho_tag(self):
        self.tamanho_tag = int(
            self.unidades_endenrecaveis - self.tamanho_endereco_conjunto)
        return self

    def __str__(self) -> str:
        return (f'Tamanho do Endereço da MP: {self.tamanho}\nValor de W: {self.quantidade_palavras}\nValor de S: {self.unidades_endenrecaveis}\nValor de D: {self.tamanho_endereco_conjunto}\nTamanho da TAG: {self.tamanho_tag}')


def kb_para_bytes(dado):
    return dado * 1024


def main():
    tamanho_MP = 256
    qtde_palavras_bloco_MP = 4
    tamanho_cache = 32
    num_linhas_conjunto = 4
    mc = MemoriaCache()
    mc.set_tamanho(tamanho_cache).set_quantidade_palavras_bloco(
        qtde_palavras_bloco_MP).set_numero_de_conjuntos(num_linhas_conjunto)
    mp = MemoriaPrincipal()
    mp.set_tamanho(tamanho_MP).set_quantidade_palavras_bloco(qtde_palavras_bloco_MP).set_numero_unidades_enderecaveis_memoria(
    ).set_numero_de_conjuntos(mc.tamanho_endereco_conjunto).set_tamanho_tag()
    print(str(mp))


if __name__ == "__main__":
    main()
