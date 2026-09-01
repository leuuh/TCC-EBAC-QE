import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '20s', target: 20 }, // Ramp-Up: 20 VUs em 20s
    { duration: '1m20s', target: 20 }, // Carga constante de 20 VUs
    { duration: '20s', target: 0 },  // Ramp-Down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% das requisi??es abaixo de 2s
    http_req_failed: ['rate<0.05'],    // Falha menor que 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://lojaebac.ebaconline.art.br';

export default function () {
  // 1. Visualizar vitrine de produtos
  const resShop = http.get(`${BASE_URL}/produtos/`);
  check(resShop, {
    'GET /produtos/ status ? 200': (r) => r.status === 200,
    'Cat?logo renderizado': (r) => r.body.includes('woocommerce-LoopProduct-link') || r.body.includes('produtos'),
  });

  sleep(1);

  // 2. Visualizar carrinho de compras
  const resCart = http.get(`${BASE_URL}/carrinho/`);
  check(resCart, {
    'GET /carrinho/ status ? 200': (r) => r.status === 200,
    'Tempo de resposta carrinho < 2000ms': (r) => r.timings.duration < 2000,
  });

  sleep(1);
}
