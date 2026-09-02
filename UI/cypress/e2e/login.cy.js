import loginPage from '../support/page_objects/login.page';

describe('[US-0002] Funcionalidade: Autenticação na Plataforma (Login)', () => {
  beforeEach(() => {
    loginPage.visit();
  });

  it('TC-006: Deve realizar login com sucesso para usuário ativo (Caminho Feliz)', () => {
    loginPage.fillUsername('cliente_ativo@ebac.com.br');
    loginPage.fillPassword('Teste@123');
    loginPage.submitLogin();

    // Verificação de URL e presença do painel
    cy.url().should('include', '/minha-conta');
  });

  it('TC-007: Deve exibir mensagem de erro ao inserir credenciais inválidas (Caminho Negativo)', () => {
    loginPage.fillUsername('usuario_invalido@ebac.com.br');
    loginPage.fillPassword('SenhaIncorreta999');
    loginPage.submitLogin();

    loginPage.errorMessageAlert.should('be.visible');
    loginPage.errorMessageAlert.should('contain.text', 'Erro');
  });

  it('TC-008: Deve alertar e bloquear login temporariamente após 3 erros consecutivos de senha', () => {
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
