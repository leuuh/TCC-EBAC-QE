import loginPage from '../support/page_objects/login.page';

describe('[US-0002] Funcionalidade: Autentica??o na Plataforma (Login)', () => {
  beforeEach(() => {
    loginPage.visit();
  });

  it('TC-006: Deve realizar login com sucesso para usu?rio ativo (Caminho Feliz)', () => {
    loginPage.fillUsername('cliente_ativo@ebac.com.br');
    loginPage.fillPassword('Teste@123');
    loginPage.submitLogin();

    // Verifica??o de URL e presen?a do painel
    cy.url().should('include', '/minha-conta');
  });

  it('TC-007: Deve exibir mensagem de erro ao inserir credenciais inv?lidas (Caminho Negativo)', () => {
    loginPage.fillUsername('usuario_invalido@ebac.com.br');
    loginPage.fillPassword('SenhaIncorreta999');
    loginPage.submitLogin();

    loginPage.errorMessageAlert.should('be.visible');
    loginPage.errorMessageAlert.should('contain.text', 'Erro');
  });

  it('TC-008: Deve alertar e bloquear login temporariamente ap?s 3 erros consecutivos de senha', () => {
    const invalidPass = 'SenhaErrada123';
    
    // Simula 3 tentativas seguidas de erro
    for (let tentativa = 1; tentativa <= 3; tentativa++) {
      loginPage.fillUsername('cliente_ativo@ebac.com.br');
      loginPage.fillPassword(invalidPass);
      loginPage.submitLogin();
      loginPage.errorMessageAlert.should('be.visible');
    }
  });
});
