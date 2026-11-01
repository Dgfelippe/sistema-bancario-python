"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🏦  BANCO DGBANK ULTRA (v3.5 POO)  🏦                 ║
║   Sistema Bancário Completo: Validação de CPF, Contas, Extrato com      ║
║       Filtros por Data, Cartão de Crédito com Fatura e Limite,           ║
║        Transferência PIX entre Contas e Auditoria de Atividades          ║
║                 Desafio DIO - Trilha Python AI Backend                   ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

from abc import ABC, abstractmethod
from datetime import datetime, date
import re


# ─────────────────────────────────────────────────────────────────────────
#  UTILITÁRIOS & VALIDAÇÕES DO MUNDO REAL
# ─────────────────────────────────────────────────────────────────────────

def limpar_cpf(cpf: str) -> str:
    """Remove caracteres não numéricos do CPF."""
    return "".join(filter(str.isdigit, str(cpf)))


def validar_cpf(cpf: str) -> bool:
    """Valida o CPF pelos dígitos verificadores (Algoritmo Oficial da Receita Federal)."""
    cpf_numeros = limpar_cpf(cpf)

    if len(cpf_numeros) != 11:
        return False

    # Bloqueia números repetidos como 111.111.111-11
    if cpf_numeros == cpf_numeros[0] * 11:
        return False

    # Primeiro dígito verificador
    soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    d1 = 0 if resto == 10 else resto
    if d1 != int(cpf_numeros[9]):
        return False

    # Segundo dígito verificador
    soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    d2 = 0 if resto == 10 else resto
    if d2 != int(cpf_numeros[10]):
        return False

    return True


def formatar_cpf(cpf: str) -> str:
    cpf_limpo = limpar_cpf(cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf


# ─────────────────────────────────────────────────────────────────────────
#  MODELO DE TRANSAÇÕES (UML DIO + EXPANSÃO)
# ─────────────────────────────────────────────────────────────────────────

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class TransferenciaPix(Transacao):
    def __init__(self, valor: float, conta_destino: "Conta"):
        self._valor = valor
        self._conta_destino = conta_destino

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def conta_destino(self) -> "Conta":
        return self._conta_destino

    def registrar(self, conta: "Conta") -> bool:
        if conta == self._conta_destino:
            print("\n  ❌ Operação cancelada! Não é possível fazer PIX para a mesma conta.")
            return False

        if conta.saldo < self.valor:
            print(f"\n  ❌ Saldo insuficiente para PIX! Seu saldo é R$ {conta.saldo:.2f}")
            return False

        if self.valor <= 0:
            print("\n  ❌ O valor do PIX deve ser maior que zero.")
            return False

        # Debita da conta de origem
        conta._saldo -= self.valor
        # Credita na conta de destino
        self._conta_destino._saldo += self.valor

        # Registra no histórico de ambas as contas
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta.historico.adicionar_registro(
            tipo="PIX Enviado",
            valor=self.valor,
            data=agora,
            detalhe=f"Para: {self._conta_destino.cliente.nome} (CC {self._conta_destino.numero})"
        )
        self._conta_destino.historico.adicionar_registro(
            tipo="PIX Recebido",
            valor=self.valor,
            data=agora,
            detalhe=f"De: {conta.cliente.nome} (CC {conta.numero})"
        )

        print(f"\n  ⚡ PIX de R$ {self.valor:.2f} enviado com sucesso para {self._conta_destino.cliente.nome}!")
        print(f"  💳 Seu saldo atual: R$ {conta.saldo:.2f}")
        return True


# ─────────────────────────────────────────────────────────────────────────
#  HISTÓRICO & AUDITORIA DE ATIVIDADES
# ─────────────────────────────────────────────────────────────────────────

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self) -> list:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "data_obj": datetime.now(),
            "detalhe": "Operação padrão em terminal"
        })

    def adicionar_registro(self, tipo: str, valor: float, data: str, detalhe: str = ""):
        self._transacoes.append({
            "tipo": tipo,
            "valor": valor,
            "data": data,
            "data_obj": datetime.now(),
            "detalhe": detalhe
        })

    def gerar_relatorio(self, tipo_filtro: str = None) -> list:
        """Permite filtrar o extrato por tipo ou data."""
        if not tipo_filtro:
            return self._transacoes
        return [t for t in self._transacoes if t["tipo"].lower() == tipo_filtro.lower()]


