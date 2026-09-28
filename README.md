# 🏦 Sistema Bancário DGBANK (v2) — Desafio Python DIO

Projeto desenvolvido como parte da **Trilha de Python** da [Digital Innovation One (DIO)](https://www.dio.me/).

## 📋 Sobre o Projeto

Sistema bancário de terminal que simula operações de uma conta corrente. Na **Versão 2 (v2)**, o sistema foi refatorado para utilizar **Funções** (modularizando o código) e agora suporta o cadastro de múltiplos **Usuários (Clientes)** e a criação de múltiplas **Contas Correntes**.

## ⚙️ Funcionalidades

| Operação | Descrição |
|---|---|
| 💰 **Depósito** | Adiciona valor ao saldo com validação |
| 💸 **Saque** | Realiza saques com regras de limite e quantidade |
| 📄 **Extrato** | Exibe o histórico completo de movimentações |
| 👤 **Criar Usuário** | Cadastra novos clientes vinculados ao seu CPF |
| 🏦 **Criar Conta** | Cria contas correntes associadas a um usuário cadastrado |
| 📋 **Listar Contas** | Lista todas as contas criadas e seus respectivos donos |

### Regras de Negócio e Validações

**Operações Bancárias:**
- ✅ Só aceita depósitos com valor positivo.
- ✅ Limite máximo de **R$ 500,00** por saque.
- ✅ Máximo de **3 saques** por dia.
- ✅ Impede saque quando o saldo é insuficiente.

**Usuários e Contas:**
- ✅ Um usuário é composto por nome, CPF, data de nascimento e endereço completo.
- ✅ **Não é permitido** cadastrar mais de um usuário com o mesmo CPF.
- ✅ As contas pertencem a um usuário e possuem numeração sequencial iniciando em 1.
- ✅ O número da agência é sempre fixo ("0001").
- ✅ Um usuário pode ter várias contas correntes, mas uma conta tem apenas um dono.

## 🚀 Como Executar

**Pré-requisito:** Python 3.x instalado

```bash
# Clone o repositório
git clone https://github.com/Dgfelippe/sistema-bancario-python.git

# Acesse a pasta
cd sistema-bancario-python

# Execute o programa
python banco.py
```

## 🖥️ Demonstração

```text
════════════════════════════════════════════
║       🏦  BANCO DGBANK — Bem-vindo(a)!   ║
════════════════════════════════════════════

──────────  ──────────
  [d] 💰  Depositar
  [s] 💸  Sacar
  [e] 📄  Ver Extrato
  [u] 👤  Novo Usuário
  [c] 🏦  Nova Conta
  [l] 📋  Listar Contas
  [q] 🚪  Sair
──────────  ──────────
  👉 Escolha uma opção: 
```

## 📚 Conceitos Avançados Aplicados (v2)

- Funções com múltiplos retornos
- Argumentos Posicionais (`/`) e Nomeados (`*`) em Funções Python
- Utilização de Listas (`list`) e Dicionários (`dict`)
- Lógica de filtros em listas (`list comprehension`)
- Organização de código em métodos para maior legibilidade

## 👤 Autor

Feito com 💙 durante a Trilha Python AI Backend Developer da DIO.

---

> **Digital Innovation One** | Trilha Python | Desafio: Otimizando o Sistema Bancário com Funções Python
