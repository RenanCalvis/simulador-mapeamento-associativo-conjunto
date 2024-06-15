import math

from memoria_cache import MemoriaCache
from memoria_principal import MemoriaPrincipal
from utils import ler_entrada
import os

def main():
    pasta_entradas = 'entradas_para_leitura'

    if not os.path.exists(pasta_entradas):
        print(f"A pasta {pasta_entradas} não existe. Por favor, crie a pasta e adicione arquivos de entrada.")
        return

    while True:
        nome_arquivo = input(f"Digite o nome do arquivo na pasta '{pasta_entradas}' ou 'q' para sair: ")

        if nome_arquivo.lower() == 'q':
            break

        caminho_arquivo = os.path.join(pasta_entradas, nome_arquivo)

        if not os.path.isfile(caminho_arquivo):
            print("Arquivo não encontrado. Tente novamente.")
            continue

        tamanho_MP, qtde_palavras_bloco_MP, tamanho_cache, num_linhas_conjunto = ler_entrada(caminho_arquivo)

        mc = MemoriaCache()
        mc.set_tamanho(tamanho_cache).set_quantidade_palavras_bloco(
            qtde_palavras_bloco_MP).set_numero_de_conjuntos(num_linhas_conjunto)

        mp = MemoriaPrincipal()
        mp.set_tamanho(tamanho_MP).set_quantidade_palavras_bloco(qtde_palavras_bloco_MP).set_numero_unidades_enderecaveis_memoria(
        ).set_numero_de_conjuntos(mc.tamanho_endereco_conjunto).set_tamanho_tag()

        print(str(mp))

if __name__ == "__main__":
    main()
