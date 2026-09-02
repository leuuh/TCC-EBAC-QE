# Justificativa Técnica da Escolha do Framework de UI (Web)

Para a automação dos testes de ponta a ponta (E2E) da plataforma **EBAC Shop**, realizamos um comparativo técnico entre as três principais ferramentas do mercado: **Cypress**, **Playwright** e **Selenium WebDriver**.

---

## 1. Matriz Comparativa de Ferramentas

| Critério de Avaliação | Cypress (Escolhido) | Playwright | Selenium WebDriver |
|---|---|---|---|
| **Linguagem Principal** | JavaScript / TypeScript | JavaScript, TypeScript, Python, Java, C# | Java, Python, C#, JS, Ruby |
| **Arquitetura de Execução** | Roda diretamente dentro do laço de eventos do navegador | Conexão via Chrome DevTools Protocol (CDP) e WebSockets | Protocolo W3C WebDriver (Driver intermediário) |
| **Velocidade de Execução** | Muito Rápida | Extremamente Rápida | Média (depende da latência do driver) |
| **Mecanismo de Espera (Auto-waiting)** | Nativo e automático em todos os comandos | Nativo e automático em ações e asserá?es | Manual (necessita de `WebDriverWait` e `ExpectedConditions`) |
| **Time-travel & Debugging** | Interface visual interativa com snapshots de DOM a cada passo | Trace Viewer visual detalhado | Logs manuais e screenshots de falhas |
| **Suporte a Múltiplas Abas / Janelas** | Limitado (focado na janela principal) | Totalmente nativo | Totalmente nativo |
| **Curva de Aprendizado** | Baixa a Média (altamente intuitivo) | Média | Alta (requer boilerplate e infraestrutura) |
| **Padrões de Projeto Suportados** | Page Objects, App Actions, Custom Commands | Page Objects, Screenplay, Fixtures | Page Objects, Page Factory, Screenplay |
| **Integração com CI/CD** | Excelente (execução headless via Docker/CLI) | Excelente | Boa (requer configuração de Grid/Selenium Hub) |

---

## 2. Justificativa da Escolha do Cypress

Optamos pelo **Cypress** com **JavaScript** para a camada de testes de UI do projeto EBAC Shop pelos seguintes motivos:

1. **Facilidade de Escrita e Produtividade:** A sintaxe fluida e encadeada do Cypress (`cy.get().type().click()`) permite criar testes expressivos que refletem fielmente as etapas dos critérios de aceitação modelados em BDD.
2. **Auto-waiting Inteligente:** O Cypress elimina o uso de `sleeps` arbitrários e espera automaticamente que os elementos da loja estejam renderizados, clicáveis e interativos, reduzindo drasticamente a ocorrência de testes instáveis (*flaky tests*).
3. **Padrão de Projeto Page Object Model (POM):** Implementamos os Page Objects em `cypress/support/page_objects/` (`login.page.js` e `cart.page.js`), centralizando localizadores e métodos de ação para maximizar o reúso e facilitar a manutenção.
4. **Relatérios Ricos com Mochawesome:** Integração nativa com `cypress-mochawesome-reporter`, gerando relatórios HTML profissionais com capturas de tela das falhas anexadas automaticamente para auditoria de QA.
5. **Harmonia com o Ecossistema Node.js:** Unificação da stack tecnológica com o projeto de API (Supertest) e Mobile (WebdriverIO), permitindo que toda a suíte de testes compartilhe ferramentas de linter, scripts npm e pipelines de CI/CD.
