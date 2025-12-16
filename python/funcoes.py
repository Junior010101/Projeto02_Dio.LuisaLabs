from datetime import datetime as date
from functools import wraps

from python.servicos import ContaCorrente, Deposito, PessoaFisica, Saque
from python.utils import (
    buscar_log,
    buscar_usuario,
    salvar_log,
    validar_cpf,
    validar_data_nascimento,
)


def registrar_log():
    def criar_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            registro_log = buscar_log()
            log_id = max(registro_log.keys(), default=0) + 1

            kwargs_filtrados = {k: v for k, v in kwargs.items() if k != "log"}

            def safe(valor):
                if isinstance(valor, (int, float, str, bool, type(None))):
                    return valor
                return str(valor)

            registro_log[log_id] = {
                "horario": date.now().strftime("%d-%m-%Y %H:%M:%S"),
                "evento": func.__name__,
                "args": [safe(a) for a in args],
                "kwargs": {k: safe(v) for k, v in kwargs_filtrados.items()},
                "status": False,
            }

            resultado = func(*args, **kwargs)

            if isinstance(resultado, tuple) and len(resultado) > 0:
                registro_log[log_id]["status"] = bool(resultado[0])

            salvar_log(registro_log)

            return resultado

        return wrapper

    return criar_log


def saque(*, valor, clientes, id_usuario, id_conta):
    if not clientes[id_usuario].contas[id_conta]:
        return None, "Conta inexistente."

    conta = clientes[id_usuario].contas[id_conta]
    resultado, resposta = Saque(valor).registrar(
        conta=conta,
        id_usuario=id_usuario,
    )

    if resultado:
        return conta, resposta

    return None, resposta


def deposito(valor, clientes, id_usuario, id_conta, /):
    if not clientes[id_usuario].contas[id_conta]:
        return None, "Conta inexistente."

    conta = clientes[id_usuario].contas[id_conta]
    resultado, resposta = Deposito(valor).registrar(
        conta=conta,
        id_usuario=id_usuario,
    )

    if resultado:
        return conta, resposta

    return None, resposta


def mostrar_extrato(clientes, /, *, status):
    conta = clientes[status[0]].contas[status[1]]

    if not conta:
        print("Conta inexistente.")
        return

    def extrato_para_texto(conta):
        linhas = []
        saldo = conta.saldo
        logs_ordenados = list(reversed(conta.historico.transacoes))

        linhas.append("EXTRATO")
        linhas.append("")

        encontrou = False

        for item in logs_ordenados:
            if item["evento"] not in ("deposito", "saque"):
                continue

            encontrou = True
            data = item["horario"]
            acao = item["evento"].title()
            status = "OK" if item["status"] else "Falhou"
            valor = float(item["valor"])

            linhas.append(f"{data} | {acao} - R$ {valor:.2f} - {status}")

        if not encontrou:
            linhas.append("Não foram realizadas movimentações.")

        linhas.append("")
        linhas.append(f"Saldo atual: R$ {saldo:.2f}")

        return "\n".join(linhas)

    return extrato_para_texto(conta)


@registrar_log()
def criar_usuario(
    clientes,
    /,
    *,
    nome,
    data_nascimento,
    cpf,
    rua,
    numero,
    bairro,
    cidade,
    estado,
):
    rua = rua.strip() or "Não informado"
    endereco = f"R.{rua}, N°{numero} - {bairro} - {cidade}/{estado}"

    data_validada, data_err = validar_data_nascimento(data_nascimento)
    if data_validada is None:
        return None, data_err

    cpf_do_usuario, cpf_err = validar_cpf(cpf)

    if cpf_do_usuario is None:
        return None, cpf_err

    id_usuario = buscar_usuario(usuarios=clientes, cpf_tratado=cpf_do_usuario)

    if id_usuario is not None:
        return None, f"O CPF {cpf} já está cadastrado."

    usuario = PessoaFisica(
        endereco=endereco,
        nome=nome,
        data_nascimento=data_validada,
        cpf=cpf_do_usuario,
    )

    clientes.append(usuario)

    return clientes[len(clientes) - 1], "Usuario cadastrado com sucesso!"


@registrar_log()
def criar_conta(*, cpf, clientes):
    cpf_do_usuario, cpf_err = validar_cpf(cpf)

    if cpf_do_usuario is None:
        return None, cpf_err

    id_usuario = buscar_usuario(usuarios=clientes, cpf_tratado=cpf_do_usuario)

    if id_usuario is None:
        return (
            None,
            f"O cpf indicado: {cpf}, Não pertence a nenhum usuario cadastrado",
        )

    novo_id = (
        1
        if len(clientes[id_usuario].contas) == 0
        else len(clientes[id_usuario].contas) + 1
    )

    conta = ContaCorrente.nova_conta(
        numero=novo_id,
        cliente=clientes[id_usuario],
    )

    clientes[id_usuario].adicionar_conta(conta)

    return conta, "Conta corrente criada com sucesso!"


def gerar_relatorio(*, logs, id_usuario, id_conta, filtro=None):
    def buscar_log():
        for log in logs:
            mesmo_usuario = log.get("id_usuario") == id_usuario
            mesma_conta = log.get("conta") == id_conta

            if mesmo_usuario and mesma_conta:
                yield log

    def filtrar_relatorio(filtro):
        for log in buscar_log():
            if log.get("evento") in filtro:
                yield log

    if filtro:
        return filtrar_relatorio(filtro)

    return buscar_log()


class ContaIterador:
    def __init__(self, clientes, /, *, id_usuario):
        self.id_usuario = id_usuario
        self.clientes = clientes
        self.nome_usuario = clientes[id_usuario].nome

        self.contas_usuario = clientes[id_usuario].contas

        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.contas_usuario):
            raise StopIteration

        conta = self.contas_usuario[self.index]
        self.index += 1

        return {
            "agencia": conta.agencia,
            "cc": conta.numero,
            "titular": self.nome_usuario,
            "saldo": conta.saldo,
        }
