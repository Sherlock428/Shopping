from database import Loja, Produto
import sistema_login, menu
import os

def cadastrar_produto(loja):
    try:
        if loja is None:
            print("Erro: Nenhuma loja encontrada. Faça o login primeiro.")
            return
        
        os.system('cls')
        nome = input('Digite O Nome do Produto: ')
        preco = float(input("Digite o Preço do Produto: "))
        unidade = int(input("Digite a quantidade de unidades: "))
        
        produto_existente = Produto.get_or_none(Produto.Nome == nome, loja=loja)

        if produto_existente:
            print(f"Produto {nome}, já existe na loja")
            return
        else:
            produto = Produto.create(Nome=nome, Preco=preco, Unidade=unidade, loja=loja)
            print(f'{nome} foi adicionado na loja {loja.Nome}')
            print(loja)

        input("[Enter] -> Retornar ao menu").capitalize()
    except (ValueError, TypeError):
        print("ERROR: Digite um Valor Válido")

def remover_produto(loja):
    try:

        produtos = Produto.select().where(Produto.loja == loja)
        print(f"""
{'=' * 30}\n
{'Remover Produto'.center(30).upper()}
{'=' * 30}""")
        ver_produto(loja)
        print("[0] Retornar ao menu")

        n = int(input("Selecione uma opção: "))

        if n == 0:
            return
        
        if 1 <= n <= len(produtos):
            produto_remover = produtos[n - 1]
            produto_remover.delete_instance()
            print(f'{produto_remover.Nome} Foi Removido com Sucesso')
            input("[Enter] -> Retornar ao menu")
        else:
            print("ERRO: Ao tentar remover Produto")
    except (ValueError, TypeError):
        print("ERROR: Digite um valor Válido")
    
    except Exception as e:
        print("ERROR: Não foi possível remover o produto")
        input('[Enter] -> Retornar ao menu')
def ver_produto(loja):
    try:
        produto = Produto.select().where(Produto.loja == loja)
        
        if not produto:
            print(f"""
{'=' * 30}
{'Nenhum Produto Cadastrado'.center().upper()}
{'=' * 30}
""")

            for i, p in enumerate(produto, start=1):
                print(f"""
{'=' * 30}
ID: \t[{i}] 
Nome: \t{p.Nome}
Preço: \t{p.Preco}
Unidade: \t{p.Unidade}""",
                      )

        print('=' * 30)
    except (ValueError, TypeError):
        print("ERROR: Digite um valor válido")

def atualizar_produto(loja):
    try:
        print(f"""
{'=' * 30}
{'Atualizar Produtos'.center(30).upper()}
{'=' * 30}""")
        
        ver_produto(loja)
        produtos = Produto.select().where(Produto.loja == loja)
        print("[0] Retornar ao Menu")

        n = int(input('Selecione uma opção: '))

        if n == 0:
            return
        if 1 <= n <= len(produtos):
            produto_atualizar = produtos[n - 1] 
           
            novo_nome = input("Digite o novo nome do Produto: ")
            novo_preco = float(input("Novo Preço: "))
            nova_unidade = int(input("Nova quantidade de unidade: "))

            produto_atualizar.Nome = novo_nome
            produto_atualizar.Preco = novo_preco
            produto_atualizar.Unidade = nova_unidade
            produto_atualizar.save()
    except (ValueError, TypeError):
        print("ERROR: Digite um valor válido")            

def bonus(loja):
    try:

        print(f"""
{'=' * 30}\n
{'Bonus'.center(30).upper()}
{'=' * 30}\n
[1] Mensagem 
[2] Desconto
""")
        op = int(input("Selecione"))

        if op == 1:
            titulo = input("Digite um Título: ")
            loja.Bonus_tipo = "Titulo"
            loja.Bonus_valor = titulo
            loja.save()
            input('[Enter] -> Retornar ao menu')

        elif op == 2:
            porcentagem = int(input("Selecione a Porcentagem do desconto: "))    
            loja.Bonus_tipo = "Desconto"
            loja.Bonus_valor = str(porcentagem)
            loja.save()
                
    except (ValueError, TypeError):
        print("ERROR: Digite Valor Válido")

