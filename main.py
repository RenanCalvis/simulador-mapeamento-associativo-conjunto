import math

from memoria_cache import MemoriaCache
from memoria_principal import MemoriaPrincipal
from utils import ler_entrada
import os


def main():
    pasta_entradas = 'entradas_para_leitura'

    if not os.path.exists(pasta_entradas):
        print(
            f"A pasta {pasta_entradas} não existe. Por favor, crie a pasta e adicione arquivos de entrada.")
        return

    while True:
        nome_arquivo = input(
            f"Digite o nome do arquivo na pasta '{pasta_entradas}' ou 'q' para sair: ")

        if nome_arquivo.lower() == 'q':
            break

        caminho_arquivo = os.path.join(pasta_entradas, nome_arquivo)

        if not os.path.isfile(caminho_arquivo):
            print("Arquivo não encontrado. Tente novamente.")
            continue

        tamanho_MP, qtde_palavras_bloco_MP, tamanho_cache, num_linhas_conjunto = ler_entrada(
            caminho_arquivo)

        mp = MemoriaPrincipal()
        mp.set_quantidade_total_palavras(tamanho_MP)\
          .set_quantidade_total_blocos(qtde_palavras_bloco_MP)\
          .set_tamanho_endereco()\
          .set_tamanho_bloco(qtde_palavras_bloco_MP)

        mc = MemoriaCache()
        mc.set_tamanho_bytes(tamanho_cache)\
          .set_tamanho_linhas(mp.tamanho_bloco)\
          .set_total_linhas()\
          .set_num_linhas_conjunto(num_linhas_conjunto)\
          .set_num_conjuntos()\
          .set_w(qtde_palavras_bloco_MP)\
          .set_s(mp.quantidade_total_blocos)\
          .set_d()\
          .set_tamanho_tag()

        print(str(mp))
        print(str(mc))


if __name__ == "__main__":
    main()