# ─────────────────────────────────────────────────────────────────────────
#  CARTÃO DE CRÉDITO & FATURA
# ─────────────────────────────────────────────────────────────────────────

class ItemFatura:
    def __init__(self, descricao: str, valor: float, data: str):
        self.descricao = descricao
        self.valor = valor
        self.data = data


class CartaoCredito:
    def __init__(self, numero: str, limite_total: float = 2000.0):
        self._numero = numero
        self._limite_total = limite_total
        self._limite_utilizado = 0.0
        self._fatura_itens: list[ItemFatura] = []

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def limite_total(self) -> float:
        return self._limite_total

    @property
    def limite_disponivel(self) -> float:
        return self._limite_total - self._limite_utilizado

    @property
    def valor_fatura(self) -> float:
        return self._limite_utilizado

    def realizar_compra(self, descricao: str, valor: float) -> bool:
        if valor <= 0:
            print("\n  ❌ O valor da compra deve ser positivo.")
            return False

        if valor > self.limite_disponivel:
            print(f"\n  ❌ Compra não autorizada! Limite disponível: R$ {self.limite_disponivel:.2f}")
            return False

        self._limite_utilizado += valor
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._fatura_itens.append(ItemFatura(descricao, valor, agora))
        print(f"\n  🛍️ Compra de '{descricao}' de R$ {valor:.2f} aprovada no Crédito!")
        print(f"  💳 Limite disponível restante: R$ {self.limite_disponivel:.2f}")
        return True

    def pagar_fatura(self, conta: "Conta", valor: float) -> bool:
        if valor <= 0:
            print("\n  ❌ Valor de pagamento inválido.")
            return False

        if valor > self._limite_utilizado:
            print(f"\n  ⚠️ O valor do pagamento (R$ {valor:.2f}) é maior que a fatura atual (R$ {self._limite_utilizado:.2f}). Ajustando para valor total.")
            valor = self._limite_utilizado

        if conta.saldo < valor:
            print(f"\n  ❌ Saldo em conta insuficiente para pagar fatura! Saldo: R$ {conta.saldo:.2f}")
            return False

        conta._saldo -= valor
        self._limite_utilizado -= valor
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta.historico.adicionar_registro(
            tipo="Pagamento Fatura",
            valor=valor,
            data=agora,
            detalhe=f"Cartão final {self._numero[-4:]}"
        )
        print(f"\n  ✅ Fatura paga com sucesso! R$ {valor:.2f} debitado da Conta.")
        print(f"  💳 Saldo restante na Conta: R$ {conta.saldo:.2f}")
        print(f"  💳 Novo Limite Disponível no Cartão: R$ {self.limite_disponivel:.2f}")
        return True

    def exibir_fatura(self):
        print("\n" + "═" * 46)
        print("║" + f"   💳 FATURA DO CARTÃO (Final {self._numero[-4:]})   ".center(44) + "║")
        print("═" * 46)
        print(f"  Limite Total:       R$ {self._limite_total:>10.2f}")
        print(f"  Limite Utilizado:   R$ {self._limite_utilizado:>10.2f}")
        print(f"  Limite Disponível:  R$ {self.limite_disponivel:>10.2f}")
        print("─" * 46)

        if not self._fatura_itens:
            print("  ℹ️  Nenhum lançamento nesta fatura.")
        else:
            print("  Lançamentos:")
            for item in self._fatura_itens:
                print(f"   • {item.data} | {item.descricao:<18} R$ {item.valor:>8.2f}")

        print("═" * 46)
        print(f"  👉 TOTAL DA FATURA ABERTA: R$ {self.valor_fatura:.2f}")
        print("═" * 46)


