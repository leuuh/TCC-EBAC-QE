import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, options as profileOptions } from './config.js';

export const options = profileOptions;

export default function () {
  // 1. Visualizar vitrine de produtos
  const resShop = http.get(`${BASE_URL}/produtos/`);
  check(resShop, {
    'GET /produtos/ status é 200': (r) => r.status === 200,
    'Catálogo renderizado': (r) =>
      typeof r.body === 'string' && r.body.includes('woocommerce-LoopProduct-link'),
  });

  sleep(1);

  // 2. Visualizar carrinho de compras
  const resCart = http.get(`${BASE_URL}/carrinho/`);
  check(resCart, {
    'GET /carrinho/ status é 200': (r) => r.status === 200,
  });

  sleep(1);
}
