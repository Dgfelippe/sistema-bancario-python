"""
╔══════════════════════════════════════════╗
║         🏦  BANCO DGBANK  🏦               ║
║    Sistema Bancário - Desafio Python     ║
╚══════════════════════════════════════════╝
"""

# ─────────────────────────────────────────
#  Funções visuais
# ─────────────────────────────────────────

def cabecalho():
    print("\n" + "═" * 44)
    print("║" + "   🏦  BANCO DGBANK — Bem-vindo(a)!   ".center(42) + "║")
    print("═" * 44)

def separador(titulo=""):
    if titulo:
        print(f"\n{'─' * 10} {titulo} {'─' * 10}")
    else:
        print("─" * 44)

def exibir_menu():
    """Mostra o menu de opções ao usuário."""
    separador()
    print("  [d] 💰  Depositar")
    print("  [s] 💸  Sacar")
    print("  [e] 📄  Ver Extrato")
    print("  [u] 👤  Novo Usuário")
    print("  [c] 🏦  Nova Conta")
    print("  [l] 📋  Listar Contas")
    print("  [q] 🚪  Sair")
    separador()
    return input("  👉 Escolha uma opção: ").strip().lower()


# ─────────────────────────────────────────
#  Funções de operação bancária
# ─────────────────────────────────────────

def depositar(saldo, valor, extrato, /):
    """
    Recebe saldo, valor e extrato apenas por posição (/).
    Retorna o saldo e extrato atualizados.
    """
    if valor <= 0:
        print("\n  ❌ O valor do depósito deve ser maior que zero.")
        return saldo, extrato

    saldo += valor
    extrato += f"  💰 Depósito:  R$ {valor:>10.2f}\n"
    print(f"\n  ✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    print(f"  💳 Saldo atual: R$ {saldo:.2f}")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Recebe argumentos apenas por nome (*).
    Retorna saldo, extrato e número de saques atualizados.
    """
    excedeu_saldo  = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if valor <= 0:
        print("\n  ❌ O valor do saque deve ser maior que zero.")
    elif excedeu_saldo:
        print(f"\n  ❌ Saldo insuficiente! Seu saldo é R$ {saldo:.2f}")
    elif excedeu_limite:
        print(f"\n  ❌ Limite por saque é R$ {limite:.2f}. Tente um valor menor.")
    elif excedeu_saques:
        print(f"\n  ❌ Limite de {limite_saques} saques diários atingido.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f"  💸 Saque:      R$ {valor:>10.2f}\n"
        print(f"\n  ✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        print(f"  💳 Saldo atual: R$ {saldo:.2f}")
        print(f"  📊 Saques hoje: {numero_saques}/{limite_saques}")

    return saldo, extrato, numero_saques


def ver_extrato(saldo, /, *, extrato):
    """
    Exibe o histórico de movimentações e o saldo atual.
    Recebe saldo por posição (/) e extrato por nome (*).
    """
    separador("📄 EXTRATO")
    if not extrato:
        print("\n  ℹ️  Nenhuma movimentação realizada ainda.")
    else:
        print()
        print(extrato, end="")
    separador()
    print(f"  💳 Saldo atual: R$ {saldo:.2f}")


def criar_usuario(usuarios):
    separador("👤 NOVO USUÁRIO")
    cpf = input("  Informe o CPF (somente números): ")
    
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n  ❌ Já existe um usuário com esse CPF!")
        return

    nome = input("  Informe o nome completo: ")
    data_nascimento = input("  Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("  Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n  ✅ Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    separador("🏦 NOVA CONTA")
    cpf = input("  Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(f"\n  ✅ Conta criada com sucesso para {usuario['nome']}!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n  ❌ Usuário não encontrado! Fluxo de criação de conta encerrado.")
    return None


def listar_contas(contas):
    separador("📋 LISTA DE CONTAS")
    if not contas:
        print("  ℹ️  Nenhuma conta cadastrada.")
        return
        
    for conta in contas:
        linha = f"""
  Agência: {conta['agencia']}
  C/C:     {conta['numero_conta']}
  Titular: {conta['usuario']['nome']}"""
        print(linha)
        print("  " + "-" * 30)


# ─────────────────────────────────────────
#  Loop principal do programa
# ─────────────────────────────────────────

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    cabecalho()
    
    while True:
        opcao = exibir_menu()

        if opcao == "d":
            separador("💰 DEPÓSITO")
            try:
                valor = float(input("  Informe o valor do depósito: R$ "))
                # A função depositar recebe argumentos apenas por posição
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\n  ❌ Valor inválido! Digite um número.")

        elif opcao == "s":
            separador("💸 SAQUE")
            try:
                valor = float(input("  Informe o valor do saque: R$ "))
                # A função sacar recebe argumentos apenas por nome
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except ValueError:
                print("\n  ❌ Valor inválido! Digite um número.")

        elif opcao == "e":
            # A função ver_extrato recebe saldo por posição e extrato por nome
            ver_extrato(saldo, extrato=extrato)

        elif opcao == "u":
            criar_usuario(usuarios)
            
        elif opcao == "c":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                
        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            separador()
            print("  👋 Até logo! Obrigado por usar o Banco DGBANK!")
            separador()
            break

        else:
            print("\n  ⚠️  Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
