# Estratégia de Testes, Critérios de Aceitação e Casos de Testes
**Projeto:** EBAC-SHOP (E-commerce)
**Engenheiro de Qualidade:** Leonardo de Almeida

---

## 1. Estratégia de Testes

### 1.1 Objetivos da Qualidade
Garantir a confiabilidade, robustez funcional, integridade de contratos de API, usabilidade mobile/web e resiliência sob carga do e-commerce EBAC-SHOP, assegurando entregas rápidas e seguras por meio de uma pirâmide de testes equilibrada e esteira de CI/CD automatizada.

### 1.2 Papéis e Responsabilidades
- **Engenheiro de Qualidade (QE):** Planejamento da estratégia, modelagem de cenários BDD/Gherkin, implementação dos testes automatizados (UI, API, Mobile, Performance), sustentação do pipeline de CI/CD e análise de métricas de qualidade.
- **Desenvolvedores:** Implementação das regras de negócio, testes unitários, correção de bugs apontados e manutenção de contratos de API.
- **Product Owner (PO):** Refinamento das histórias de usuário, priorização de backlog e validação dos critérios de aceitação.

### 1.3 Níveis e Tipos de Teste
- **Testes de Unidade:** Cobertura de métodos e validações internas de componentes.
- **Testes de Integração e Contrato de API:** Validação de endpoints `/wc/v3/coupons`, schemas JSON, autenticação Basic e regras de unicidade via Supertest.
- **Testes de Interface Web (E2E):** Fluxos críticos de carrinho, checkout e autenticação via Cypress com Page Objects.
- **Testes Mobile:** Validação de vitrine e catálogo de produtos no aplicativo Android via WebdriverIO + Appium.
- **Testes de Performance e Carga:** Simulação de 20 usuários virtuais concorrentes com ramp-up de 20s via K6, avaliando thresholds de p95 < 2s e taxa de erro < 5%.

### 1.4 Técnicas de Teste Aplicadas
1. **Partição de Equivalência (EP):** Classes válidas e inválidas para faixas de desconto e limites de itens.
2. **Análise do Valor Limite (BVA):** Limites exatos de quantidade de itens (0, 1, 10, 11) e faixas de valores (R$ 199,99, R$ 200,00, R$ 600,00, R$ 600,01, R$ 990,00, R$ 990,01).
3. **Tabela de Decisão:** Combinações de autenticação, status do usuário (ativo/inativo) e tentativas incorretas (bloqueio temporário).
4. **Transição de Estados:** Ciclo de vida do carrinho de compras e status de sessão de usuário.

---

## 2. Histórias de Usuário e Critérios de Aceitação (Gherkin)

### [US-0001] é Adicionar item ao carrinho
**Como** cliente da EBAC-SHOP  
**Quero** adicionar produtos no carrinho  
**Para** realizar a compra dos itens  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0001] Adicionar item ao carrinho

  Contexto:
    Dado que o cliente acessa a vitrine de produtos da EBAC-SHOP

  Cenário: Adicionar até 10 unidades de um mesmo produto com sucesso (Caminho Feliz)
    Quando o cliente seleciona o produto "Ingrid Running Jacket"
    E define a quantidade de "10" itens
    E clica em "Adicionar ao Carrinho"
    Então o produto deve ser incluído no carrinho com a quantidade "10"
    E o subtotal do carrinho deve ser atualizado corretamente

  Cenário: Tentativa de adicionar mais de 10 itens do mesmo produto (Caminho Negativo)
    Quando o cliente seleciona o produto "Ingrid Running Jacket"
    E tenta definir a quantidade de "11" itens
    E clica em "Adicionar ao Carrinho"
    Então o sistema deve bloquear a ação
    E exibir a mensagem de alerta "Não é permitido inserir mais de 10 itens de um mesmo produto ao carrinho"

  Cenário: Bloqueio de compra com valor total superior a R$ 990,00 (Valor Limite / Negativo)
    Quando o cliente possui itens no carrinho totalizando R$ 995,00
    E tenta avançar para a finalização da compra
    Então o sistema deve impedir o avanço para o checkout
    E exibir a mensagem "O valor total da compra não pode ultrapassar R$ 990,00"

  Cenário: Aplicação automática de cupom de 10% para compras entre R$ 200,00 e R$ 600,00 (Tabela de Decisão)
    Quando o cliente adiciona itens cujo subtotal resulta em R$ 400,00
    E visualiza a página do carrinho
    Então o sistema deve aplicar automaticamente o desconto de 10% (R$ 40,00)
    E o valor final a pagar deve ser R$ 360,00

  Cenário: Aplicação automática de cupom de 15% para compras acima de R$ 600,00 (Tabela de Decisão)
    Quando o cliente adiciona itens cujo subtotal resulta em R$ 800,00
    E visualiza a página do carrinho
    Então o sistema deve aplicar automaticamente o desconto de 15% (R$ 120,00)
    E o valor final a pagar deve ser R$ 680,00