def dados_loja(loja):

    print(f"""
{'=' * 30}
{f'{loja.Nome}'.upper().center(30)}
{'=' * 30}
{f'Faturamento: R${loja.Faturamento}'}
{'=' *30}
          
[1] Nome
[2] CNPJ
[3] Senha
[4] Apagar Loja

[0] Sair
""")
    try: 
        editar = int(input("O que você deseja Editar: "))

        if editar == 1:
            print("Você está Editando Nome da Loja")
            
            novo_nome = input("Digite o novo nome da loja: ")
            print(f"Nome Alterado para {novo_nome}")
            loja.Nome = novo_nome
            loja.save()
            input("[Enter] -> Retornar Menu")
            return
        elif editar == 2:
            print("Editando CNPJ: ")
            novo_cnpj = input("Digite o Novo CNPJ: ")
            loja.Cnpj = novo_cnpj
            loja.save()
            input("[Enter] -> Retornar Menu")
            return
        elif editar == 3:
            print("Editando Senha")
            nova_senha = input("Digite uma nova senha: ")

            confirmar = input("Confirme sua Senha: ")

            while nova_senha != confirmar:
                print("As senhas não coecidem: ")
                nova_senha = input("Digite uma Nova Senha: ")
                confirmar = input("Confirme a senha: ")

                loja.Senha = nova_senha
                loja.save()
                input("[0] -> Retornar ao menu")
                return
        

            
        
    except (ValueError, TypeError, Exception) as e:
        print(f"ERROR: {e}")

def produtos(loja):

    if loja is None:
        return   # Retorna a lista de lojas sem modificação


    while True:
        os.system('cls')
        print(f"""
{'=' * 30}
{f'{loja.Nome}'.upper().center(30)}
{'=' * 30}

[1] Cadastrar Produto
[2] Remover Produto
[3] Ver Produto
[4] Atualizar Produto
[5] Dados da Loja
[6] Bonus
[7] Deletar Loja

[0] Sair
    """)
        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                cadastrar_produto(loja)
            elif opcao == 2:
                remover_produto(loja)
            elif opcao == 3:
                ver_produto(loja) 
                enter = input("[Enter] -> Retornar ao menu: ")
            elif opcao == 4:
                atualizar_produto(loja)
            elif opcao == 5:
               dados_loja(loja)
            elif opcao == 6:
                bonus(loja)
            elif opcao == 7:
                print(f"Deseja Realmente Apagar a Loja {loja.Nome}?"
                      "\n[0] -> Retornar ao menu")
                
                enter = input("[Enter] -> Confirmar")

                if enter == "0":
                    return
                
                loja.delete_instance()
                break
            else:
                break  # Sair do loop e retornar a lista de lojas atualizada

        except ValueError:
            print("Erro: Opção inválida. Tente novamente.")

    
    
# lojas = sistema_login.lojas_logadas()
# a = sistema_login.cadastrar_loja(lojas)
# loja = sistema_login.login_loja(lojas)
# cadastrar_produto(loja)
# def promocao(loja):
#     try:

#         if "Produtos" not in loja or not loja["Produtos"]:
#             print("Nenhum Produto Cadastrado")
#         for i, produto in enumerate(loja["Produtos"], start=1):
#             print(f"[{i}] {produto["Nome"]}")

#         n = int(input("Selecione uma opção"))

#         if 1 <= n <= len(loja["Produtos"]):
#             porcentagem = int(input("Digite a porcentagem a ser aplicada em compras acima de 100 reais"))
#             diminuir = (loja["Produtos"][n-1]["Preco"] * porcentagem) / 100
#             loja["Produtos"][n - 1]["Preco"] = diminuir

#     except (TypeError, ValueError):
#         print("ERROR: Digite um valor válido")
