import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// Carrega a massa de dados de usuários do arquivo JSON
const users = new SharedArray('massa de usuarios', function () {
  return JSON.parse(open('../data/users.json'));
});

export const options = {
  stages: [
    { duration: '20s', target: 20 }, // Ramp-Up: atinge 20 VUs em 20 segundos
    { duration: '1m20s', target: 20 }, // Sustentação de carga com 20 VUs
    { duration: '20s', target: 0 },  // Ramp-Down: desaceleração
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% das requisições devem responder em menos de 2s
    http_req_failed: ['rate<0.05'],    // Taxa de erro inferior a 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://lojaebac.ebaconline.art.br';

export default function () {
  // Seleciona um usuário da massa de dados de forma distribuída entre os VUs
  const user = users[__VU % users.length];

  // Passo 1: Acesso à página de login
  const resLoginPage = http.get(`${BASE_URL}/minha-conta/`);
  check(resLoginPage, {
    'GET /minha-conta/ status é 200': (r) => r.status === 200,
    'Formulário de login renderizado': (r) => r.body.includes('username') || r.body.includes('login'),
  });

  sleep(1);

  // Passo 2: Submissão de autenticação (POST)
  const loginPayload = {
    username: user.username,
    password: user.password,
    'woocommerce-login-nonce': '',
    login: 'Login',
  };

  const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
  const resLoginSubmit = http.post(`${BASE_URL}/minha-conta/`, loginPayload, { headers });

  check(resLoginSubmit, {
    'POST Login status é 200 ou 302': (r) => [200, 302].includes(r.status),
    'Tempo de resposta de login < 2000ms': (r) => r.timings.duration < 2000,
  });

  sleep(1);
}
