from database import conectar_banco, Loja, Cliente
import os

def formatar(cnpj):
    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:15]}'

def validar(email):
    dominio_permitido = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
    dominio = email.split('@')[-1]
    return dominio in dominio_permitido
def cadastrar_loja():

    try:
        print(f"""
{'=' * 30}
{'Cadastro de Loja'.center(30).upper()}
{'=' * 30}
""")
        nome = input("Digite o Nome da Loja: ")
        cnpj = input("Digite o CNPJ: ")
        while len(cnpj) < 14:
            print("CNPJ Deve Possuir 14 Dígitos")
            cnpj = input("Digite o CNPJ Válido: ")
        senha = input("Crie sua Senha: ")
        while len(senha) < 6:
            print("A Senha precisa ter no Mínimo 6 caracteres")
            senha = input("Digite uma Senha: ")

        confimar_senha = input("Confirme sua senha: ")
            


        while confimar_senha != senha:
            print("Senhas não coecidem: ")
            senha = input("Digite uma senha: ")
            confimar_senha = input("Confirme sua senha: ")

        if senha == confimar_senha:
            loja_existente = Loja.get_or_none((Loja.Nome == nome) & (Loja.Cnpj == cnpj))

            if loja_existente:
                print('=' * 30)
                print("\nLoja já existente")
                input("[Enter] -> Retornar ao menu")
            
            else:
                Loja.create(Nome=nome, Cnpj=cnpj, Senha=senha, Bonus_tipo=None, Bonus_valor=None)
                formatado_cnpj = formatar(cnpj)
                print(f"""
    {'=' * 30}
    {'Conta Criada'.upper()}
    {'=' * 30}

    Nome da loja: {nome}
    CNPJ: {formatado_cnpj}
                    """)
            input('[Enter] -> Retornar ao Menu')

    except (ValueError, TypeError):
        print("ERROR: Digite apenas valores válidos: ")
    
    

def login_loja():
    try:
        os.system('cls')
        print(f"""
{'=' * 30}
{'Login Loja'.center(30).upper()}
{'=' * 30}
""")
        cnpj = input("Digite seu CNPJ: ")
        senha = input("Digite sua Senha: ")

        loja = Loja.get(Loja.Cnpj == cnpj, Loja.Senha == senha)

        if loja:
            print(f"{Loja.Nome} Encontrada")
            return loja
        
        else:
            print("Dados não coecidem")
            return None
    
    except (ValueError, TypeError, Exception) as e:
        print(f"ERROR: Usuario não encontrado")
        input('[Enter] -> Retornar ao menu')

def cadastrar_cliente():
    try:
        print(f"""
{'=' * 30}
{'Cadastro de Cliente'.center(30).upper()}
{'=' * 30}
""")
        nome = input("Digite Seu Nome: ")
        email= input("Digite Seu Email: ").lower()
        while not validar(email):
            print("Digite um Email Válido: Aceitamos gmail, hotmail, yahoo, outlook")
            email = input("Digite seu email: ")
        senha = input("Digite Sua senha: ")
            
        while len(senha) < 6:        
            print("Senha Menor que 6 Caracteres: ")
            senha = input("Digite Sua Senha novamente: ")
            
        confirmar_senha = input("Confirme sua Senha: ")
        credito = float(input("Digite um Valor para Depositar em Sua Conta: R$"))
        while senha != confirmar_senha:
            print("As Senhas não Coecidim")
            senha = input("Digite Sua Senha: ")
            confirmar_senha = input("Confirme Sua Senha: ")
        
        if senha == confirmar_senha:
            Cliente.create(Nome=nome, Email=email, Senha=senha, Credito=credito)
            print(f"""
{'=' * 30}
{'Conta Criada'.upper()}
{'=' * 30}

Nome: {nome}
Email: {email}
                  """)
            print(f"Usuario: {nome} Foi Cadastrado com Sucesso")
            input("[Enter] -> Retornar ao menu")

    except (ValueError, TypeError):
        print("ERROR: Ao Realizar Cadastro")
    

    

def login_cliente():
    os.system('cls')
    try:
        print(f"""
{'=' * 30}
{'Login Cliente'.center(30).upper()}
{'=' * 30}
""")
        email = input("Digite Seu Email: ")
        senha = input("Digite Sua Senha: ")
    
        cliente = Cliente.get(Cliente.Email == email, Cliente.Senha == senha)

        if cliente:
            return cliente

        else:
            print("Dados não coecidem: ")
            return None

    except (ValueError, TypeError):
        print("ERROR: Digite Apeans Valores válidos")

