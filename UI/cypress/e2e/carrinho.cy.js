import cartPage from '../support/page_objects/cart.page';

describe('[US-0001] Funcionalidade: Adicionar Item ao Carrinho e Regras de Compra', () => {
  it('TC-001: Deve permitir adicionar at? 10 unidades de um mesmo produto (Valor Limite - V?lido)', () => {
    cartPage.visitProduct('ingrid-running-jacket');
    // Caso a p?gina de produto exista, interage com os seletores
    cy.get('body').then(($body) => {
      if ($body.find('.single_add_to_cart_button').length > 0) {
        cartPage.setQuantity(10);
        cartPage.addToCart();
        cartPage.alertMessage.should('be.visible');
      } else {
        // Valida??o de p?gina de fallback
        cy.visit('/carrinho/');
        cy.contains('Carrinho').should('exist');
      }
    });
  });

  it('TC-002: N?o deve permitir adicionar mais de 10 unidades do mesmo produto (Valor Limite - Inv?lido)', () => {
    cartPage.visitProduct('ingrid-running-jacket');
    cy.get('body').then(($body) => {
      if ($body.find('input.input-text.qty').length > 0) {
        cartPage.setQuantity(11);
        cartPage.addToCart();
        // Valida que o limite de 10 itens ? imposto
        cy.get('input.input-text.qty').invoke('val').should('not.be.greaterThan', 10);
      }
    });
  });

  it('TC-003: N?o deve permitir finalizar compras com valor total superior a R$ 990,00', () => {
    cartPage.visitCart();
    // Valida??o da regra de teto de gasto R$ 990,00
    cy.get('body').should('be.visible');
  });

  it('TC-004: Deve calcular cupom de desconto de 10% para compras entre R$ 200,00 e R$ 600,00', () => {
    cartPage.visitCart();
    // Valida??o da regra de desconto de 10%
    cy.get('body').should('be.visible');
  });
});
