class ProductPage {
  get productTitle() {
    return $('~product-title');
  }

  get productPrice() {
    return $('~product-price');
  }

  get quantitySelector() {
    return $('~quantity-input');
  }

  get addToCartButton() {
    return $('~add-to-cart-button');
  }

  get successToastMessage() {
    return $('~toast-success');
  }

  async addProductToCart(quantity = 1) {
    await this.quantitySelector.setValue(quantity.toString());
    await this.addToCartButton.click();
  }
}

module.exports = new ProductPage();
