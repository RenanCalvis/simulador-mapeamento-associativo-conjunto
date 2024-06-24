import os
from memoria_cache import MemoriaCache
from memoria_principal import MemoriaPrincipal
from utils import ler_enderecos, ler_entrada

# Solicita o nome de um arquivo na pasta especificada e retorna o caminho completo do arquivo


def ler_arquivo(pasta_entradas):
    nome_arquivo = input(
        f"Digite o nome do arquivo na pasta '{pasta_entradas}' ou 'q' para sair: ")
    print("-" * 100)
    if nome_arquivo.lower() == 'q':  # Verifica se o usuário deseja sair
        return None

    # Constrói o caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_entradas, nome_arquivo)

    if not os.path.isfile(caminho_arquivo):  # Verifica se o arquivo existe
        print("\nArquivo não encontrado. Tente novamente.")
        return None

    return caminho_arquivo  # Retorna o caminho do arquivo se encontrado

    # Lê os parâmetros de configuração das memórias a partir de um arquivo de entrada


def configurar_memorias(caminho_arquivo):
    tamanho_MP, qtde_palavras_bloco_MP, tamanho_cache, num_linhas_conjunto = ler_entrada(
        caminho_arquivo)

    # Configura a memória principal (MP)
    mp = MemoriaPrincipal()
    mp.set_quantidade_total_palavras(tamanho_MP)\
      .set_quantidades_palavras_por_bloco(qtde_palavras_bloco_MP)\
      .set_quantidade_total_blocos()\
      .set_tamanho_endereco()\
      .set_tamanho_bloco()

    # Configura a memória cache (MC)
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

    return mp, mc  # Retorna as instâncias configuradas de MP e MC

    # Exibe o menu de opções para o usuário


def mostrar_menu():
    print("-" * 100)
    print("Menu:\n")
    print("1. Ler nome de arquivo com informações necessárias")
    print("2. Apresentar informações da Memória Cache, Memória Principal e os valores para os bits endereçáveis")
    print("3. Informar um endereço em bits válido para realizar o mapeamento")
    print("4. Ler lista de endereços de um arquivo")
    print("5. Visualizar os dados contidos na Memória Principal")
    print("6. Sair")
    print("-" * 100)


def main():
    # Define a pasta onde os arquivos de entrada estão localizados
    pasta_entradas = 'entradas_para_leitura'

    # Verifica se a pasta de entradas existe
    if not os.path.exists(pasta_entradas):
        print(
            f"\nA pasta {pasta_entradas} não existe. Por favor, crie a pasta e adicione arquivos de entrada.")
        return

    mp, mc = None, None  # Inicializa as variáveis para as memórias principal e cache

    while True:
        mostrar_menu()  # Exibe o menu de opções
        opcao = input("Escolha uma opção: ")
        print("-" * 100)

        # Opção para ler o nome do arquivo de configuração
        if opcao == '1':
            caminho_arquivo = ler_arquivo(pasta_entradas)
            if caminho_arquivo:
                mp, mc = configurar_memorias(caminho_arquivo)
                print("\nMemórias configuradas com sucesso.\n")
            else:
                print("\nNenhum arquivo foi lido.\n")

            # Opção para apresentar informações da memória cache e principal
        elif opcao == '2':
            if mp and mc:
                print(str(mc))
                print(str(mp))
                print(str(mc.informacoes_bits_endereco()))
            else:
                print(
                    "\nAs memórias não foram configuradas. Por favor, leia um arquivo primeiro.")

            # Opção para informar um endereço válido e realizar o mapeamento
        elif opcao == '3':
            if mp and mc:
                while True:
                    endereco = input(
                        f"\nInforme um endereço de MP válido, contendo {mp.tamanho_endereco} bits ou 'q' para sair: ")
                    print("-" * 100)

                    if endereco.lower() == 'q':
                        print("\nNenhum endereço foi lido.\n")
                        break

                    # Verifica se o endereço tem o tamanho correto
                    if len(endereco) != mp.tamanho_endereco:
                        print(
                            f"\nEndereço inválido! Deve conter exatamente {mp.tamanho_endereco} bits.")
                        continue

                    print(f"\nEndereço {endereco} adicionado à memória cache.")
                    mc.adicionar_endereco(endereco, mp)
                    break
            else:
                print(
                    "\nAs memórias não foram configuradas. Por favor, leia um arquivo primeiro.")

            # Opção para ler uma lista de endereços de um arquivo
        elif opcao == '4':
            if mp and mc:
                caminho_arquivo = ler_arquivo(pasta_entradas)
                if caminho_arquivo:
                    enderecos = ler_enderecos(caminho_arquivo)
                    for endereco in enderecos:
                        # Verifica se cada endereço tem o tamanho correto
                        if len(endereco) != mp.tamanho_endereco:
                            print(
                                f"\nEndereço {endereco} inválido! Deve conter exatamente {mp.tamanho_endereco} bits.")
                            continue
                        print(
                            f"\nEndereço {endereco} adicionado à memória cache.")

                        mc.adicionar_endereco(endereco, mp)
                else:
                    print("\nNenhum arquivo de endereços foi lido.\n")
            else:
                print(
                    "\nAs memórias não foram configuradas. Por favor, leia um arquivo primeiro.")

            # Opção para visualizar os dados da memória principal
        elif opcao == '5':
            if mp:
                print("\nDados dos Blocos da Memória Principal:\n")
                for bloco, dados in mp.dados_bloco.items():
                    print(f"Bloco {bloco}: {dados}")
            else:
                print(
                    "\nA memória principal não foi configurada. Por favor, leia um arquivo primeiro.")

            # Opção para sair do programa
        elif opcao == '6':
            print("\nSaindo...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()  # Executa a função principal / digite em seu terminal: python main.py  para inicializar o programa
