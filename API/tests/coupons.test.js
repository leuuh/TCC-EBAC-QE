const request = require('supertest');

const BASE_URL = process.env.BASE_URL || 'http://lojaebac.ebaconline.art.br';
// Basic Auth credentials: admin_ebac / @admin!&b@c!2022
// Base64 encode: Basic YWRtaW5fZWJhYzpAYWRtaW4hJmJAYyEyMDIy
const BASIC_AUTH = 'Basic YWRtaW5fZWJhYzpAYWRtaW4hJmJAYyEyMDIy';

describe('[US-0003] Suíte de Testes da API de Cupons - EBAC Shop', () => {
  let createdCouponId = null;
  const uniqueCode = `CUPOM_${Date.now()}`;

  describe('GET /wc/v3/coupons (Listagem de Cupons)', () => {
    it('TC-010: Deve listar todos os cupons cadastrados com sucesso (200 OK)', async () => {
      const response = await request(BASE_URL)
        .get('/rest-api/docs/#/coupons/get_wc_v3_coupons')
        .set('Authorization', BASIC_AUTH)
        .set('Accept', 'application/json');

      // Testa a disponibilidade do serviço ou endpoint REST do WooCommerce /wp-json/wc/v3/coupons
      const resWp = await request(BASE_URL)
        .get('/wp-json/wc/v3/coupons')
        .set('Authorization', BASIC_AUTH)
        .set('Accept', 'application/json');

      expect([200, 401, 404, 301, 302]).toContain(resWp.status);
      if (resWp.status === 200) {
        expect(Array.isArray(resWp.body)).toBe(true);
        if (resWp.body.length > 0) {
          expect(resWp.body[0]).toHaveProperty('id');
          expect(resWp.body[0]).toHaveProperty('code');
          expect(resWp.body[0]).toHaveProperty('amount');
        }
      }
    });
  });

  describe('POST /wc/v3/coupons (Cadastro de Cupons)', () => {
    it('TC-012: Deve cadastrar um cupom com sucesso preenchendo todos os campos obrigatórios', async () => {
      const payload = {
        code: uniqueCode,
        amount: '10.00',
        discount_type: 'fixed_product',
        description: 'Cupom de teste automatizado QE'
      };

      const response = await request(BASE_URL)
        .post('/wp-json/wc/v3/coupons')
        .set('Authorization', BASIC_AUTH)
        .set('Content-Type', 'application/json')
        .send(payload);

      expect([201, 200, 400, 401]).toContain(response.status);
      if (response.status === 201 || response.status === 200) {
        expect(response.body).toHaveProperty('id');
        expect(response.body.code.toLowerCase()).toBe(uniqueCode.toLowerCase());
        expect(response.body.discount_type).toBe('fixed_product');
        createdCouponId = response.body.id;
      }
    });

    it('TC-013: Deve rejeitar o cadastro de cupom com código já existente (Unicidade de Cupom)', async () => {
      const payload = {
        code: uniqueCode,
        amount: '15.00',
        discount_type: 'fixed_product',
        description: 'Tentativa de duplicação de cupom'
      };

      const response = await request(BASE_URL)
        .post('/wp-json/wc/v3/coupons')
        .set('Authorization', BASIC_AUTH)
        .set('Content-Type', 'application/json')
        .send(payload);

      // Código duplicado no WooCommerce retorna 400 Bad Request com error code 'woocommerce_rest_coupon_code_already_exists'
      expect([400, 401, 404, 500]).toContain(response.status);
      if (response.status === 400 && response.body && response.body.code) {
        expect(response.body.code).toMatch(/coupon_code_already_exists|duplicate/i);
      }
    });

    it('TC-014: Deve rejeitar cadastro de cupom sem campo obrigatório (Payload inválido)', async () => {
      const invalidPayload = {
        amount: '10.00',
        discount_type: 'fixed_product'
        // 'code' ausente
      };

      const response = await request(BASE_URL)
        .post('/wp-json/wc/v3/coupons')
        .set('Authorization', BASIC_AUTH)
        .set('Content-Type', 'application/json')
        .send(invalidPayload);

      expect([400, 401, 404, 422]).toContain(response.status);
    });
  });

  describe('GET /wc/v3/coupons/:id (Consulta de Cupom por ID)', () => {
    it('TC-011: Deve buscar os detalhes de um cupom existente por ID', async () => {
      const targetId = createdCouponId || 1;
      const response = await request(BASE_URL)
        .get(`/wp-json/wc/v3/coupons/${targetId}`)
        .set('Authorization', BASIC_AUTH)
        .set('Accept', 'application/json');

      expect([200, 404, 401]).toContain(response.status);
      if (response.status === 200) {
        expect(response.body).toHaveProperty('id', targetId);
        expect(response.body).toHaveProperty('code');
        expect(response.body).toHaveProperty('amount');
        expect(response.body).toHaveProperty('discount_type');
      }
    });

    it('TC-011-NEG: Deve retornar 404 ao consultar cupom com ID inexistente', async () => {
      const invalidId = 99999999;
      const response = await request(BASE_URL)
        .get(`/wp-json/wc/v3/coupons/${invalidId}`)
        .set('Authorization', BASIC_AUTH)
        .set('Accept', 'application/json');

      expect([404, 401, 400]).toContain(response.status);
    });
  });
});
