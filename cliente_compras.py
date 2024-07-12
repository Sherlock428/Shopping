import sistema_login, menu, os
from database import Cliente, Loja, Produto, Bonus, Cliente_produtos


def deposistar(cliente):
    try:
        credito = float(input("Quanto deseja depositar em sua conta: R$"))
        cliente.Credito += credito
        cliente.save()
        print(f"O Valor de R${credito} foi Depositado em sua conta, Você possui R${cliente.Credito}")

        input("[Enter] -> Retornar ao Menu")
    except (ValueError, TypeError):
        print("ERROR, Digite um Valor Válido")


def comprar(cliente):
    try:
        lojas = Loja.select()

        print(f"""
{'=' * 30}
{'Lojas do Shopping'.center(30).upper()}
{'=' * 30}
""")
        if not lojas.exists():
            print("Nenhuma Loja Encontrada: ")
            input('[Enter] -> Retornar ao menu')
            return
        
        for i, loja in enumerate(lojas, start=1):
            print(f"[{i}] {loja.Nome}")

        print("[0] -> Retornar ao Menu")
        n = int(input("Selecione uma loja para ver os produtos: "))
        
        if n == 0:
            return
        
        
        if 1 <= n <= len(lojas):
            loja_selecionada = lojas[n - 1]
            produtos = Produto.select().where(Produto.loja == loja_selecionada)
            print(f"\nAcessando Produtos da Loja {loja_selecionada.Nome}")


            if not produtos:
                print("Nenhum Produto Encontrado")
            
            for i, produto in enumerate(produtos, start=1):
                print(f"""
ID: [{i}] 
Nome: {produto.Nome}
Preço: {produto.Preco}
Unidades Disponiveis: {produto.Unidade}""")
            
            print("\n[0] Retornar ao Menu")
            compra = int(input("\nEscolha o Produto que deseja comprar: "))

            if compra == 0:
                return 

            if compra < 1 or compra > len(produtos):
                print("Produto Invalido\n")
                input("[Enter] -> Retornar Menu")
                return
            
            produto_selecionado = produtos[compra - 1]
            qtd_unidades = int(input("Quantas Unidades: "))

            if qtd_unidades > produto_selecionado.Unidade:
                print("Não tem Unidade Suficiente para realizar sua compra")

            if produto_selecionado.Unidade == 0:
                print("Nenhuma Unidade Disponível: ")
                if produto_selecionado.Unidade <= 0:
                    produto_selecionado.Unidade = 0
                    input("")
                    return
                    
            valor_final = produto_selecionado.Preco * qtd_unidades
            print(f"\nVocê está Comprando o produto {produto_selecionado.Nome}, {qtd_unidades} Unidades no valor de R${valor_final:.2f}")
            print("\n[0] Retornar ao menu")

            confirmar = input("\n[Enter] -> Confirmar ")
            if confirmar == "0":
                return
            
            
            if valor_final >= 100:
                # cliente.bonus = loja_selecionada.Bonus

                if loja_selecionada.Bonus_tipo == "Desconto":
                    desconto = (valor_final * float(loja_selecionada.Bonus_valor)) / 100
                    valor_final -= desconto

                elif loja_selecionada.Bonus_tipo == "Titulo":
                    bonus_existente = Bonus.select().where(
                        (Bonus.cliente == cliente) & 
                        (Bonus.loja == loja_selecionada) & 
                        (Bonus.Tipo == loja_selecionada.Bonus_tipo) & 
                        (Bonus.Valor == loja_selecionada.Bonus_valor))
                    
                    if bonus_existente.exists():
                        print("Você já possui o Bonus dessa loja")
                        input("[Enter] -> Continuar")
                    else:
                        bonus =  Bonus.create(cliente=cliente, loja=loja_selecionada, Tipo=loja_selecionada.Bonus_tipo, Valor=loja_selecionada.Bonus_valor)
                        print(f"Você Recebeu o Título {loja_selecionada.Bonus_valor}.")
                        input('[Enter] -> Continuar')

            if cliente.Credito >= valor_final:
                cliente.Credito -= valor_final
                produto_selecionado.Unidade -= qtd_unidades

                if loja_selecionada.Faturamento is None:
                    loja_selecionada.Faturamento = 0.0
                produto_cliente_existente = Cliente_produtos.get_or_none((Cliente_produtos.cliente == cliente) &
                                                                            (Cliente_produtos.produto == produto_selecionado))
                
                if produto_cliente_existente:
                    # produto_qtd = Cliente_produtos.select().where(Cliente_produtos.cliente == cliente, Cliente_produtos.produto == produto_selecionado)
                    nova_qtd = qtd_unidades + produto_cliente_existente.quantidade

                    print(f"Você Comprou {qtd_unidades} unidades do produto {produto_selecionado.Nome}\n"
                         f"Quantidade anterior: {produto_cliente_existente.quantidade}\n"
                         f"Nova Quantidade: {nova_qtd}\n")
                    produto_cliente_existente.quantidade = nova_qtd
                    produto_cliente_existente.save()
                    input("[Enter] -> Continuar")
                
                else:  
                    cliente_produto = Cliente_produtos.create(cliente=cliente, produto=produto_selecionado, quantidade=qtd_unidades)

                loja_selecionada.Faturamento += valor_final
                produto_selecionado.save()
                loja_selecionada.save()
                cliente.save()


            print(f"\nVocê comprou {qtd_unidades} do Produto {produto_selecionado['Nome']} no valor de R${valor_final:.2f} ")
            
            input("\n[Enter] -> Retornar ao Menu")

    except (ValueError, TypeError):
        print('ERROR: Digite um valor válido')

