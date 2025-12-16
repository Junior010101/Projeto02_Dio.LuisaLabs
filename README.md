<h1>
  <table>
    <tr>
      <td>
        <img src="https://assets.dio.me/Xl98YWbvhhAF2MJhHva1jjFf-NNKiYP86uVUHeJpj6U/f:webp/h:120/q:80/L3RyYWNrcy84MmI1NWE0OC1kOTlmLTRjZDItYjJhMC1hNjc0N2JkYjM5YzUucG5n" height="120">
      </td>
      <td width="700">
        <p>Luizalabs - Back-end com Python</p>
      </td>
    </tr>
  </table>
</h1>

[![Python](https://img.shields.io/badge/Python-3.12-yellow)](https://docs.python.org/3.12/)
[![DIO.](https://img.shields.io/badge/DIO.-LuisaLabs-blue)](https://web.dio.me/track/luizalabs-back-end-com-python)

```mermaid
---
config:
  theme: redux
  layout: elk
---
flowchart TB
    A(["Inicio"]) --> B{"mostrar_menu(1)"}
    B --> C["[c] Cadastro"] & D["[a] Acessar/Criar Conta"] & n1["[d] Depositar"] & n2["[s] Sacar"] & n3["[e] Extrato"] & n5["[q] Sair"]
    C --> n6["criar_usuario()"]
    n6 --> n7["Valida data"]
    n7 --> n39["Data valida?"]
    n8["validar_cpf()"] --> n35["CPF é valido?"]
    n9["buscar_usuario()"] --> n43["Usuario encontrado?"]
    D --> n11["mostrar_menu(2)"]
    n11 --> n12["[s] fazer login"] & n13["[n] criar conta"]
    n15["validar_cpf()"] --> n47["CPF é valido?"]
    n16["buscar_usuario()"] --> n51["Usuario encontrado?"]
    n17["print(Contas encontradas:)"] --> n18["input(digite o numero da conta que quer acessar:)"]
    n18 --> n19["return status[]"]
    n13 --> n20["criar_conta()"]
    n12 --> n15
    n20 --> n21["validar_cpf()"]
    n21 --> n55@{ label: "<span style=\"padding-left:\">CPF é valido?</span>" }
    n22["buscar_usuario()"] --> n59@{ label: "<span style=\"padding-left:\">Usuario encontrado?</span>" }
    n1 --> n24["status[1] is not None"]
    n24 --> n25["input(digite o valor:)"]
    n25 --> n63["Valor valido?"]
    n26["deposito()"] --> n27["return saldo, extrato"]
    n2 --> n28["status[1] is not None"]
    n28 --> n29["input(digite o valor:)"]
    n29 --> n67["Valor valido?"]
    n30["saque()"] --> n31["return saldo, extrato"]
    n3 --> n32["status[1] is not None"]
    n32 --> n33["mostrar_extrato()"]
    n5 --> n34["break"]
    n35 --> n36["Sim"] & n37["Não"]
    n36 --> n9
    n37 --> n38["return None, mensagem"]
    n39 --> n40["Sim"] & n41["Não"]
    n40 --> n8
    n41 --> n42@{ label: "<span style=\"padding-left:\">return None, mensagem</span>" }
    n43 --> n44["Sim"] & n45["Não"]
    n44 --> n10["return usuario[]"]
    n45 --> n46@{ label: "<span style=\"padding-left:\">return None, mensagem</span>" }
    n47 --> n48["Sim"] & n49["Não"]
    n48 --> n16
    n49 --> n50@{ label: "<span style=\"padding-left:\">return None, mensagem</span>" }
    n51 --> n52["Sim"] & n53["Não"]
    n52 --> n17
    n53 --> n54@{ label: "<span style=\"padding-left:\">return None, mensagem</span>" }
    n55 --> n56@{ label: "<span style=\"padding-left:\">Sim</span>" } & n57@{ label: "<span style=\"padding-left:\">Não</span>" }
    n56 --> n22
    n57 --> n58@{ label: "<span style=\"padding-left:\"><span style=\"padding-left:\">return None, mensagem</span></span>" }
    n59 --> n60@{ label: "<span style=\"padding-left:\">Sim</span>" } & n61@{ label: "<span style=\"padding-left:\">Não</span>" }
    n60 --> n23["return conta[]"]
    n61 --> n62@{ label: "<span style=\"padding-left:\"><span style=\"padding-left:\">return None, mensagem</span></span>" }
    n63 --> n64["Sim"] & n65["Não"]
    n64 --> n26
    n65 --> n66["return None, mensagem"]
    n67 --> n68["Sim"] & n69["Não"]
    n68 --> n30
    n69 --> n70@{ label: "<span style=\"padding-left:\">return None, mensagem</span>" }
    n33 --> n71["return extrato[]"]

    n1@{ shape: rect}
    n6@{ shape: lean-l}
    n7@{ shape: rect}
    n39@{ shape: diam}
    n8@{ shape: lean-l}
    n35@{ shape: diam}
    n9@{ shape: lean-l}
    n43@{ shape: diam}
    n11@{ shape: diam}
    n15@{ shape: lean-l}
    n47@{ shape: diam}
    n16@{ shape: lean-l}
    n51@{ shape: diam}
    n19@{ shape: lean-r}
    n20@{ shape: lean-l}
    n21@{ shape: lean-l}
    n55@{ shape: diam}
    n22@{ shape: lean-l}
    n59@{ shape: diam}
    n25@{ shape: lean-l}
    n63@{ shape: diam}
    n26@{ shape: lean-l}
    n27@{ shape: lean-r}
    n67@{ shape: diam}
    n30@{ shape: lean-l}
    n31@{ shape: lean-r}
    n33@{ shape: lean-l}
    n38@{ shape: lean-r}
    n42@{ shape: lean-r}
    n10@{ shape: lean-r}
    n46@{ shape: lean-r}
    n50@{ shape: lean-r}
    n54@{ shape: lean-r}
    n56@{ shape: rect}
    n57@{ shape: rect}
    n58@{ shape: lean-r}
    n60@{ shape: rect}
    n61@{ shape: rect}
    n23@{ shape: lean-r}
    n62@{ shape: lean-r}
    n66@{ shape: lean-r}
    n70@{ shape: lean-r}
    n71@{ shape: lean-r}
```

## Instalação e Execução

### Requisitos
- Python 3.12+
- Ambiente de terminal (Linux, macOS ou Windows)

### Passos
```bash
git clone https://github.com/Junior010101/Projeto01_Dio.LuisaLabs
cd Projeto01_Dio.LuisaLabs
python main.py
```

## Estrutura do Projeto

```
root/
  python/
    funcoes.py       # Depósitos, saques, extratos, cadastro, criação de contas.
    utils.py         # listagem, validação, busca de usuários, Validação de CPF.
  main.py            # Loop principal e menu.
```

---

## Regras de Negócio

### Usuários
- CPF único por usuário
- Data de nascimento validada (DD/MM/AAAA)
- Usuário pode ter múltiplas contas

### Contas
- Conta vinculada a um usuário já cadastrado
- Número da conta gerado automaticamente
- Um usuario pode criar varias contas

## Operações

**Depósito**
- Apenas valores positivos
- Registrado no extrato

**Saque**
- Limite configurado no código
- Número máximo de saques
- Recusado se o saldo for insuficiente

**Extrato**
- Lista todas as operações
- Mostra saldo atual

---
**Desenvolvido por [Junior010101](https://github.com/Junior010101)**
