# Rate Limiter

Implementação de algoritmos de rate limiting em Python puro, focada em aprendizado de system design e engenharia.

Sem frameworks. Sem Redis. Só Python e lógica.

---

## Algoritmos

| Algoritmo | Status | Quando usar |
|---|---|---|
| Token Bucket | ✅ Implementado | Controle simples com burst permitido |
| Sliding Window Log | ✅ Implementado | Janela de tempo precisa, sem burst |
| Leaky Bucket | ⏭ Pulado | Taxa de saída estritamente uniforme |

---

## Uso

```python
from src.factory import create_limiter

# via factory — troca o algoritmo sem mudar o código cliente
limiter = create_limiter("token_bucket", capacity=10, refill_rate=1/60)

if limiter.is_allowed("user_123"):
    print("request permitido")
else:
    print("rate limit atingido")
```

### Simulação comparativa

```bash
uv run main.py
```

```
=======================================================
  Comparativo — 100 usuários, limite 10 req/min
=======================================================
Algoritmo            Requests       OK  Bloqueado  Block%
-------------------------------------------------------
token_bucket             1050     1000         50    4.8%
sliding_window           1050      998         52    5.0%
=======================================================
```

---

## Como funciona — Token Bucket

O bucket começa cheio. Cada request consome 1 token. Tokens são gerados continuamente a uma taxa constante (`refill_rate` tokens/segundo). Quando o bucket está vazio, requests são rejeitados.

```
tokens_gerados = tempo_passado × refill_rate
tokens = min(tokens + tokens_gerados, capacity)
```

**Burst**: um usuário inativo por 10s com `capacity=10` e `refill_rate=1/s` volta com bucket cheio — pode disparar 10 requests instantaneamente. Feature intencional, não bug.

→ [Diagrama visual + decisões de design](https://matheusbuniotto.github.io/rate-limiter-service/)

---

## Estrutura

```
src/
├── rate_limiter.py       # Interface base (RateLimiter ABC)
├── token_bucket.py       # Token Bucket + TokenBucketStore
├── sliding_window.py     # Sliding Window Log + SlidingWindowStore
└── factory.py            # Factory: cria qualquer limiter por nome
main.py                   # Simulação comparativa entre algoritmos
tests/
├── test_token_bucket.py
├── test_sliding_window.py
└── test_factory.py
docs/
├── index.html            # Diagrama visual interativo
└── decisions/
    └── 001-token-bucket.md  # ADR — decisões e trade-offs
```

---

## Stack

- Python 3.12
- Sem dependências externas
- `uv` para gerenciamento de ambiente

---

## Roadmap

- [x] Token Bucket
- [x] Sliding Window Log
- [x] Interface unificada (`RateLimiter` base class)
- [x] Factory pattern: trocar algoritmo sem mudar código cliente
- [x] Simulação comparativa entre algoritmos
- [ ] Leaky Bucket
- [ ] Análise de trade-offs com exemplos reais
