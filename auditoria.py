"""Registro das chamadas de operações bancárias em log.txt."""

from datetime import datetime
from functools import wraps
from pathlib import Path


ARQUIVO_LOG = Path(__file__).resolve().with_name("log.txt")


def log_transacao(funcao):
    """Registra chamadas e preserva o retorno ou a exceção da função."""
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        data_hora = datetime.now().astimezone().isoformat(timespec="seconds")
        argumentos = repr(args)
        argumentos_nomeados = repr(kwargs)
        try:
            resultado = funcao(*args, **kwargs)
        except Exception as erro:
            desfecho = f"sem retorno | erro={type(erro).__name__}: {erro}"
            raise
        else:
            desfecho = repr(resultado)
            return resultado
        finally:
            registro = (
                f"{data_hora} | funcao={funcao.__qualname__} | "
                f"args={argumentos} | kwargs={argumentos_nomeados} | "
                f"retorno={desfecho}"
            )
            registro = registro.replace("\r", "\\r").replace("\n", "\\n")
            with ARQUIVO_LOG.open("a", encoding="utf-8") as arquivo:
                arquivo.write(registro + "\n")

    return wrapper
