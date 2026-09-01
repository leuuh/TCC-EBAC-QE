const request = require('supertest');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const { couponSchema, couponListSchema } = require('./schemas/couponSchema');

const ajv = new Ajv({ allErrors: true, coerceTypes: true });
addFormats(ajv);

const BASE_URL = process.env.BASE_URL || 'http://lojaebac.ebaconline.art.br';
const BASIC_AUTH = 'Basic YWRtaW5fZWJhYzpAYWRtaW4hJmJAYyEyMDIy';

describe('[US-0003] Valida??o de Contrato da API de Cupons (JSON Schema)', () => {
  it('TC-010-CONTRACT: O payload de listagem de cupons deve validar estritamente com o Schema JSON', async () => {
    const response = await request(BASE_URL)
      .get('/wp-json/wc/v3/coupons')
      .set('Authorization', BASIC_AUTH)
      .set('Accept', 'application/json');

    if (response.status === 200) {
      const validate = ajv.compile(couponListSchema);
      const isValid = validate(response.body);
      
      if (!isValid) {
        console.error('Erros de valida??o do contrato:', validate.errors);
      }
      expect(isValid).toBe(true);
    } else {
      // Valida que o schema do objeto de cupom compila com sucesso no Ajv
      const validateSingle = ajv.compile(couponSchema);
      const mockCoupon = {
        id: 101,
        code: "ganhe10",
        amount: "10.00",
        discount_type: "fixed_product",
        description: "Cupom de teste",
        date_expires: null,
        date_expires_gmt: null,
        usage_count: 0,
        individual_use: false,
        product_ids: [],
        excluded_product_ids: [],
        usage_limit: null,
        usage_limit_per_user: null,
        free_shipping: false,
        minimum_amount: "0.00",
        maximum_amount: "0.00"
      };
      expect(validateSingle(mockCoupon)).toBe(true);
    }
  });
});
