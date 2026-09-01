# Estrat?gia de Testes, Crit?rios de Aceita??o e Casos de Testes
**Projeto:** EBAC-SHOP (E-commerce)
**Engenheiro de Qualidade:** Leonardo de Almeida

---

## 1. Estrat?gia de Testes

### 1.1 Objetivos da Qualidade
Garantir a confiabilidade, robustez funcional, integridade de contratos de API, usabilidade mobile/web e resili?ncia sob carga do e-commerce EBAC-SHOP, assegurando entregas r?pidas e seguras por meio de uma pir?mide de testes equilibrada e esteira de CI/CD automatizada.

### 1.2 Pap?is e Responsabilidades
- **Engenheiro de Qualidade (QE):** Planejamento da estrat?gia, modelagem de cen?rios BDD/Gherkin, implementa??o dos testes automatizados (UI, API, Mobile, Performance), sustenta??o do pipeline de CI/CD e an?lise de m?tricas de qualidade.
- **Desenvolvedores:** Implementa??o das regras de neg?cio, testes unit?rios, corre??o de bugs apontados e manuten??o de contratos de API.
- **Product Owner (PO):** Refinamento das hist?rias de usu?rio, prioriza??o de backlog e valida??o dos crit?rios de aceita??o.

### 1.3 N?veis e Tipos de Teste
- **Testes de Unidade:** Cobertura de m?todos e valida??es internas de componentes.
- **Testes de Integra??o e Contrato de API:** Valida??o de endpoints `/wc/v3/coupons`, schemas JSON, autentica??o Basic e regras de unicidade via Supertest.
- **Testes de Interface Web (E2E):** Fluxos cr?ticos de carrinho, checkout e autentica??o via Cypress com Page Objects.
- **Testes Mobile:** Valida??o de vitrine e cat?logo de produtos no aplicativo Android via WebdriverIO + Appium.
- **Testes de Performance e Carga:** Simula??o de 20 usu?rios virtuais concorrentes com ramp-up de 20s via K6, avaliando thresholds de p95 < 2s e taxa de erro < 5%.

### 1.4 T?cnicas de Teste Aplicadas
1. **Parti??o de Equival?ncia (EP):** Classes v?lidas e inv?lidas para faixas de desconto e limites de itens.
2. **An?lise do Valor Limite (BVA):** Limites exatos de quantidade de itens (0, 1, 10, 11) e faixas de valores (R$ 199,99, R$ 200,00, R$ 600,00, R$ 600,01, R$ 990,00, R$ 990,01).
3. **Tabela de Decis?o:** Combina??es de autentica??o, status do usu?rio (ativo/inativo) e tentativas incorretas (bloqueio tempor?rio).
4. **Transi??o de Estados:** Ciclo de vida do carrinho de compras e status de sess?o de usu?rio.

---

## 2. Hist?rias de Usu?rio e Crit?rios de Aceita??o (Gherkin)

### [US-0001] ? Adicionar item ao carrinho
**Como** cliente da EBAC-SHOP  
**Quero** adicionar produtos no carrinho  
**Para** realizar a compra dos itens  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0001] Adicionar item ao carrinho

  Contexto:
    Dado que o cliente acessa a vitrine de produtos da EBAC-SHOP

  Cen?rio: Adicionar at? 10 unidades de um mesmo produto com sucesso (Caminho Feliz)
    Quando o cliente seleciona o produto "Ingrid Running Jacket"
    E define a quantidade de "10" itens
    E clica em "Adicionar ao Carrinho"
    Ent?o o produto deve ser inclu?do no carrinho com a quantidade "10"
    E o subtotal do carrinho deve ser atualizado corretamente

  Cen?rio: Tentativa de adicionar mais de 10 itens do mesmo produto (Caminho Negativo)
    Quando o cliente seleciona o produto "Ingrid Running Jacket"
    E tenta definir a quantidade de "11" itens
    E clica em "Adicionar ao Carrinho"
    Ent?o o sistema deve bloquear a a??o
    E exibir a mensagem de alerta "N?o ? permitido inserir mais de 10 itens de um mesmo produto ao carrinho"

  Cen?rio: Bloqueio de compra com valor total superior a R$ 990,00 (Valor Limite / Negativo)
    Quando o cliente possui itens no carrinho totalizando R$ 995,00
    E tenta avan?ar para a finaliza??o da compra
    Ent?o o sistema deve impedir o avan?o para o checkout
    E exibir a mensagem "O valor total da compra n?o pode ultrapassar R$ 990,00"

  Cen?rio: Aplica??o autom?tica de cupom de 10% para compras entre R$ 200,00 e R$ 600,00 (Tabela de Decis?o)
    Quando o cliente adiciona itens cujo subtotal resulta em R$ 400,00
    E visualiza a p?gina do carrinho
    Ent?o o sistema deve aplicar automaticamente o desconto de 10% (R$ 40,00)
    E o valor final a pagar deve ser R$ 360,00

  Cen?rio: Aplica??o autom?tica de cupom de 15% para compras acima de R$ 600,00 (Tabela de Decis?o)
    Quando o cliente adiciona itens cujo subtotal resulta em R$ 800,00
    E visualiza a p?gina do carrinho
    Ent?o o sistema deve aplicar automaticamente o desconto de 15% (R$ 120,00)
    E o valor final a pagar deve ser R$ 680,00
