# Rate Limiter

Implementação de algoritmos de rate limiting em Python puro, focada em aprendizado de system design e engenharia.

Sem frameworks. Sem Redis. Só Python e lógica.

---

## Algoritmos

| Algoritmo | Status | Quando usar |
|---|---|---|
| Token Bucket | ✅ Implementado | Controle simples com burst permitido |
| Sliding Window Log | 🔜 Em breve | Janela de tempo precisa, sem burst |
| Leaky Bucket | 🔜 Em breve | Taxa de saída estritamente uniforme |

---

## Uso

```python
from src.token_bucket import TokenBucket

# 10 requests por minuto
limiter = TokenBucket(capacity=10, refill_rate=10/60)

if limiter.is_allowed():
    print("request permitido")
else:
    print("rate limit atingido")
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
└── token_bucket.py       # Token Bucket
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
- [ ] Sliding Window Log
- [ ] Leaky Bucket
- [ ] Interface unificada (`RateLimiter` base class)
- [ ] Testes comparativos entre algoritmos
- [ ] Análise de trade-offs com exemplos reais
