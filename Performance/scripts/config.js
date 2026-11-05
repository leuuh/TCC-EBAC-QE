// Perfis de execução compartilhados pelos scripts K6.
// Escolha com a variável de ambiente PROFILE (padrão: load).
//
//   smoke -> 2 VUs por 30s. Valida que o fluxo funciona. Usado no CI,
//            porque a loja é um ambiente compartilhado do curso e os
//            runners do GitHub ficam nos EUA (latência maior).
//   load  -> cenário do TCC: ramp-up de 20s até 20 VUs, 1m20s de carga
//            constante e 20s de ramp-down. Rodar localmente ou sob demanda.

export const BASE_URL = __ENV.BASE_URL || 'http://lojaebac.ebaconline.art.br';

const PROFILES = {
  smoke: {
    vus: 2,
    duration: '30s',
    thresholds: {
      http_req_duration: ['p(95)<3000'],
      http_req_failed: ['rate<0.01'],
      checks: ['rate>0.99'],
    },
  },
  load: {
    stages: [
      { duration: '20s', target: 20 },
      { duration: '1m20s', target: 20 },
      { duration: '20s', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<2000'],
      http_req_failed: ['rate<0.05'],
    },
  },
};

const PROFILE = __ENV.PROFILE || 'load';

if (!PROFILES[PROFILE]) {
  throw new Error(`PROFILE inválido: "${PROFILE}". Use: ${Object.keys(PROFILES).join(', ')}`);
}

export const options = PROFILES[PROFILE];