# ─────────────────────────────────────────────────────────────────────────
#  MODELO DE CONTAS (UML DIO + EXTENSÃO)
# ─────────────────────────────────────────────────────────────────────────

class Conta:
    def __init__(self, numero: int, cliente: "Cliente"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        # Cada conta pode ter um cartão de crédito vinculado
        numero_cartao = f"4002 8922 {str(numero).zfill(4)} {datetime.now().strftime('%y%m')}"
        self._cartao = CartaoCredito(numero=numero_cartao, limite_total=2500.0)

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

    @property
    def cartao(self) -> CartaoCredito:
        return self._cartao

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(f"\n  ❌ Operação falhou! Saldo insuficiente. Saldo atual: R$ {saldo:.2f}")
        elif valor <= 0:
            print("\n  ❌ Operação falhou! O valor informado deve ser maior que zero.")
        else:
            self._saldo -= valor
            print(f"\n  ✅ Saque de R$ {valor:.2f} realizado com sucesso!")
            print(f"  💳 Saldo atual da conta: R$ {self._saldo:.2f}")
            return True

        return False

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n  ❌ Operação falhou! O valor do depósito deve ser maior que zero.")
            return False

        self._saldo += valor
        print(f"\n  ✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        print(f"  💳 Saldo atual da conta: R$ {self._saldo:.2f}")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: "Cliente", limite: float = 1000.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    def saques_realizados_hoje(self) -> int:
        hoje_str = datetime.now().strftime("%d/%m/%Y")
        return len([
            t for t in self.historico.transacoes 
            if (t["tipo"] == Saque.__name__ or t["tipo"] == "Saque") and t["data"].startswith(hoje_str)
        ])

    def sacar(self, valor: float) -> bool:
        numero_saques = self.saques_realizados_hoje()
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"\n  ❌ O valor do saque (R$ {valor:.2f}) excede o limite permitido por saque de R$ {self._limite:.2f}.")
        elif excedeu_saques:
            print(f"\n  ❌ Limite de {self._limite_saques} saques diários atingido para hoje!")
        else:
            sucesso = super().sacar(valor)
            if sucesso:
                print(f"  📊 Saques utilizados hoje: {numero_saques + 1}/{self._limite_saques}")
            return sucesso

        return False

    def __str__(self) -> str:
        return (
            f"  Agência:\t{self.agencia}\n"
            f"  Conta C/C:\t{self.numero}\n"
            f"  Titular:\t{self.cliente.nome}\n"
            f"  CPF Titular:\t{formatar_cpf(self.cliente.cpf)}\n"
            f"  Saldo Atual:\tR$ {self.saldo:.2f}\n"
            f"  Cartão Fin.:\t{self.cartao.numero[-4:]} (Limite disp: R$ {self.cartao.limite_disponivel:.2f})"
        )


# ─────────────────────────────────────────────────────────────────────────
#  MODELO DE CLIENTES (UML DIO)
# ─────────────────────────────────────────────────────────────────────────

class Cliente:
    def __init__(self, endereco: str, telefone: str = "", email: str = ""):
        self._endereco = endereco
        self._telefone = telefone
        self._email = email
        self._contas: list[Conta] = []
        self._data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def telefone(self) -> str:
        return self._telefone

    @property
    def email(self) -> str:
        return self._email

    @property
    def contas(self) -> list:
        return self._contas

    @property
    def data_cadastro(self) -> str:
        return self._data_cadastro

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str, telefone: str = "", email: str = ""):
        super().__init__(endereco, telefone, email)
        self._cpf = limpar_cpf(cpf)
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

    def __str__(self) -> str:
        return (
            f"  Nome:          {self.nome}\n"
            f"  CPF:           {formatar_cpf(self.cpf)}\n"
            f"  Nascimento:    {self.data_nascimento}\n"
            f"  Endereço:      {self.endereco}\n"
            f"  Telefone:      {self.telefone or 'Não informado'}\n"
            f"  Email:         {self.email or 'Não informado'}\n"
            f"  Desde:         {self.data_cadastro}\n"
            f"  Total Contas:  {len(self.contas)}"
        )