```

---

### [US-0002] é Login na plataforma
**Como** cliente da EBAC-SHOP  
**Quero** fazer o login (autenticação) na plataforma  
**Para** visualizar meus pedidos  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0002] Login na plataforma

  Contexto:
    Dado que o usuário está na página "Minha Conta" da EBAC-SHOP

  Cenário: Autenticação de usuário ativo com credenciais válidas (Caminho Feliz)
    Quando o usuário informa o e-mail "cliente_ativo@ebac.com.br"
    E informa a senha válida "Teste@123"
    E clica no botão "LOGIN"
    Então o usuário deve ser autenticado com sucesso
    E deve ser redirecionado para o painel da Minha Conta

  Cenário: Tentativa de login com usuário inativo (Caminho Alternativo)
    Quando o usuário informa o e-mail "cliente_inativo@ebac.com.br"
    E informa a senha "Teste@123"
    E clica no botão "LOGIN"
    Então o sistema deve impedir o acesso
    E exibir a mensagem "Esta conta de usuário está inativa. Entre em contato com o suporte."

  Cenário: Exibição de erro com senha ou usuário incorreto (Caminho Negativo)
    Quando o usuário informa o e-mail "cliente_ativo@ebac.com.br"
    E informa uma senha incorreta "SenhaErrada123"
    E clica no botão "LOGIN"
    Então o sistema deve exibir a mensagem de erro "Nome de usuário ou senha incorretos."

  Cenário: Bloqueio de login por 15 minutos após 3 falhas consecutivas de senha (Transição de Estados)
    Dado que o usuário errou a senha 2 vezes consecutivas
    Quando o usuário insere a senha incorreta pela 3ª vez
    E clica no botão "LOGIN"
    Então o acesso da conta deve ser temporariamente bloqueado por 15 minutos
    E deve exibir o aviso "Muitas tentativas de login incorretas. Conta bloqueada por 15 minutos."
```

---

### [US-0003] é API de cupons
**Como** admin da EBAC-SHOP  
**Quero** criar um serviço de cupom  
**Para** poder listar e cadastrar os cupons  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0003] API de cupons

  Contexto:
    Dado que o cliente autentica na API com Basic Auth "admin_ebac:@admin!&b@c!2022"
    E o cabeçalho "Content-Type" está definido como "application/json"

  Cenário: Listar todos os cupons cadastrados com sucesso (Caminho Feliz - GET)
    Quando enviar uma requisição GET para o endpoint "/wc/v3/coupons"
    Então o status code da resposta deve ser 200 OK
    E o corpo da resposta deve conter um array com a lista de cupons cadastrados
    E o contrato da resposta deve respeitar o JSON Schema definido

  Cenário: Buscar cupom por ID existente (Caminho Feliz - GET por ID)
    Quando enviar uma requisição GET para "/wc/v3/coupons/1234"
    Então o status code da resposta deve ser 200 OK
    E a resposta deve conter os dados detalhados do cupom com id 1234

  Cenário: Cadastrar novo cupom com campos obrigatórios válidos (Caminho Feliz - POST)
    Quando enviar uma requisição POST para "/wc/v3/coupons" com o payload:
      """
      {
        "code": "Ganhe10",
        "amount": "10.00",
        "discount_type": "fixed_product",
        "description": "Cupom de teste"
      }
      """
    Então o status code da resposta deve ser 201 Created
    E o corpo da resposta deve conter o id gerado e o código "Ganhe10"

  Cenário: Impedir cadastro de cupom com código duplicado (Caminho Negativo - POST)
    Dado que já existe um cupom cadastrado com o código "Ganhe10"
    Quando tentar cadastrar um novo cupom com o mesmo código "Ganhe10"
    Então o status code da resposta deve ser 400 Bad Request
    E a mensagem de erro deve indicar que o código do cupom já existe

  Cenário: Tentativa de cadastro sem campos obrigatórios (Caminho Negativo - POST)
    Quando enviar uma requisição POST para "/wc/v3/coupons" sem o campo obrigatório "code"
    Então o status code da resposta deve ser 400 Bad Request
    E o corpo da resposta deve informar que o campo "code" é obrigatório
