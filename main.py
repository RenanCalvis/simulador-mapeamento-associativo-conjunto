import os
from memoria_cache import MemoriaCache
from memoria_principal import MemoriaPrincipal
from utils import ler_entrada

def ler_arquivo(pasta_entradas):
    nome_arquivo = input(
        f"Digite o nome do arquivo na pasta '{pasta_entradas}' ou 'q' para sair: ")
    if nome_arquivo.lower() == 'q':
        return None

    caminho_arquivo = os.path.join(pasta_entradas, nome_arquivo)

    if not os.path.isfile(caminho_arquivo):
        print("Arquivo não encontrado. Tente novamente.")
        return None

    return caminho_arquivo

def configurar_memorias(caminho_arquivo):
    tamanho_MP, qtde_palavras_bloco_MP, tamanho_cache, num_linhas_conjunto = ler_entrada(
        caminho_arquivo)

    mp = MemoriaPrincipal()
    mp.set_quantidade_total_palavras(tamanho_MP)\
      .set_quantidades_palavras_por_bloco(qtde_palavras_bloco_MP)\
      .set_quantidade_total_blocos()\
      .set_tamanho_endereco()\
      .set_tamanho_bloco()

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

    return mp, mc

def mostrar_menu():
    print("\nMenu:")
    print("1. Ler nome de arquivo com informações necessárias")
    print("2. Apresentar informações da memória cache e memória principal")
    print("3. Informar um endereço de MP válido para acesso à MP")
    print("4. Sair")

def main():
    pasta_entradas = 'entradas_para_leitura'

    if not os.path.exists(pasta_entradas):
        print(
            f"A pasta {pasta_entradas} não existe. Por favor, crie a pasta e adicione arquivos de entrada.")
        return

    mp, mc = None, None

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            caminho_arquivo = ler_arquivo(pasta_entradas)
            if caminho_arquivo:
                mp, mc = configurar_memorias(caminho_arquivo)
                print("Memórias configuradas com sucesso.")
            else:
                print("Nenhum arquivo foi lido.")

        elif opcao == '2':
            if mp and mc:
                print(str(mp))
                print(str(mc))
            else:
                print(
                    "As memórias não foram configuradas. Por favor, leia um arquivo primeiro.")

        elif opcao == '3':
            if mp and mc:
                while True:
                    endereco = input(
                        f"Informe um endereço de MP válido, contendo {mp.tamanho_endereco} bits: ")

                    if len(endereco) != mp.tamanho_endereco:
                        print(
                            f"Endereço inválido! Deve conter exatamente {mp.tamanho_endereco} bits.")
                        continue  # Volta ao início do loop para solicitar outro endereço

                    conjunto_index = mc.adicionar_endereco(endereco,mp)
                    print(f"Endereço {endereco} adicionado à memória cache.")
                    print(f"Conjunto acessado: {conjunto_index}")
                    mc.imprimir_conjunto(conjunto_index, mp)

                    break  # Sai do loop após adicionar o endereço válido
            else:
                print(
                    "As memórias não foram configuradas. Por favor, leia um arquivo primeiro.")

        elif opcao == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
