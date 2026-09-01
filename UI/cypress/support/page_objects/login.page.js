class LoginPage {
  get usernameInput() { return cy.get('#username'); }
  get passwordInput() { return cy.get('#password'); }
  get loginButton() { return cy.get('input[name="login"]'); }
  get rememberMeCheckbox() { return cy.get('#rememberme'); }
  get lostPasswordLink() { return cy.get('a[href*="lost-password"]'); }
  get errorMessageAlert() { return cy.get('.woocommerce-error'); }
  get accountWelcomeText() { return cy.get('.woocommerce-MyAccount-content'); }

  visit() {
    cy.visit('/minha-conta/');
    return this;
  }

  fillUsername(username) {
    this.usernameInput.clear().type(username);
    return this;
  }

  fillPassword(password) {
    this.passwordInput.clear().type(password, { log: false });
    return this;
  }

  submitLogin() {
    this.loginButton.click();
    return this;
  }

  loginWith(username, password) {
    this.visit();
    this.fillUsername(username);
    this.fillPassword(password);
    this.submitLogin();
    return this;
  }
}

export default new LoginPage();