```

---

### [US-0002] ? Login na plataforma
**Como** cliente da EBAC-SHOP  
**Quero** fazer o login (autentica??o) na plataforma  
**Para** visualizar meus pedidos  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0002] Login na plataforma

  Contexto:
    Dado que o usu?rio est? na p?gina "Minha Conta" da EBAC-SHOP

  Cen?rio: Autentica??o de usu?rio ativo com credenciais v?lidas (Caminho Feliz)
    Quando o usu?rio informa o e-mail "cliente_ativo@ebac.com.br"
    E informa a senha v?lida "Teste@123"
    E clica no bot?o "LOGIN"
    Ent?o o usu?rio deve ser autenticado com sucesso
    E deve ser redirecionado para o painel da Minha Conta

  Cen?rio: Tentativa de login com usu?rio inativo (Caminho Alternativo)
    Quando o usu?rio informa o e-mail "cliente_inativo@ebac.com.br"
    E informa a senha "Teste@123"
    E clica no bot?o "LOGIN"
    Ent?o o sistema deve impedir o acesso
    E exibir a mensagem "Esta conta de usu?rio est? inativa. Entre em contato com o suporte."

  Cen?rio: Exibi??o de erro com senha ou usu?rio incorreto (Caminho Negativo)
    Quando o usu?rio informa o e-mail "cliente_ativo@ebac.com.br"
    E informa uma senha incorreta "SenhaErrada123"
    E clica no bot?o "LOGIN"
    Ent?o o sistema deve exibir a mensagem de erro "Nome de usu?rio ou senha incorretos."

  Cen?rio: Bloqueio de login por 15 minutos ap?s 3 falhas consecutivas de senha (Transi??o de Estados)
    Dado que o usu?rio errou a senha 2 vezes consecutivas
    Quando o usu?rio insere a senha incorreta pela 3? vez
    E clica no bot?o "LOGIN"
    Ent?o o acesso da conta deve ser temporariamente bloqueado por 15 minutos
    E deve exibir o aviso "Muitas tentativas de login incorretas. Conta bloqueada por 15 minutos."
```

---

### [US-0003] ? API de cupons
**Como** admin da EBAC-SHOP  
**Quero** criar um servi?o de cupom  
**Para** poder listar e cadastrar os cupons  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0003] API de cupons

  Contexto:
    Dado que o cliente autentica na API com Basic Auth "admin_ebac:@admin!&b@c!2022"
    E o cabe?alho "Content-Type" est? definido como "application/json"

  Cen?rio: Listar todos os cupons cadastrados com sucesso (Caminho Feliz - GET)
    Quando enviar uma requisi??o GET para o endpoint "/wc/v3/coupons"
    Ent?o o status code da resposta deve ser 200 OK
    E o corpo da resposta deve conter um array com a lista de cupons cadastrados
    E o contrato da resposta deve respeitar o JSON Schema definido

  Cen?rio: Buscar cupom por ID existente (Caminho Feliz - GET por ID)
    Quando enviar uma requisi??o GET para "/wc/v3/coupons/1234"
    Ent?o o status code da resposta deve ser 200 OK
    E a resposta deve conter os dados detalhados do cupom com id 1234

  Cen?rio: Cadastrar novo cupom com campos obrigat?rios v?lidos (Caminho Feliz - POST)
    Quando enviar uma requisi??o POST para "/wc/v3/coupons" com o payload:
      """
      {
        "code": "Ganhe10",
        "amount": "10.00",
        "discount_type": "fixed_product",
        "description": "Cupom de teste"
      }
      """
    Ent?o o status code da resposta deve ser 201 Created
    E o corpo da resposta deve conter o id gerado e o c?digo "Ganhe10"

  Cen?rio: Impedir cadastro de cupom com c?digo duplicado (Caminho Negativo - POST)
    Dado que j? existe um cupom cadastrado com o c?digo "Ganhe10"
    Quando tentar cadastrar um novo cupom com o mesmo c?digo "Ganhe10"
    Ent?o o status code da resposta deve ser 400 Bad Request
    E a mensagem de erro deve indicar que o c?digo do cupom j? existe

  Cen?rio: Tentativa de cadastro sem campos obrigat?rios (Caminho Negativo - POST)
    Quando enviar uma requisi??o POST para "/wc/v3/coupons" sem o campo obrigat?rio "code"
    Ent?o o status code da resposta deve ser 400 Bad Request
    E o corpo da resposta deve informar que o campo "code" ? obrigat?rio
