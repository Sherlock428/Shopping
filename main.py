from sistema_login import  login_loja,  login_cliente, cadastrar_cliente, cadastrar_loja
from produtos import  produtos
from cliente_compras import clientes_
from menu import menu_cliente, menu_cliente_c, menu_inicial, menu_lojista, menu_lojista_p
from database import conectar_banco
import os



def main():
    conectar_banco()
    
    while True:
        os.system('cls')
        print(menu_inicial)  # Usar a variável diretamente

        try:
            opcao = int(input("Selecione: "))
            os.system('cls')
        except ValueError:
            print("Opção inválida. Tente novamente.")
            continue
    
        if opcao == 1:
            print(menu_lojista)  # Usar a variável diretamente

            try:
                opcao = int(input("Selecione: "))
            except (ValueError, TypeError):
                print("Opção inválida. Tente novamente.")
                continue

            if opcao == 1:
                os.system('cls')
                loja = login_loja()
                if loja:
                    produtos(loja)
                
                      
            elif opcao == 2:
                os.system('cls')  
                cadastrar_loja()
                
            
        elif opcao == 2:
            print(menu_cliente)

            try:
                opcao = int(input("Selecione: "))
            except ValueError:
                print("Opção inválida. Tente novamente.")
                continue
            
            if opcao == 1:
                os.system('cls')
                cliente = login_cliente()
                if cliente:
                    clientes_(cliente)
                else:
                    print("ERROR: Cliente invalido")
                    input('[Enter] -> Retornar ao Menu')                

            elif opcao == 2:
                os.system('cls')
                cadastrar_cliente()
        
        elif opcao == 3:
            print("Obrigado por utilizar nosso Sistema: ")
            break

if __name__ == "__main__":
    main()