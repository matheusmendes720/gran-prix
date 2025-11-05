import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.1'],
  },
};

export default function () {
  const params = {
    timeout: '5s',
    tags: { endpoint: 'bacen_exchange_rate' },
  };

  const url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial=01/01/2024&dataFinal=31/12/2024';
  const res = http.get(url, params);

  check(res, {
    'status is 200 or 204': (r) => r.status === 200 || r.status === 204,
  });

  sleep(1);
}