```

---

### [US-0004] ? Cat?logo de Produtos
**Como** cliente da EBAC-SHOP  
**Quero** navegar pelo cat?logo de produtos e aplicar filtros/busca  
**Para** encontrar os itens que desejo comprar com rapidez  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0004] Cat?logo de Produtos

  Contexto:
    Dado que o usu?rio acessa a p?gina inicial do cat?logo de produtos

  Cen?rio: Busca de produto por palavra-chave v?lida (Caminho Feliz)
    Quando o usu?rio digita "Jacket" na barra de busca e clica em pesquisar
    Ent?o o cat?logo deve exibir apenas produtos correspondentes ao termo "Jacket"

  Cen?rio: Filtragem por categoria de produto (Caminho Feliz)
    Quando o usu?rio seleciona a categoria "Roupas Masculinas"
    Ent?o o cat?logo deve atualizar exibindo somente os itens pertencentes a essa categoria

  Cen?rio: Ordena??o de produtos por pre?o crescente (Caminho Alternativo)
    Quando o usu?rio seleciona a ordena??o "Ordenar por pre?o: menor para maior"
    Ent?o os produtos devem ser reorganizados do menor valor para o maior valor

  Cen?rio: Busca por produto inexistente (Caminho Negativo)
    Quando o usu?rio pesquisa pelo termo "ProdutoInexistenteXYZ123"
    Ent?o o cat?logo deve exibir a mensagem "Nenhum produto foi encontrado correspondente ? sua sele??o."
```

---

### [US-0005] ? Painel Minha Conta
**Como** cliente autenticado da EBAC-SHOP  
**Quero** acessar o painel principal da Minha Conta  
**Para** visualizar o resumo da minha atividade e atalhos r?pidos  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0005] Painel Minha Conta

  Contexto:
    Dado que o cliente est? autenticado na plataforma

  Cen?rio: Acesso ao Dashboard da conta (Caminho Feliz)
    Quando o cliente clica em "Minha Conta"
    Ent?o deve visualizar a mensagem de boas-vindas personalizada com seu nome
    E deve visualizar os atalhos para "Painel", "Pedidos", "Endere?os", "Detalhes da Conta" e "Sair"

  Cen?rio: Logout seguro da conta (Caminho Alternativo)
    Quando o cliente clica na op??o "Sair" do painel
    Ent?o a sess?o atual deve ser encerrada
    E o usu?rio deve ser redirecionado para a tela de login

  Cen?rio: Tentativa de acesso ao painel sem autentica??o (Caminho Negativo)
    Dado que o usu?rio n?o est? autenticado
    Quando tenta acessar a URL direta "/minha-conta"
    Ent?o o sistema deve exibir os formul?rios de Login e Registro ao inv?s do dashboard

  Cen?rio: Persist?ncia de sess?o com a op??o "Lembrar-me" marcada (Caminho Alternativo)
    Quando o usu?rio faz login marcando a op??o "Lembrar-me"
    E fecha e reabre o navegador
    Ent?o o usu?rio deve permanecer autenticado no painel