def editar_perfil(cliente):
    try:
        print(f"""
{'='  *30}
{'Editar'.upper().center(30)}
{'=' * 30}

[1] Nome
[2] Email
[3] Senha
[4] Bonus       """)
        
        opcao = int(input("Opção: "))

        if opcao == 1:
            cliente.Nome = input("Digite o Seu Nome: ")
            cliente.save()
            print(f"Nome Alterado para {cliente.Nome}")
        elif opcao == 2:
            cliente.Email = input("Digite seu novo Email: ")
            print(f"Email Alterado para {cliente.Email}")
            cliente.save()

        elif opcao == 3:
            cliente.Senha = input("Digite sua nova Senha: ")
            
            while len(cliente.Senha) < 6:
                cliente.Senha = input("Digite uma senha com pelo menos 6 caracteres: ")
            
            confirmar_senha = input("Confirme sua senha: ")
            
            if cliente.Senha == confirmar_senha:
                print("Senha Alterada Com Sucesso")
                cliente.save()            
        
        elif opcao == 4:
            os.system('cls')
            print(f"""
{'=' * 30}
{f'Bonus'.upper().center()}
{'=' * 30}

[1] Adicionar Bonus
[2] Remover Bonus
                  """)
            escolha = int(input("Selecione: "))
            bonus = Bonus.select().where(Bonus.cliente == cliente)

            if escolha == 1:
                if not bonus.exists():
                    print("Você não tem nenhum Bonus Disponivel")
                    input("[Enter] -> Retornar Menu")
                    return
                for i, b in enumerate(bonus, start=1):
                    print(f"[{i}] {b.Valor}")

                n = int(input("Selecione o Titulo: "))

                titulo_selecionado = bonus[n - 1].Valor
                if 1 <= n <= len(bonus):
                    print(f"Deseja Equipar o Titulo: {titulo_selecionado}")
                    print("\n[0] Retornar ao Menu")

                    confirme = input("\n[Enter] -> confirmar")

                    cliente.Nome = f'[{titulo_selecionado}] {cliente.Nome}'
                    cliente.save()
                    if confirme == "0":
                        return
                    
                    print(f"Titulo {titulo_selecionado} Equipado com Sucesso ")
                    input("[Enter] -> Retornar ao Menu")

            elif escolha == 2:
                if not bonus.exists():
                    print("Você não tem nenhum Bonus para ser Removido")
                    input("[Enter] -> Retornar ao menu")
                    return
                
                for i, b in enumerate(bonus, start=1):
                    print(f"[{i}] {b.Valor}")

                n = int(input("selecione o Titulo a ser Removido: "))

                if 1 <= n <= len(bonus):
                    titulo_selecionado = bonus[n - 1]
                    titulo_selecionado.delete_instance()
                    print(f"{titulo_selecionado.Valor} foi Removido com Sucesso")
                    input("[Enter] -> Enter Retornar ao Menu")
                    return 
                

    except (ValueError, TypeError):
        print("ERROR, Digite um valor válido")

def meus_pedidos(cliente):
    
    clientes_produtos = Cliente_produtos.select().where(Cliente_produtos.cliente == cliente)

    if not clientes_produtos.exists():
        print("Nenhum Produto Encontrado")
        input("[Enter] -> Retornar ao Menu")
        return
    print(f"""
{'=' * 30}
{'Meus Pedidos'.center(30).upper()}
{'=' * 30}
""")
    for i, p in enumerate(clientes_produtos, start=1):
        print(f"""
{'=' * 30}               
ID: \t[{i}] 
Nome: \t{p.produto.Nome}
Quantidade: \t{p.quantidade}
""")
        print('=' * 30)

    input("[Enter] -> Retornar ao Menu: ")
def clientes_(cliente):

    if cliente is None:
        print("Usuario Invalido: ")
        os.system('cls')
        input('[Enter] -> Retornar ao menu')
        return
    
    while True:
        os.system('cls')
        print(f"""
{'=' * 30}
{f'Cliente {cliente.Nome}'.upper().center(30)}
{'=' * 30}
{f"Seu SALDO: R${cliente.Credito:.2f}".upper()}
{'=' * 30}

[1] Depositar Crédito
[2] Ver Lojas
[3] Editar Perfil
[4] Meus Produtos
[5] Deletar Conta

[0] Sair
""")
        try:
            opcao = int(input("Selecione: "))

            if opcao == 1:
                deposistar(cliente)
            elif opcao == 2:
                comprar(cliente)
            elif opcao == 3:
                editar_perfil(cliente)
            elif opcao == 4:
                meus_pedidos(cliente)
            elif opcao == 5:
                print(f"Deseja Realmente Apagar a Conta?\n"
                     f"[0] -> Retornar ao Menu")
               
                enter = input("[Enter] -> Continuar")

                if enter == '0':
                    return
                
                cliente.delete_instance()
                break

            else:
                break
        
        except (ValueError, TypeError):
            print("ERROR: Digite um valor válido")