```

---

### [US-0004] é Catélogo de Produtos
**Como** cliente da EBAC-SHOP  
**Quero** navegar pelo catálogo de produtos e aplicar filtros/busca  
**Para** encontrar os itens que desejo comprar com rapidez  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0004] Catélogo de Produtos

  Contexto:
    Dado que o usuário acessa a página inicial do catálogo de produtos

  Cenário: Busca de produto por palavra-chave válida (Caminho Feliz)
    Quando o usuário digita "Jacket" na barra de busca e clica em pesquisar
    Então o catálogo deve exibir apenas produtos correspondentes ao termo "Jacket"

  Cenário: Filtragem por categoria de produto (Caminho Feliz)
    Quando o usuário seleciona a categoria "Roupas Masculinas"
    Então o catálogo deve atualizar exibindo somente os itens pertencentes a essa categoria

  Cenário: Ordenação de produtos por preço crescente (Caminho Alternativo)
    Quando o usuário seleciona a ordenação "Ordenar por preço: menor para maior"
    Então os produtos devem ser reorganizados do menor valor para o maior valor

  Cenário: Busca por produto inexistente (Caminho Negativo)
    Quando o usuário pesquisa pelo termo "ProdutoInexistenteXYZ123"
    Então o catálogo deve exibir a mensagem "Nenhum produto foi encontrado correspondente à sua seleção."
```

---

### [US-0005] é Painel Minha Conta
**Como** cliente autenticado da EBAC-SHOP  
**Quero** acessar o painel principal da Minha Conta  
**Para** visualizar o resumo da minha atividade e atalhos rápidos  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0005] Painel Minha Conta

  Contexto:
    Dado que o cliente está autenticado na plataforma

  Cenário: Acesso ao Dashboard da conta (Caminho Feliz)
    Quando o cliente clica em "Minha Conta"
    Então deve visualizar a mensagem de boas-vindas personalizada com seu nome
    E deve visualizar os atalhos para "Painel", "Pedidos", "Endereços", "Detalhes da Conta" e "Sair"

  Cenário: Logout seguro da conta (Caminho Alternativo)
    Quando o cliente clica na opção "Sair" do painel
    Então a sessão atual deve ser encerrada
    E o usuário deve ser redirecionado para a tela de login

  Cenário: Tentativa de acesso ao painel sem autenticação (Caminho Negativo)
    Dado que o usuário não está autenticado
    Quando tenta acessar a URL direta "/minha-conta"
    Então o sistema deve exibir os formulários de Login e Registro ao invés do dashboard

  Cenário: Persistência de sessão com a opção "Lembrar-me" marcada (Caminho Alternativo)
    Quando o usuário faz login marcando a opção "Lembrar-me"
    E fecha e reabre o navegador
    Então o usuário deve permanecer autenticado no painel