# ─────────────────────────────────────────────────────────────────────────
#  INTERFACE VISUAL / CLI (ESTILO DGBANK COMPLETO)
# ─────────────────────────────────────────────────────────────────────────

def cabecalho():
    print("\n" + "═" * 50)
    print("║" + "   🏦  BANCO DGBANK — SISTEMA COMPLETO   ".center(48) + "║")
    print("║" + "      Contas • Cartão • Extrato • PIX     ".center(48) + "║")
    print("═" * 50)


def separador(titulo=""):
    if titulo:
        print(f"\n{'─' * 14} {titulo} {'─' * 14}")
    else:
        print("─" * 50)


def exibir_menu():
    separador()
    print("  [d]  💰  Depositar")
    print("  [s]  💸  Sacar")
    print("  [p]  ⚡  Transferência PIX")
    print("  [e]  📄  Extrato Completo & Histórico")
    print("  [f]  💳  Fatura do Cartão de Crédito")
    print("  [k]  🛍️  Simular Compra no Crédito")
    print("  [pg] 💵  Pagar Fatura do Cartão")
    print("  [u]  👤  Novo Cliente (Cadastro Completo)")
    print("  [du] 🔍  Consultar Dados do Cliente")
    print("  [c]  🏦  Nova Conta Corrente")
    print("  [l]  📋  Listar Contas")
    print("  [q]  🚪  Sair")
    separador()
    return input("  👉 Escolha uma opção: ").strip().lower()


def filtrar_cliente(cpf: str, clientes: list) -> PessoaFisica | None:
    cpf_limpo = limpar_cpf(cpf)
    for cliente in clientes:
        if cliente.cpf == cpf_limpo:
            return cliente
    return None


def recuperar_conta_cliente(cliente: Cliente) -> Conta | None:
    if not cliente.contas:
        print("\n  ❌ Este cliente não possui nenhuma conta cadastrada!")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\n  O cliente possui múltiplas contas. Selecione uma:")
    for i, conta in enumerate(cliente.contas, start=1):
        print(f"    [{i}] Agência: {conta.agencia} | Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}")

    try:
        opcao = int(input("  👉 Digite o número da conta desejada: "))
        if 1 <= opcao <= len(cliente.contas):
            return cliente.contas[opcao - 1]
        print("\n  ❌ Opção de conta inválida!")
    except ValueError:
        print("\n  ❌ Entrada inválida! Digite um número.")

    return None


# ─────────────────────────────────────────────────────────────────────────
#  FLUXOS DE OPERAÇÕES BANCÁRIAS
# ─────────────────────────────────────────────────────────────────────────

def criar_cliente(clientes: list):
    separador("👤 CADASTRO DE CLIENTE")
    cpf_input = input("  Informe o CPF (somente números ou formatado): ").strip()
    cpf_limpo = limpar_cpf(cpf_input)

    # 1. Validação de formato e dígitos verificadores
    if not validar_cpf(cpf_limpo):
        print("\n  ❌ CPF INVÁLIDO!")
        print("  O CPF informado não existe ou possui dígitos verificadores incorretos.")
        return

    # 2. Verificação se CPF já está cadastrado
    cliente_existente = filtrar_cliente(cpf_limpo, clientes)
    if cliente_existente:
        print("\n  ⚠️  CLIENTE JÁ CADASTRADO NO SISTEMA!")
        print("  Detalhes do cliente já registrado:")
        print("  " + "-" * 40)
        print(str(cliente_existente))
        print("  " + "-" * 40)
        print("  Dica: Você pode criar uma nova conta vinculada para este CPF na opção [c].")
        return

    # 3. Solicitação de dados cadastrais completos
    nome = input("  Informe o nome completo: ").strip()
    while not nome:
        print("  ❌ Nome não pode ser vazio.")
        nome = input("  Informe o nome completo: ").strip()

    data_nascimento = input("  Informe a data de nascimento (dd/mm/aaaa): ").strip()
    
    # Validação simples de data
    try:
        partes = data_nascimento.replace("-", "/").split("/")
        if len(partes) == 3:
            d, m, y = int(partes[0]), int(partes[1]), int(partes[2])
            date(y, m, d)
        else:
            raise ValueError
    except Exception:
        print("  ⚠️ Data em formato inválido! Use o padrão dd/mm/aaaa.")
        return

    print("\n  📍 Dados de Endereço:")
    logradouro = input("    Logradouro (Rua/Av/Travessa): ").strip()
    numero = input("    Número: ").strip()
    bairro = input("    Bairro: ").strip()
    cidade = input("    Cidade: ").strip()
    estado = input("    Estado (Sigla ex: SP, RJ): ").strip().upper()
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    print("\n  📞 Contato (Opcional):")
    telefone = input("    Telefone/Celular: ").strip()
    email = input("    E-mail: ").strip()

    novo_cliente = PessoaFisica(
        cpf=cpf_limpo,
        nome=nome,
        data_nascimento=data_nascimento,
        endereco=endereco,
        telefone=telefone,
        email=email
    )
    clientes.append(novo_cliente)

    print("\n  ✅ CLIENTE CADASTRADO COM SUCESSO!")
    print(f"  👤 Nome: {novo_cliente.nome}")
    print(f"  🆔 CPF:  {formatar_cpf(novo_cliente.cpf)}")
    print(f"  📍 End:  {novo_cliente.endereco}")


