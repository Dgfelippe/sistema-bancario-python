# 🏦 Sistema Bancário DGBANK — Desafio Python DIO

Projeto desenvolvido como parte da **Trilha de Python** da [Digital Innovation One (DIO)](https://www.dio.me/).

## 📋 Sobre o Projeto

Sistema bancário de terminal que simula operações essenciais de uma conta corrente, com foco em lógica de programação, estruturas de controle e organização de código em funções.

## ⚙️ Funcionalidades

| Operação | Descrição |
|---|---|
| 💰 Depósito | Adiciona valor ao saldo com validação |
| 💸 Saque | Realiza saques com 3 regras de segurança |
| 📄 Extrato | Exibe o histórico completo de movimentações |

### Regras de Negócio

- ✅ Só aceita depósitos com valor positivo
- ✅ Limite máximo de **R$ 500,00** por saque
- ✅ Máximo de **3 saques** por dia
- ✅ Impede saque quando saldo é insuficiente

## 🚀 Como Executar

**Pré-requisito:** Python 3.x instalado

```bash
# Clone o repositório
git clone https://github.com/SEU-USUARIO/sistema-bancario-python.git

# Acesse a pasta
cd sistema-bancario-python

# Execute o programa
python banco.py
```

## 🖥️ Demonstração

```
══════════════════════════════════════════════
║       🏦  BANCO DGBANK — Bem-vindo(a)!      ║
══════════════════════════════════════════════
  👤 Digite seu nome: Diogo

  Olá, Diogo! Seja bem-vindo(a) ao Banco DGBANK. 🎉

────────────────────────────────────────────
  [d] 💰  Depositar
  [s] 💸  Sacar
  [e] 📄  Ver Extrato
  [q] 🚪  Sair
────────────────────────────────────────────
  👉 Escolha uma opção:
```

## 🛠️ Tecnologias

- **Python 3.x**
- Biblioteca padrão (sem dependências externas)

## 📚 Conceitos Aplicados

- Variáveis e tipos de dados
- Estruturas condicionais (`if/elif/else`)
- Laço de repetição (`while`)
- Funções com parâmetros e retorno de valores
- Tratamento de erros (`try/except`)
- Formatação de strings com f-strings

## 👤 Autor

Feito com 💙 durante a Trilha Python da DIO.

---

> **Digital Innovation One** | Trilha Python | Desafio: Sistema Bancário