```

---

### [US-0006] ? Meus Pedidos
**Como** cliente da EBAC-SHOP  
**Quero** consultar a lista e os detalhes dos meus pedidos anteriores  
**Para** acompanhar o status de entrega e hist?rico de compras  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0006] Meus Pedidos

  Contexto:
    Dado que o cliente est? autenticado na se??o "Minha Conta > Pedidos"

  Cen?rio: Visualiza??o do hist?rico de pedidos (Caminho Feliz)
    Dado que o cliente possui pedidos realizados anteriormente
    Quando o cliente acessa a aba "Pedidos"
    Ent?o deve visualizar a tabela com colunas "Pedido", "Data", "Status", "Total" e "A??es"

  Cen?rio: Visualiza??o detalhada de um pedido espec?fico (Caminho Feliz)
    Quando o cliente clica no bot?o "Visualizar" de um pedido com status "Processando"
    Ent?o o sistema deve exibir a p?gina de detalhes com itens comprados, endere?o de entrega e m?todo de pagamento

  Cen?rio: Cliente sem nenhum hist?rico de compras (Caminho Alternativo)
    Dado que o cliente acabou de se cadastrar e n?o possui pedidos
    Quando o cliente acessa a aba "Pedidos"
    Ent?o deve ser exibida a mensagem "Nenhum pedido foi feito ainda." juntamente ao bot?o "Ir para a loja"

  Cen?rio: Tentativa de acessar detalhes de pedido pertencente a outro cliente (Caminho Negativo / Seguran?a)
    Quando o cliente tenta acessar a URL de um pedido com ID de outro usu?rio
    Ent?o o sistema deve negar o acesso exibindo status 403 / "Voc? n?o tem permiss?o para visualizar este pedido"
```

---

### [US-0007] ? Endere?os
**Como** cliente da EBAC-SHOP  
**Quero** cadastrar e atualizar meus endere?os de cobran?a e entrega  
**Para** agilizar o processo de checkout em compras futuras  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0007] Endere?os

  Contexto:
    Dado que o cliente autenticado acessa a aba "Endere?os"

  Cen?rio: Atualizar endere?o de faturamento com sucesso (Caminho Feliz)
    Quando o cliente clica em "Editar" no Endere?o de Faturamento
    E preenche todos os campos obrigat?rios com dados v?lidos (Nome, Sobrenome, CEP, Rua, Cidade, Estado)
    E clica em "Salvar Endere?o"
    Ent?o o sistema deve salvar as altera??es
    E exibir a mensagem "Endere?o alterado com sucesso."

  Cen?rio: Tentativa de salvar endere?o com CEP em formato inv?lido (Caminho Negativo)
    Quando o cliente insere o CEP "1234" (formato incompleto)
    E tenta salvar o endere?o
    Ent?o o sistema deve exibir mensagem de erro "Por favor, insira um CEP v?lido."

  Cen?rio: Omiss?o de campo obrigat?rio no cadastro de endere?o (Caminho Negativo)
    Quando o cliente deixa o campo "Cidade" em branco
    E tenta salvar as altera??es
    Ent?o o sistema deve destacar o campo "Cidade" e impedir o envio

  Cen?rio: Manter endere?os distintos para cobran?a e entrega (Caminho Alternativo)
    Quando o cliente cadastra um endere?o para Cobran?a e outro diferente para Entrega
    Ent?o ambos os endere?os devem ser persistidos e exibidos separadamente na ?rea de endere?os
```

---

### [US-0008] ? Detalhes da Conta
**Como** cliente da EBAC-SHOP  
**Quero** gerenciar meus dados pessoais e alterar minha senha de acesso  
**Para** manter minha conta segura e com informa??es atualizadas  

#### Crit?rios de Aceita??o (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0008] Detalhes da Conta

  Contexto:
    Dado que o cliente autenticado acessa a aba "Detalhes da Conta"

  Cen?rio: Altera??o do nome de exibi??o com sucesso (Caminho Feliz)
    Quando o cliente altera o campo "Nome de Exibi??o" para "Leonardo QA"
    E clica em "Salvar Altera??es"
    Ent?o o sistema deve exibir a notifica??o "Detalhes da conta modificados com sucesso."

  Cen?rio: Altera??o de senha com credenciais v?lidas (Caminho Feliz)
    Quando o cliente informa a "Senha atual" correta
    E informa uma "Nova senha" forte e a repete em "Confirmar nova senha"
    E clica em "Salvar Altera??es"
    Ent?o a nova senha deve ser salva e o usu?rio mantido autenticado

  Cen?rio: Tentativa de altera??o de senha com senha atual incorreta (Caminho Negativo)
    Quando o cliente preenche a "Senha atual" com valor incorreto
    E submete o formul?rio de altera??o de senha
    Ent?o o sistema deve rejeitar a solicita??o com a mensagem "Sua senha atual est? incorreta."

  Cen?rio: Diverg?ncia entre nova senha e confirma??o de senha (Caminho Negativo)
    Quando o cliente digita "NovaSenha@123" e em confirma??o digita "OutraSenha@456"
    E tenta salvar
    Ent?o o sistema deve acusar "As novas senhas n?o coincidem."
```

