Cypress.Commands.add('login', (username, password) => {
  cy.visit('/minha-conta/');
  cy.get('#username').clear().type(username);
  cy.get('#password').clear().type(password, { log: false });
  cy.get('input[name="login"]').click();
});
