from datetime import datetime

usuarios = []

menu_2 = """
    ================ MENU ================
    [1]Depositar
    [2]Sacar
    [3]Extrato
    [4]Nova conta
    [5]Listar contas
    [0]Sair
    => """

menu_3 = """Cliente não Cadastrado, deseja se cadastrar?
    [1]Sim
    [2]Não
    ==> """

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        data_deposito = datetime.now()
        extrato += f"Depósito: R$ {valor:.2f} {data_deposito.strftime("%d/%m/%Y %H:%M:%S")}\n"
        print(f"Depósito no valor de R$ {valor:.2f} concluído!")
    else:
        print("Operação não concluída, tente novamente")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Saldo Insuficiente.")

    elif excedeu_limite:
        print("Valor acima do limite permitido!")

    elif excedeu_saques:
        print("Máximo de saques já realizados.")

    elif valor > 0:
        saldo -= valor
        data_saque = datetime.now()
        extrato += f"Saque: R$ {valor:.2f} {data_saque.strftime("%d/%m/%Y %H:%M:%S")}\n"
        numero_saques += 1
        print(f"Saque no valor de R$ {valor:.2f} realizado")

    else:
        print("Operação não concluída, tente novamente")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        
    print("Usuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:{conta['agencia']}
            C/C:    {conta['numero_conta']}
            Titular:{conta['usuario']['nome']}
        """
        
        print(linha)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    contas = []

    while True:
        cpf = input("Digite o seu CPF (somente números): ")
        usuario = filtrar_usuario(cpf, usuarios)
        if not usuario:            
            opcao1 = int(input(menu_3))
            if opcao1 == 1:
                criar_usuario(usuarios)
              
            elif opcao1 == 2:
                print("Finalizado! Retornando ao menu anterior")
                
            else:
                print("Informação incorreta! Retornando ao menu anterior")
            

        else:
            while True:
                opcao = input(menu_2)

                if opcao == "1":
                    valor = float(input("Informe o valor do depósito: "))

                    saldo, extrato = depositar(saldo, valor, extrato)

                elif opcao == "2":
                    valor = float(input("Informe o valor do saque: "))

                    saldo, extrato = sacar(
                        saldo=saldo,
                        valor=valor,
                        extrato=extrato,
                        limite=limite,
                        numero_saques=numero_saques,
                        limite_saques=LIMITE_SAQUES,
                        )

                elif opcao == "3":
                    exibir_extrato(saldo, extrato=extrato)

                elif opcao == "4":
                    numero_conta = len(contas) + 1
                    conta = criar_conta(AGENCIA, numero_conta, usuarios)

                    if conta:
                        contas.append(conta)

                elif opcao == "5":
                    listar_contas(contas)

                elif opcao == "0":
                    print("Obrigado por utilizar nosso sistema!")
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")
    

main()   



    