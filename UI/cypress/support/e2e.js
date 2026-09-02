import './commands';
import 'cypress-mochawesome-reporter/register';

Cypress.on('uncaught:exception', (err, runnable) => {
  // Ignora exce📌es não tratadas do front-end do WordPress / tema da loja
  return false;
});
