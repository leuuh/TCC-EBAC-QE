const couponSchema = {
  type: 'object',
  required: ['id', 'code', 'amount', 'discount_type'],
  properties: {
    id: { type: 'integer' },
    code: { type: 'string' },
    amount: { type: 'string' },
    discount_type: { 
      type: 'string',
      enum: ['percent', 'fixed_cart', 'fixed_product']
    },
    description: { type: 'string' },
    date_expires: { type: ['string', 'null'] },
    date_expires_gmt: { type: ['string', 'null'] },
    usage_count: { type: 'integer' },
    individual_use: { type: 'boolean' },
    product_ids: { 
      type: 'array',
      items: { type: 'integer' }
    },
    excluded_product_ids: { 
      type: 'array',
      items: { type: 'integer' }
    },
    usage_limit: { type: ['integer', 'null'] },
    usage_limit_per_user: { type: ['integer', 'null'] },
    free_shipping: { type: 'boolean' },
    minimum_amount: { type: 'string' },
    maximum_amount: { type: 'string' }
  }
};

const couponListSchema = {
  type: 'array',
  items: couponSchema
};

module.exports = {
  couponSchema,
  couponListSchema
};
