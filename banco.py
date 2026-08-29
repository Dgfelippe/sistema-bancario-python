"""
╔══════════════════════════════════════════╗
║         🏦  BANCO DGBANK  🏦               ║
║    Sistema Bancário - Desafio Python     ║
╚══════════════════════════════════════════╝
"""

# ─────────────────────────────────────────
#  PASSO 1: Variáveis de estado da conta
#  (a "memória" do nosso banco enquanto
#   o programa está rodando)
# ─────────────────────────────────────────

saldo = 0               # quanto tem na conta
limite = 500            # limite máximo por saque
extrato = ""            # histórico de movimentações
numero_saques = 0       # quantos saques foram feitos
LIMITE_SAQUES = 3       # máximo de saques permitidos por dia


# ─────────────────────────────────────────
#  PASSO 2: Funções visuais (deixam o
#  terminal bonito e organizado)
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
    print("  [q] 🚪  Sair")
    separador()
    return input("  👉 Escolha uma opção: ").strip().lower()


# ─────────────────────────────────────────
#  PASSO 3: Funções de operação bancária
#  (cada uma resolve um problema pequeno)
# ─────────────────────────────────────────

def depositar(nome, saldo, extrato):
    """
    Recebe o nome, saldo e extrato atuais.
    Valida e processa um depósito.
    Retorna o saldo e extrato atualizados.
    """
    separador("💰 DEPÓSITO")
    print(f"  Cliente: {nome}")
    try:
        valor = float(input("  Informe o valor do depósito: R$ "))
    except ValueError:
        print("\n  ❌ Valor inválido! Digite um número.")
        return saldo, extrato

    if valor <= 0:
        print("\n  ❌ O valor do depósito deve ser maior que zero.")
        return saldo, extrato

    saldo += valor
    extrato += f"  💰 Depósito:  R$ {valor:>10.2f}\n"
    print(f"\n  ✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    print(f"  💳 Saldo atual: R$ {saldo:.2f}")

    return saldo, extrato


def sacar(nome, saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    """
    Recebe nome e dados da conta.
    Valida 3 regras e processa o saque.
    Retorna saldo, extrato e número de saques atualizados.
    """
    separador("💸 SAQUE")
    # ✅ CORREÇÃO: o nome já chegou como parâmetro — só exibimos, não pedimos de novo!
    print(f"  Cliente: {nome}")
    try:
        valor = float(input("  Informe o valor do saque: R$ "))
    except ValueError:
        print("\n  ❌ Valor inválido! Digite um número.")
        return saldo, extrato, numero_saques

    # ── Validações ───────────────────────
    excedeu_saldo  = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if valor <= 0:
        print("\n  ❌ O valor do saque deve ser maior que zero.")
    elif excedeu_saldo:
        print(f"\n  ❌ Saldo insuficiente! Seu saldo é R$ {saldo:.2f}")
    elif excedeu_limite:
        print(f"\n  ❌ Limite por saque é R$ {limite:.2f}. Tente um valor menor.")
    elif excedeu_saques:
        print(f"\n  ❌ Limite de {LIMITE_SAQUES} saques diários atingido.")
    else:
        # ── Operação aprovada! ────────────
        saldo -= valor
        numero_saques += 1
        extrato += f"  💸 Saque:      R$ {valor:>10.2f}\n"
        print(f"\n  ✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        print(f"  💳 Saldo atual: R$ {saldo:.2f}")
        print(f"  📊 Saques hoje: {numero_saques}/{LIMITE_SAQUES}")

    return saldo, extrato, numero_saques


def ver_extrato(nome, saldo, extrato):
    """
    Exibe o histórico de movimentações e o saldo atual.
    """
    separador("📄 EXTRATO")
    print(f"  Cliente: {nome}")
    if not extrato:
        print("\n  ℹ️  Nenhuma movimentação realizada ainda.")
    else:
        print()
        print(extrato, end="")
    separador()
    print(f"  💳 Saldo atual: R$ {saldo:.2f}")


# ─────────────────────────────────────────
#  PASSO 4: Loop principal do programa
#  (o "coração" que mantém tudo rodando)
# ─────────────────────────────────────────

cabecalho()
# ✅ Pedimos o nome UMA ÚNICA VEZ, antes do loop começar
nome = input("  👤 Digite seu nome: ").strip()
print(f"\n  Olá, {nome}! Seja bem-vindo(a) ao Banco DGBANK. 🎉")

while True:
    opcao = exibir_menu()

    if opcao == "d":
        saldo, extrato = depositar(nome, saldo, extrato)

    elif opcao == "s":
        saldo, extrato, numero_saques = sacar(
            nome, saldo, extrato, numero_saques, limite, LIMITE_SAQUES
        )

    elif opcao == "e":
        ver_extrato(nome, saldo, extrato)

    elif opcao == "q":
        separador()
        # ✅ Mensagem de saída personalizada com o nome do cliente
        print(f"  👋 Até logo, {nome}! Obrigado por usar o Banco DGBANK!")
        separador()
        break

    else:
        print("\n  ⚠️  Opção inválida. Tente novamente.")