def consultar_cliente(clientes: list):
    separador("🔍 CONSULTAR DADOS DO CLIENTE")
    cpf = input("  Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Nenhum cliente encontrado com este CPF!")
        return

    print("\n" + str(cliente))
    if cliente.contas:
        print("\n  🏦 Contas vinculadas:")
        for c in cliente.contas:
            print(f"    • Agência: {c.agencia} | Conta: {c.numero} | Saldo: R$ {c.saldo:.2f}")
    else:
        print("\n  ℹ️ O cliente ainda não possui nenhuma conta bancária aberta.")


def criar_conta(numero_conta: int, clientes: list, contas: list):
    separador("🏦 ABERTURA DE NOVA CONTA CORRENTE")
    cpf = input("  Informe o CPF do titular: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado no sistema!")
        print("  Cadastre o cliente primeiro utilizando a opção [u].")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"\n  ✅ CONTA CORRENTE ABERTA COM SUCESSO!")
    print(f"  Agência:         {conta.agencia}")
    print(f"  Número da Conta: {conta.numero}")
    print(f"  Titular:         {cliente.nome} (CPF: {formatar_cpf(cliente.cpf)})")
    print(f"  Cartão Criado:   {conta.cartao.numero} (Limite: R$ {conta.cartao.limite_total:.2f})")


def depositar(clientes: list):
    separador("💰 DEPÓSITO EM CONTA")
    cpf = input("  Informe o CPF do titular: ").strip()
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
        print("\n  ❌ Digite um valor numérico válido!")


def sacar(clientes: list):
    separador("💸 SAQUE EM CONTA")
    cpf = input("  Informe o CPF do titular: ").strip()
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
        print("\n  ❌ Digite um valor numérico válido!")


def transferir_pix(clientes: list, contas: list):
    separador("⚡ TRANSFERÊNCIA PIX")
    cpf_origem = input("  Informe o seu CPF (Origem): ").strip()
    cliente_origem = filtrar_cliente(cpf_origem, clientes)

    if not cliente_origem:
        print("\n  ❌ Cliente de origem não encontrado!")
        return

    conta_origem = recuperar_conta_cliente(cliente_origem)
    if not conta_origem:
        return

    print(f"  💳 Saldo disponível para transferência: R$ {conta_origem.saldo:.2f}")

    cpf_destino = input("\n  Informe o CPF do favorecido (Destino): ").strip()
    cliente_destino = filtrar_cliente(cpf_destino, clientes)

    if not cliente_destino:
        print("\n  ❌ Favorecido não encontrado no sistema!")
        return

    conta_destino = recuperar_conta_cliente(cliente_destino)
    if not conta_destino:
        return

    print(f"  Confirmar envio para: {cliente_destino.nome} (Conta {conta_destino.numero})")

    try:
        valor = float(input("  Informe o valor do PIX: R$ "))
        pix = TransferenciaPix(valor=valor, conta_destino=conta_destino)
        cliente_origem.realizar_transacao(conta_origem, pix)
    except ValueError:
        print("\n  ❌ Digite um valor numérico válido!")


