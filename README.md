# TCC - Engenheiro de Qualidade de Software (EBAC)
**Autor:** Leonardo de Almeida  
**Projeto:** Automação e Estratégia de Qualidade de Software para a EBAC-SHOP  
**Repositório:** `TCC-EBAC-QE`  

---

## 📌 Visão Geral do Projeto
Este repositório consolida o Trabalho de Conclusão de Curso (TCC) da formação **Engenheiro de Qualidade de Software** da **EBAC**. O projeto implementa uma abordagem completa de Engenharia de Qualidade (QE) para a plataforma de e-commerce **EBAC Shop** (http://lojaebac.ebaconline.art.br/), cobrindo desde a modelagem de testes em BDD (Gherkin), matriz de casos de teste com técnicas formais, até a automação em múltiplos níveis (UI, API, Mobile, Performance) e integração contínua (CI/CD).

---

## ├── Estrutura do Repositório

```text
TCC-EBAC-QE/
├── .github/
?   ├── workflows/              # Pipelines de CI/CD (GitHub Actions)
?       ├── test-api.yml        # Testes automatizados de API (Supertest + Jest)
?       ├── test-ui.yml         # Testes E2E Web (Cypress Headless)
?       ├── test-k6.yml         # Testes de Carga e Performance (K6)
├── UI/                         # Automação de Interface Web (Cypress + POM)
?   ├── cypress/
?   é   ├── e2e/                # Cenários de Carrinho (US-0001) e Login (US-0002)
?   é   ├── support/page_objects/ # Padrão Page Object Model
?   ├── JUSTIFICATIVA_FERRAMENTAS.md # Comparativo Cypress vs Playwright vs Selenium
?   ├── cypress.config.js
├── API/                        # Automação de API Rest e Contrato (US-0003)
?   ├── tests/
?   é   ├── coupons.test.js     # Validações funcionais e de regras da API de Cupons
?   é   ├── contract.test.js    # Teste de Contrato com JSON Schema (Ajv)
?   é   ├── schemas/            # Schemas de validação
?   ├── jest.config.js
├── Mobile/                     # Automação Mobile Android (US-0004)
?   ├── pageobjects/            # Page Objects do Catélogo e Detalhes de Produtos
?   ├── specs/                  # Specs de automação com WebdriverIO
?   ├── wdio.conf.js            # Configuração do Appium / UiAutomator2
├── Performance/                # Testes de Carga e Performance (K6)
?   ├── data/users.json         # Massa de dados (user1_ebac a user5_ebac)
?   ├── scripts/                # Scripts de Carga (20 VUs, 2min, Ramp-Up 20s)
?       ├── login-performance.js
?       ├── cart-performance.js
├── docs/                       # Documentação técnica e Mapa Mental
?   ├── estrategia-e-casos-de-teste.md
?   ├── mapa-mental-estrategia.png
├── Trabalho de conclusao - Engenheiro de Qualidade de software.docx
```

---

## 📌 Como Executar os Testes

### 1. Testes de API Rest (Supertest)
```bash
cd API
npm install
npm test
```

### 2. Testes de Interface Web (Cypress)
```bash
cd UI
npm install
# Modo interativo com interface gráfica:
npm run cypress:open
# Modo headless (linha de comando):
npm run cypress:run
```

### 3. Testes Mobile (WebdriverIO + Appium)
```bash
cd Mobile
npm install
npm run test:android
```

### 4. Testes de Performance (K6)
```bash
cd Performance
# Execução local com k6 instalado:
npm run test:login
npm run test:cart

# Ou execução via Docker:
npm run docker:login
```

---

## ├── Tecnologias e Padrões Utilizados
- **Linguagem:** JavaScript (Node.js) / Python
- **Automação Web:** Cypress com Page Object Model (POM) e Mochawesome Reporter
- **Automação API:** Supertest + Jest + Ajv (JSON Schema Validation)
- **Automação Mobile:** WebdriverIO + Appium + UiAutomator2
- **Performance:** K6 (Grafana)
- **CI/CD:** GitHub Actions
- **Modelagem de Testes:** BDD / Gherkin, Partição de Equivalência, Análise do Valor Limite e Tabela de Decisão.
