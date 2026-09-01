# Justificativa T?cnica da Escolha do Framework de UI (Web)

Para a automa??o dos testes de ponta a ponta (E2E) da plataforma **EBAC Shop**, realizamos um comparativo t?cnico entre as tr?s principais ferramentas do mercado: **Cypress**, **Playwright** e **Selenium WebDriver**.

---

## 1. Matriz Comparativa de Ferramentas

| Crit?rio de Avalia??o | Cypress (Escolhido) | Playwright | Selenium WebDriver |
|---|---|---|---|
| **Linguagem Principal** | JavaScript / TypeScript | JavaScript, TypeScript, Python, Java, C# | Java, Python, C#, JS, Ruby |
| **Arquitetura de Execu??o** | Roda diretamente dentro do la?o de eventos do navegador | Conex?o via Chrome DevTools Protocol (CDP) e WebSockets | Protocolo W3C WebDriver (Driver intermedi?rio) |
| **Velocidade de Execu??o** | Muito R?pida | Extremamente R?pida | M?dia (depende da lat?ncia do driver) |
| **Mecanismo de Espera (Auto-waiting)** | Nativo e autom?tico em todos os comandos | Nativo e autom?tico em a??es e asser??es | Manual (necessita de `WebDriverWait` e `ExpectedConditions`) |
| **Time-travel & Debugging** | Interface visual interativa com snapshots de DOM a cada passo | Trace Viewer visual detalhado | Logs manuais e screenshots de falhas |
| **Suporte a M?ltiplas Abas / Janelas** | Limitado (focado na janela principal) | Totalmente nativo | Totalmente nativo |
| **Curva de Aprendizado** | Baixa a M?dia (altamente intuitivo) | M?dia | Alta (requer boilerplate e infraestrutura) |
| **Padr?es de Projeto Suportados** | Page Objects, App Actions, Custom Commands | Page Objects, Screenplay, Fixtures | Page Objects, Page Factory, Screenplay |
| **Integra??o com CI/CD** | Excelente (execu??o headless via Docker/CLI) | Excelente | Boa (requer configura??o de Grid/Selenium Hub) |

---

## 2. Justificativa da Escolha do Cypress

Optamos pelo **Cypress** com **JavaScript** para a camada de testes de UI do projeto EBAC Shop pelos seguintes motivos:

1. **Facilidade de Escrita e Produtividade:** A sintaxe fluida e encadeada do Cypress (`cy.get().type().click()`) permite criar testes expressivos que refletem fielmente as etapas dos crit?rios de aceita??o modelados em BDD.
2. **Auto-waiting Inteligente:** O Cypress elimina o uso de `sleeps` arbitr?rios e espera automaticamente que os elementos da loja estejam renderizados, clic?veis e interativos, reduzindo drasticamente a ocorr?ncia de testes inst?veis (*flaky tests*).
3. **Padr?o de Projeto Page Object Model (POM):** Implementamos os Page Objects em `cypress/support/page_objects/` (`login.page.js` e `cart.page.js`), centralizando localizadores e m?todos de a??o para maximizar o re?so e facilitar a manuten??o.
4. **Relat?rios Ricos com Mochawesome:** Integra??o nativa com `cypress-mochawesome-reporter`, gerando relat?rios HTML profissionais com capturas de tela das falhas anexadas automaticamente para auditoria de QA.
5. **Harmonia com o Ecossistema Node.js:** Unifica??o da stack tecnol?gica com o projeto de API (Supertest) e Mobile (WebdriverIO), permitindo que toda a su?te de testes compartilhe ferramentas de linter, scripts npm e pipelines de CI/CD.
