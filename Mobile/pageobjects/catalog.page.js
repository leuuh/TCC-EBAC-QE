class CatalogPage {
  get searchInput() {
    return $('~search-input');
  }

  get searchButton() {
    return $('~search-button');
  }

  get productList() {
    return $$('~product-card');
  }

  get categoryFilterDropdown() {
    return $('~category-filter');
  }

  get emptyResultsMessage() {
    return $('~empty-catalog-message');
  }

  async searchProduct(term) {
    await this.searchInput.setValue(term);
    await this.searchButton.click();
  }

  async selectFirstProduct() {
    const products = await this.productList;
    if (products.length > 0) {
      await products[0].click();
    }
  }

  async filterByCategory(categoryName) {
    await this.categoryFilterDropdown.click();
    const option = await $(`//*[@text="${categoryName}"]`);
    await option.click();
  }
}

module.exports = new CatalogPage();
