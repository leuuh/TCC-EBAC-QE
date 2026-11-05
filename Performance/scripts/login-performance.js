import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { BASE_URL, options as profileOptions } from './config.js';

// Carrega a massa de dados de usuários do arquivo JSON
const users = new SharedArray('massa de usuarios', function () {
  return JSON.parse(open('../data/users.json'));
});

export const options = profileOptions;

const LOGIN_URL = `${BASE_URL}/minha-conta/`;

export default function () {
  // Seleciona um usuário da massa de dados de forma distribuída entre os VUs
  const user = users[__VU % users.length];

  // Cada iteração começa deslogada: sem isso, a partir da 2ª iteração o VU já
  // estaria logado e a página não teria o formulário (nem o nonce).
  http.cookieJar().clear(BASE_URL);

  // Passo 1: Acesso à página de login
  const resLoginPage = http.get(LOGIN_URL);
  const nonce = resLoginPage.html()
    .find('input[name="woocommerce-login-nonce"]')
    .attr('value');

  check(resLoginPage, {
    'GET /minha-conta/ status é 200': (r) => r.status === 200,
    'Formulário de login com nonce': () => !!nonce,
  });

  if (!nonce) {
    sleep(1);
    return;
  }

  sleep(1);

  // Passo 2: Submissão de autenticação (POST). O WooCommerce exige o nonce do
  // formulário; sem ele o login é recusado. O 302 é seguido automaticamente.
  const resLoginSubmit = http.post(LOGIN_URL, {
    username: user.username,
    password: user.password,
    'woocommerce-login-nonce': nonce,
    _wp_http_referer: '/minha-conta/',
    login: 'Login',
  });

  check(resLoginSubmit, {
    'POST Login status é 200': (r) => r.status === 200,
    'Usuário autenticado (link de logout visível)': (r) =>
      typeof r.body === 'string' && r.body.includes('customer-logout'),
  });

  sleep(1);
}
