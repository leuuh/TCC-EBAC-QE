# TCC - Engenheiro de Qualidade de Software (EBAC)
**Autor:** Leonardo de Almeida  
**Projeto:** Automa??o e Estrat?gia de Qualidade de Software para a EBAC-SHOP  
**Reposit?rio:** `TCC-EBAC-QE`  

---

## ?? Vis?o Geral do Projeto
Este reposit?rio consolida o Trabalho de Conclus?o de Curso (TCC) da forma??o **Engenheiro de Qualidade de Software** da **EBAC**. O projeto implementa uma abordagem completa de Engenharia de Qualidade (QE) para a plataforma de e-commerce **EBAC Shop** (http://lojaebac.ebaconline.art.br/), cobrindo desde a modelagem de testes em BDD (Gherkin), matriz de casos de teste com t?cnicas formais, at? a automa??o em m?ltiplos n?veis (UI, API, Mobile, Performance) e integra??o cont?nua (CI/CD).

---

## ??? Estrutura do Reposit?rio

```text
TCC-EBAC-QE/
??? .github/
?   ??? workflows/              # Pipelines de CI/CD (GitHub Actions)
?       ??? test-api.yml        # Testes automatizados de API (Supertest + Jest)
?       ??? test-ui.yml         # Testes E2E Web (Cypress Headless)
?       ??? test-k6.yml         # Testes de Carga e Performance (K6)
??? UI/                         # Automa??o de Interface Web (Cypress + POM)
?   ??? cypress/
?   ?   ??? e2e/                # Cen?rios de Carrinho (US-0001) e Login (US-0002)
?   ?   ??? support/page_objects/ # Padr?o Page Object Model
?   ??? JUSTIFICATIVA_FERRAMENTAS.md # Comparativo Cypress vs Playwright vs Selenium
?   ??? cypress.config.js
??? API/                        # Automa??o de API Rest e Contrato (US-0003)
?   ??? tests/
?   ?   ??? coupons.test.js     # Valida??es funcionais e de regras da API de Cupons
?   ?   ??? contract.test.js    # Teste de Contrato com JSON Schema (Ajv)
?   ?   ??? schemas/            # Schemas de valida??o
?   ??? jest.config.js
??? Mobile/                     # Automa??o Mobile Android (US-0004)
?   ??? pageobjects/            # Page Objects do Cat?logo e Detalhes de Produtos
?   ??? specs/                  # Specs de automa??o com WebdriverIO
?   ??? wdio.conf.js            # Configura??o do Appium / UiAutomator2
??? Performance/                # Testes de Carga e Performance (K6)
?   ??? data/users.json         # Massa de dados (user1_ebac a user5_ebac)
?   ??? scripts/                # Scripts de Carga (20 VUs, 2min, Ramp-Up 20s)
?       ??? login-performance.js
?       ??? cart-performance.js
??? docs/                       # Documenta??o t?cnica e Mapa Mental
?   ??? estrategia-e-casos-de-teste.md
?   ??? mapa-mental-estrategia.png
??? Trabalho de conclusao - Engenheiro de Qualidade de software.docx
```

---

## ?? Como Executar os Testes

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
# Modo interativo com interface gr?fica:
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
# Execu??o local com k6 instalado:
npm run test:login
npm run test:cart

# Ou execu??o via Docker:
npm run docker:login
```

---

## ??? Tecnologias e Padr?es Utilizados
- **Linguagem:** JavaScript (Node.js) / Python
- **Automa??o Web:** Cypress com Page Object Model (POM) e Mochawesome Reporter
- **Automa??o API:** Supertest + Jest + Ajv (JSON Schema Validation)
- **Automa??o Mobile:** WebdriverIO + Appium + UiAutomator2
- **Performance:** K6 (Grafana)
- **CI/CD:** GitHub Actions
- **Modelagem de Testes:** BDD / Gherkin, Parti??o de Equival?ncia, An?lise do Valor Limite e Tabela de Decis?o.