def exibir_extrato(clientes: list):
    separador("📄 EXTRATO & HISTÓRICO DE ATIVIDADES")
    cpf = input("  Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    separador(f"EXTRATO DA CONTA {conta.numero} - TITULAR: {cliente.nome}")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("\n  ℹ️  Nenhuma movimentação realizada nesta conta.")
    else:
        print(f"\n  {'DATA / HORA':<20} | {'TIPO':<15} | {'VALOR (R$)':>10} | {'DETALHES'}")
        print("  " + "─" * 68)
        for t in transacoes:
            tipo = t["tipo"]
            valor = f"R$ {t['valor']:>8.2f}"
            detalhe = t.get("detalhe", "")
            print(f"  {t['data']:<20} | {tipo:<15} | {valor:>10} | {detalhe}")

    separador()
    print(f"  💳 Saldo em Conta Corrente: R$ {conta.saldo:.2f}")
    print(f"  🛍️ Fatura em Aberto:       R$ {conta.cartao.valor_fatura:.2f}")
    print(f"  💳 Limite Cartão Dispon.:  R$ {conta.cartao.limite_disponivel:.2f}")


def simular_compra_cartao(clientes: list):
    separador("🛍️ SIMULAR COMPRA NO CRÉDITO")
    cpf = input("  Informe o CPF do titular: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print(f"  Cartão: {conta.cartao.numero}")
    print(f"  Limite Disponível: R$ {conta.cartao.limite_disponivel:.2f}")

    descricao = input("  Estabelecimento / Descrição da compra: ").strip()
    try:
        valor = float(input("  Valor da compra: R$ "))
        conta.cartao.realizar_compra(descricao, valor)
    except ValueError:
        print("\n  ❌ Valor numérico inválido!")


def exibir_fatura_cartao(clientes: list):
    separador("💳 FATURA DO CARTÃO")
    cpf = input("  Informe o CPF do titular: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    conta.cartao.exibir_fatura()


def pagar_fatura_cartao(clientes: list):
    separador("💵 PAGAMENTO DE FATURA")
    cpf = input("  Informe o CPF do titular: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n  ❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print(f"  Valor atual da fatura: R$ {conta.cartao.valor_fatura:.2f}")
    print(f"  Saldo disponível na conta: R$ {conta.saldo:.2f}")

    if conta.cartao.valor_fatura == 0:
        print("\n  ℹ️ Esta fatura está zerada! Nenhum pagamento necessário.")
        return

    try:
        valor = float(input("  Informe o valor que deseja pagar da fatura: R$ "))
        conta.cartao.pagar_fatura(conta, valor)
    except ValueError:
        print("\n  ❌ Valor numérico inválido!")


def listar_contas(contas: list):
    separador("📋 LISTA DE TODAS AS CONTAS")
    if not contas:
        print("  ℹ️  Nenhuma conta cadastrada no banco.")
        return

    for conta in contas:
        print()
        print(str(conta))
        print("  " + "─" * 46)


# ─────────────────────────────────────────────────────────────────────────
#  LOOP PRINCIPAL DO SISTEMA
# ─────────────────────────────────────────────────────────────────────────

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

        elif opcao == "p":
            transferir_pix(clientes, contas)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "f":
            exibir_fatura_cartao(clientes)

        elif opcao == "k":
            simular_compra_cartao(clientes)

        elif opcao == "pg":
            pagar_fatura_cartao(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "du":
            consultar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            separador()
            print("  👋 Obrigado por utilizar o Banco DGBANK!")
            print("  Sistema encerrado com segurança.")
            separador()
            break

        else:
            print("\n  ⚠️  Opção inválida! Escolha uma opção do menu.")


if __name__ == "__main__":
    main()
