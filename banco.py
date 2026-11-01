"""
╔══════════════════════════════════════════════════════════╗
║                🏦  BANCO DGBANK (v3 POO)  🏦             ║
║     Sistema Bancário Modelado com Classes em Python     ║
║            Desafio DIO - Trilha Python Backend           ║
╚══════════════════════════════════════════════════════════╝
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ─────────────────────────────────────────────────────────
#  MODELO DE CLASSES (UML DIO)
# ─────────────────────────────────────────────────────────

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, numero: int, cliente: "Cliente"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: "Cliente", numero: int):
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> "Cliente":
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n  ❌ Operação falhou! Saldo insuficiente.")
        elif valor <= 0:
            print("\n  ❌ Operação falhou! O valor informado deve ser maior que zero.")
        else:
            self._saldo -= valor
            print(f"\n  ✅ Saque de R$ {valor:.2f} realizado com sucesso!")
            print(f"  💳 Saldo atual: R$ {self._saldo:.2f}")
            return True

        return False

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n  ❌ Operação falhou! O valor do depósito deve ser maior que zero.")
            return False

        self._saldo += valor
        print(f"\n  ✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        print(f"  💳 Saldo atual: R$ {self._saldo:.2f}")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: "Cliente", limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"\n  ❌ Limite por saque é R$ {self._limite:.2f}. Tente um valor menor.")
        elif excedeu_saques:
            print(f"\n  ❌ Limite diário de {self._limite_saques} saques já foi atingido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self) -> str:
        return (
            f"  Agência:\t{self.agencia}\n"
            f"  C/C:\t\t{self.numero}\n"
            f"  Titular:\t{self.cliente.nome}"
        )


class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento


# ─────────────────────────────────────────────────────────
#  INTERFACE VISUAL / CLI (ESTILO DGBANK)
# ─────────────────────────────────────────────────────────

def cabecalho():
    print("\n" + "═" * 46)
    print("║" + "   🏦  BANCO DGBANK (POO) — Bem-vindo(a)!   ".center(44) + "║")
    print("═" * 46)


def separador(titulo=""):
    if titulo:
        print(f"\n{'─' * 12} {titulo} {'─' * 12}")
    else:
        print("─" * 46)


def exibir_menu():
    """Mostra o menu elegante de opções ao usuário."""
    separador()
    print("  [d] 💰  Depositar")
    print("  [s] 💸  Sacar")
    print("  [e] 📄  Ver Extrato")
    print("  [u] 👤  Novo Usuário / Cliente")
    print("  [c] 🏦  Nova Conta Corrente")
    print("  [l] 📋  Listar Contas")
    print("  [q] 🚪  Sair")
    separador()
    return input("  👉 Escolha uma opção: ").strip().lower()


def filtrar_cliente(cpf: str, clientes: list) -> PessoaFisica | None:
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    clientes_filtrados = [
        cliente for cliente in clientes 
        if "".join(filter(str.isdigit, cliente.cpf)) == cpf_limpo
    ]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente: Cliente) -> Conta | None:
    if not cliente.contas:
        print("\n  ❌ Cliente não possui contas cadastradas!")
        return None

    # Se tiver apenas 1 conta, seleciona automaticamente
    if len(cliente.contas) == 1:
        return cliente.contas[0]

    # Se tiver mais de uma, permite escolher
    print("\n  Selecione a conta para a operação:")
    for i, conta in enumerate(cliente.contas, start=1):
        print(f"    [{i}] Agência: {conta.agencia} | Conta: {conta.numero}")

    try:
        escolha = int(input("  👉 Digite o número da opção desejada: "))
        if 1 <= escolha <= len(cliente.contas):
            return cliente.contas[escolha - 1]
        print("\n  ❌ Opção inválida!")
    except ValueError:
        print("\n  ❌ Entrada inválida!")

    return None


def depositar(clientes: list):
    separador("💰 DEPÓSITO")
    cpf = input("  Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("  Informe o valor do depósito: R$ "))
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n  ❌ Entrada inválida! Digite um valor numérico.")


def sacar(clientes: list):
    separador("💸 SAQUE")
    cpf = input("  Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("  Informe o valor do saque: R$ "))
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n  ❌ Entrada inválida! Digite um valor numérico.")


def exibir_extrato(clientes: list):
    separador("📄 EXTRATO")
    cpf = input("  Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    separador(f"EXTRATO: AG {conta.agencia} | CC {conta.numero}")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("\n  ℹ️  Nenhuma movimentação realizada nesta conta.")
    else:
        print()
        for transacao in transacoes:
            tipo = "💰 Depósito" if transacao["tipo"] == "Deposito" else "💸 Saque"
            print(f"  {tipo:<12} R$ {transacao['valor']:>10.2f}   ({transacao['data']})")

    separador()
    print(f"  💳 Saldo atual: R$ {conta.saldo:.2f}")


def criar_cliente(clientes: list):
    separador("👤 NOVO CLIENTE")
    cpf = input("  Informe o CPF (somente números): ").strip()
    
    if not cpf:
        print("\n  ❌ CPF não pode ser vazio!")
        return

    cliente_existente = filtrar_cliente(cpf, clientes)
    if cliente_existente:
        print("\n  ❌ Já existe um cliente cadastrado com este CPF!")
        return

    nome = input("  Informe o nome completo: ").strip()
    data_nascimento = input("  Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("  Informe o endereço (logradouro, nro - bairro - cidade/sigla): ").strip()

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)

    print("\n  ✅ Cliente cadastrado com sucesso!")


def criar_conta(numero_conta: int, clientes: list, contas: list):
    separador("🏦 NOVA CONTA CORRENTE")
    cpf = input("  Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado! Cadastre o cliente primeiro.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"\n  ✅ Conta número {numero_conta} criada com sucesso para {cliente.nome}!")


def listar_contas(contas: list):
    separador("📋 LISTA DE CONTAS")
    if not contas:
        print("  ℹ️  Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print()
        print(str(conta))
        print("  " + "-" * 32)


# ─────────────────────────────────────────────────────────
#  LOOP PRINCIPAL DO SISTEMA
# ─────────────────────────────────────────────────────────

def main():
    clientes = []
    contas = []

    cabecalho()

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

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
