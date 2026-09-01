class CartPage {
  get quantityInput() { return cy.get('input.input-text.qty'); }
  get addToCartButton() { return cy.get('.single_add_to_cart_button'); }
  get cartTable() { return cy.get('.woocommerce-cart-form'); }
  get cartItemRows() { return cy.get('.cart_item'); }
  get subtotalElement() { return cy.get('.cart-subtotal .woocommerce-Price-amount'); }
  get totalElement() { return cy.get('.order-total .woocommerce-Price-amount'); }
  get discountElement() { return cy.get('.cart-discount'); }
  get checkoutButton() { return cy.get('.checkout-button'); }
  get alertMessage() { return cy.get('.woocommerce-message, .woocommerce-error'); }

  visitProduct(productSlug) {
    cy.visit(`/produtos/${productSlug}/`);
    return this;
  }

  visitCart() {
    cy.visit('/carrinho/');
    return this;
  }

  setQuantity(qty) {
    this.quantityInput.clear().type(qty.toString());
    return this;
  }

  addToCart() {
    this.addToCartButton.click();
    return this;
  }

  proceedToCheckout() {
    this.checkoutButton.click();
    return this;
  }
}

export default new CartPage();