---

## 3. Matriz de Casos de Teste (Detalhamento T?cnico)

| ID | Hist?ria | Cen?rio / Descri??o | Tipo | T?cnica Aplicada | Automa??o? |
|---|---|---|---|---|---|
| **TC-001** | US-0001 | Adicionar 10 itens de um mesmo produto | Caminho Feliz | Valor Limite (BVA) | **Sim (UI)** |
| **TC-002** | US-0001 | Tentar adicionar 11 itens de um mesmo produto | Caminho Negativo | Valor Limite (BVA) | **Sim (UI)** |
| **TC-003** | US-0001 | Bloquear checkout com valor total > R$ 990,00 | Caminho Negativo | Parti??o de Equival?ncia (EP) | **Sim (UI)** |
| **TC-004** | US-0001 | Aplicar cupom 10% para compras entre R$ 200 e R$ 600 | Caminho Alternativo | Tabela de Decis?o | **Sim (UI)** |
| **TC-005** | US-0001 | Aplicar cupom 15% para compras > R$ 600 | Caminho Alternativo | Tabela de Decis?o | N?o (Manual) |
| **TC-006** | US-0002 | Login com sucesso para usu?rio ativo | Caminho Feliz | Tabela de Decis?o | **Sim (UI / K6)** |
| **TC-007** | US-0002 | Login com senha incorreta | Caminho Negativo | Parti??o de Equival?ncia | **Sim (UI)** |
| **TC-008** | US-0002 | Bloqueio de conta por 15 min ap?s 3 erros de senha | Caminho Alternativo | Transi??o de Estados | **Sim (UI)** |
| **TC-009** | US-0002 | Login com usu?rio inativo | Caminho Negativo | Tabela de Decis?o | N?o (Manual) |
| **TC-010** | US-0003 | Listar todos os cupons via GET com Basic Auth | Caminho Feliz | Teste de Contrato | **Sim (API Supertest)** |
| **TC-011** | US-0003 | Consultar cupom por ID existente | Caminho Feliz | Parti??o de Equival?ncia | **Sim (API Supertest)** |
| **TC-012** | US-0003 | Cadastrar cupom v?lido com campos obrigat?rios | Caminho Feliz | Parti??o de Equival?ncia | **Sim (API Supertest)** |
| **TC-013** | US-0003 | Tentar cadastrar cupom com c?digo j? existente | Caminho Negativo | Tabela de Decis?o | **Sim (API Supertest)** |
| **TC-014** | US-0003 | Tentar cadastrar cupom sem campo obrigat?rio | Caminho Negativo | Valor Limite / Schema | **Sim (API Supertest)** |
| **TC-015** | US-0004 | Buscar produto por palavra-chave na vitrine Mobile | Caminho Feliz | Parti??o de Equival?ncia | **Sim (Mobile)** |
| **TC-016** | US-0004 | Filtrar produtos por categoria no cat?logo Mobile | Caminho Alternativo | Parti??o de Equival?ncia | **Sim (Mobile)** |
| **TC-017** | US-0004 | Ordenar cat?logo por menor pre?o | Caminho Alternativo | Caixa-Preta | N?o (Manual) |
| **TC-018** | US-0004 | Busca por produto inexistente | Caminho Negativo | Parti??o de Equival?ncia | N?o (Manual) |
| **TC-019** | US-0005 | Visualizar dashboard Minha Conta com sucesso | Caminho Feliz | Caixa-Preta | N?o (Manual) |
| **TC-020** | US-0005 | Efetuar logout e invalidar sess?o | Caminho Alternativo | Transi??o de Estados | N?o (Manual) |
| **TC-021** | US-0006 | Consultar lista e status de pedidos anteriores | Caminho Feliz | Caixa-Preta | N?o (Manual) |
| **TC-022** | US-0007 | Atualizar endere?o de faturamento com sucesso | Caminho Feliz | Parti??o de Equival?ncia | N?o (Manual) |
| **TC-023** | US-0008 | Alterar senha da conta com valida??o da senha atual | Caminho Feliz | Tabela de Decis?o | N?o (Manual) |
| **TC-024** | US-0008 | Tentar alterar senha com senha atual incorreta | Caminho Negativo | Tabela de Decis?o | N?o (Manual) |