```

---

### [US-0006] é Meus Pedidos
**Como** cliente da EBAC-SHOP  
**Quero** consultar a lista e os detalhes dos meus pedidos anteriores  
**Para** acompanhar o status de entrega e histórico de compras  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0006] Meus Pedidos

  Contexto:
    Dado que o cliente está autenticado na seção "Minha Conta > Pedidos"

  Cenário: Visualização do histórico de pedidos (Caminho Feliz)
    Dado que o cliente possui pedidos realizados anteriormente
    Quando o cliente acessa a aba "Pedidos"
    Então deve visualizar a tabela com colunas "Pedido", "Data", "Status", "Total" e "Ações"

  Cenário: Visualização detalhada de um pedido específico (Caminho Feliz)
    Quando o cliente clica no botão "Visualizar" de um pedido com status "Processando"
    Então o sistema deve exibir a página de detalhes com itens comprados, endereço de entrega e método de pagamento

  Cenário: Cliente sem nenhum histórico de compras (Caminho Alternativo)
    Dado que o cliente acabou de se cadastrar e não possui pedidos
    Quando o cliente acessa a aba "Pedidos"
    Então deve ser exibida a mensagem "Nenhum pedido foi feito ainda." juntamente ao botão "Ir para a loja"

  Cenário: Tentativa de acessar detalhes de pedido pertencente a outro cliente (Caminho Negativo / Segurança)
    Quando o cliente tenta acessar a URL de um pedido com ID de outro usuário
    Então o sistema deve negar o acesso exibindo status 403 / "Você não tem permissão para visualizar este pedido"
```

---

### [US-0007] é Endereços
**Como** cliente da EBAC-SHOP  
**Quero** cadastrar e atualizar meus endereços de cobrança e entrega  
**Para** agilizar o processo de checkout em compras futuras  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0007] Endereços

  Contexto:
    Dado que o cliente autenticado acessa a aba "Endereços"

  Cenário: Atualizar endereço de faturamento com sucesso (Caminho Feliz)
    Quando o cliente clica em "Editar" no Endereço de Faturamento
    E preenche todos os campos obrigatórios com dados válidos (Nome, Sobrenome, CEP, Rua, Cidade, Estado)
    E clica em "Salvar Endereço"
    Então o sistema deve salvar as alterações
    E exibir a mensagem "Endereço alterado com sucesso."

  Cenário: Tentativa de salvar endereço com CEP em formato inválido (Caminho Negativo)
    Quando o cliente insere o CEP "1234" (formato incompleto)
    E tenta salvar o endereço
    Então o sistema deve exibir mensagem de erro "Por favor, insira um CEP válido."

  Cenário: Omissão de campo obrigatório no cadastro de endereço (Caminho Negativo)
    Quando o cliente deixa o campo "Cidade" em branco
    E tenta salvar as alterações
    Então o sistema deve destacar o campo "Cidade" e impedir o envio

  Cenário: Manter endereços distintos para cobrança e entrega (Caminho Alternativo)
    Quando o cliente cadastra um endereço para Cobrança e outro diferente para Entrega
    Então ambos os endereços devem ser persistidos e exibidos separadamente na área de endereços
```

---

### [US-0008] é Detalhes da Conta
**Como** cliente da EBAC-SHOP  
**Quero** gerenciar meus dados pessoais e alterar minha senha de acesso  
**Para** manter minha conta segura e com informações atualizadas  

#### Critérios de Aceitação (BDD / Gherkin):
```gherkin
Funcionalidade: [US-0008] Detalhes da Conta

  Contexto:
    Dado que o cliente autenticado acessa a aba "Detalhes da Conta"

  Cenário: Alteração do nome de exibição com sucesso (Caminho Feliz)
    Quando o cliente altera o campo "Nome de Exibição" para "Leonardo QA"
    E clica em "Salvar Alterações"
    Então o sistema deve exibir a notificação "Detalhes da conta modificados com sucesso."

  Cenário: Alteração de senha com credenciais válidas (Caminho Feliz)
    Quando o cliente informa a "Senha atual" correta
    E informa uma "Nova senha" forte e a repete em "Confirmar nova senha"
    E clica em "Salvar Alterações"
    Então a nova senha deve ser salva e o usuário mantido autenticado

  Cenário: Tentativa de alteração de senha com senha atual incorreta (Caminho Negativo)
    Quando o cliente preenche a "Senha atual" com valor incorreto
    E submete o formulário de alteração de senha
    Então o sistema deve rejeitar a solicitação com a mensagem "Sua senha atual está incorreta."

  Cenário: Divergência entre nova senha e confirmação de senha (Caminho Negativo)
    Quando o cliente digita "NovaSenha@123" e em confirmação digita "OutraSenha@456"
    E tenta salvar
    Então o sistema deve acusar "As novas senhas não coincidem."
