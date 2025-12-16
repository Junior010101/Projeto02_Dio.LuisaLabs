from abc import ABC, abstractmethod
from datetime import datetime as date

from python.utils import buscar_log, salvar_log


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realisar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, nome, data_nascimento, cpf):
        super().__init__(endereco)

        self.nome = nome
        self.data_nascimento = data_nascimento
        self._cpf = cpf
        self._endereco = endereco

    def __str__(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
        }

    @property
    def endereco(self):
        return self._endereco

    @property
    def cpf(self):
        return self._cpf

    @property
    def contas(self):
        return self._contas


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico(conta=self.numero)

    @classmethod
    def nova_conta(cls, *, cliente, numero):
        return cls(numero=numero, cliente=cliente)

    def __str__(self):
        return (
            f"Agência: {self.agencia} | "
            f"Conta: {self.numero} | "
            f"Saldo: {self.saldo}"
        )

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, *, valor):
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            return False, "Operação falhou! Você não tem saldo suficiente."
        if valor <= 0:
            return False, "Operação falhou! O valor informado é inválido."

        self.saldo -= valor

        return True, f"Saque de: R$ {valor:.2f}, feito com sucesso!"

    def depositar(self, *, valor):
        if valor <= 0:
            return False, "Operação falhou! O valor informado é inválido."

        self.saldo += valor

        return True, f"Depósito de: R$ {valor:.2f}, feito com sucesso!"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)

        self.limite = limite
        self.limite_saques = limite_saques
        self._numero_saques = 0

    @property
    def numero_saques(self):
        return self._numero_saques

    @numero_saques.setter
    def numero_saques(self, valor):
        self._numero_saques = valor

    def sacar(self, *, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_limite:
            return False, "Operação falhou! O valor do saque excede o limite."
        if excedeu_saques:
            return False, "Operação falhou! Número máximo de saques excedido."

        self.numero_saques += 1
        return super().sacar(valor=valor)


class Historico:
    def __init__(self, conta):
        self._conta = conta

    @property
    def transacoes(self):
        registros = buscar_log()
        transacoes = []

        for data in registros.values():
            mesma_conta = data.get("conta") == self._conta

            if mesma_conta:
                transacoes.append(data)

        return transacoes

    def adicionar_transacao(self, *, evento, valor, status, cliente):
        registros = buscar_log()

        novo_id = max(registros.keys(), default=0) + 1

        registros[novo_id] = {
            "horario": date.now().strftime("%d-%m-%Y %H:%M:%S"),
            "evento": evento,
            "id_usuario": cliente,
            "conta": self._conta,
            "valor": valor,
            "status": status,
        }

        salvar_log(registros)


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta, id_usuario):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta, id_usuario):
        resultado, resposta = conta.sacar(valor=self.valor)

        conta.historico.adicionar_transacao(
            evento=self.__class__.__name__.lower(),
            valor=self.valor,
            status=resultado,
            cliente=id_usuario,
        )

        if resultado:
            return resultado, resposta

        return None, resposta


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, *, conta, id_usuario):
        resultado, resposta = conta.depositar(valor=self.valor)

        conta.historico.adicionar_transacao(
            evento=self.__class__.__name__.lower(),
            valor=self.valor,
            status=resultado,
            cliente=id_usuario,
        )

        if resultado:
            return resultado, resposta

        return None, resposta