```

---

## 3. Matriz de Casos de Teste (Detalhamento Técnico)

| ID | História | Cenário / Descrição | Tipo | Técnica Aplicada | Automação? |
|---|---|---|---|---|---|
| **TC-001** | US-0001 | Adicionar 10 itens de um mesmo produto | Caminho Feliz | Valor Limite (BVA) | **Sim (UI)** |
| **TC-002** | US-0001 | Tentar adicionar 11 itens de um mesmo produto | Caminho Negativo | Valor Limite (BVA) | **Sim (UI)** |
| **TC-003** | US-0001 | Bloquear checkout com valor total > R$ 990,00 | Caminho Negativo | Partição de Equivalência (EP) | **Sim (UI)** |
| **TC-004** | US-0001 | Aplicar cupom 10% para compras entre R$ 200 e R$ 600 | Caminho Alternativo | Tabela de Decisão | **Sim (UI)** |
| **TC-005** | US-0001 | Aplicar cupom 15% para compras > R$ 600 | Caminho Alternativo | Tabela de Decisão | Não (Manual) |
| **TC-006** | US-0002 | Login com sucesso para usuário ativo | Caminho Feliz | Tabela de Decisão | **Sim (UI / K6)** |
| **TC-007** | US-0002 | Login com senha incorreta | Caminho Negativo | Partição de Equivalência | **Sim (UI)** |
| **TC-008** | US-0002 | Bloqueio de conta por 15 min após 3 erros de senha | Caminho Alternativo | Transição de Estados | **Sim (UI)** |
| **TC-009** | US-0002 | Login com usuário inativo | Caminho Negativo | Tabela de Decisão | Não (Manual) |
| **TC-010** | US-0003 | Listar todos os cupons via GET com Basic Auth | Caminho Feliz | Teste de Contrato | **Sim (API Supertest)** |
| **TC-011** | US-0003 | Consultar cupom por ID existente | Caminho Feliz | Partição de Equivalência | **Sim (API Supertest)** |
| **TC-012** | US-0003 | Cadastrar cupom válido com campos obrigatórios | Caminho Feliz | Partição de Equivalência | **Sim (API Supertest)** |
| **TC-013** | US-0003 | Tentar cadastrar cupom com código já existente | Caminho Negativo | Tabela de Decisão | **Sim (API Supertest)** |
| **TC-014** | US-0003 | Tentar cadastrar cupom sem campo obrigatório | Caminho Negativo | Valor Limite / Schema | **Sim (API Supertest)** |
| **TC-015** | US-0004 | Buscar produto por palavra-chave na vitrine Mobile | Caminho Feliz | Partição de Equivalência | **Sim (Mobile)** |
| **TC-016** | US-0004 | Filtrar produtos por categoria no catálogo Mobile | Caminho Alternativo | Partição de Equivalência | **Sim (Mobile)** |
| **TC-017** | US-0004 | Ordenar catálogo por menor preço | Caminho Alternativo | Caixa-Preta | Não (Manual) |
| **TC-018** | US-0004 | Busca por produto inexistente | Caminho Negativo | Partição de Equivalência | Não (Manual) |
| **TC-019** | US-0005 | Visualizar dashboard Minha Conta com sucesso | Caminho Feliz | Caixa-Preta | Não (Manual) |
| **TC-020** | US-0005 | Efetuar logout e invalidar sessão | Caminho Alternativo | Transição de Estados | Não (Manual) |
| **TC-021** | US-0006 | Consultar lista e status de pedidos anteriores | Caminho Feliz | Caixa-Preta | Não (Manual) |
| **TC-022** | US-0007 | Atualizar endereço de faturamento com sucesso | Caminho Feliz | Partição de Equivalência | Não (Manual) |
| **TC-023** | US-0008 | Alterar senha da conta com validação da senha atual | Caminho Feliz | Tabela de Decisão | Não (Manual) |
| **TC-024** | US-0008 | Tentar alterar senha com senha atual incorreta | Caminho Negativo | Tabela de Decisão | Não (Manual) |
