# Token Bucket
> 2026-04-04

## Contexto
Quando precisamos limitar o número de requests aceitos pela API para não explodir a capacidade do servidor, além de controlar e nos proteger contra ataques de DoS.

## Decisão
Token Bucket como primeiro algoritmo de rate limiting. É um dos algoritmos mais simples que resolve o problema sem agregar muita complexidade sistêmica.

## Trade-offs

### Vantagens
- Simplicidade de implementação e manutenção
- Controle granular (capacity + refill_rate independentes)
- Fácil de alterar parâmetros sem mudar a interface

### Desvantagens
- Permite burst: bucket cheio = muitas requisições de uma vez (pode não ser desejado)
- Não diferencia picos de uso legítimos de ataques
- Comportamento uniforme — não adapta à carga real do sistema

## Quando usar
Quando precisamos de uma forma simples de controlar o volume de requests, sem necessidade de janela de tempo precisa ou análise de padrão de uso.

## Quando NÃO usar
- Quando o padrão de burst é problemático — se o bucket está cheio e o cliente disparar tudo ao mesmo tempo, o downstream precisa absorver o pico. Se não suportar (ex: banco com limite rígido de queries/s), token bucket pode derrubar o serviço mesmo dentro do limite configurado.
- Quando precisamos de fairness por janela de tempo — token bucket não garante "exatamente 10/minuto", só garante que a média respeita a taxa.
- Quando o comportamento precisa ser auditável por timestamp — token bucket não registra histórico de requisições.

## Burst — exemplo concreto
Com `capacity=10` e `refill_rate=1/s`, um cliente inativo por 10s volta com bucket cheio e pode disparar 10 requests instantaneamente. O servidor precisa suportar esse pico.

## Onde vive no sistema
O bucket precisa viver no ponto de entrada dos requests — load balancer ou API gateway. Se cada servidor mantiver seu próprio estado em memória, um cliente com 3 servidores disponíveis efetivamente tem 3x o limite configurado. Estado compartilhado é obrigatório em produção — o que exige Redis ou similar (decisão adiada neste projeto).

## Alternativas consideradas
- **Sliding Window Log** — melhor quando precisamos de controle preciso por janela de tempo (sem burst)
- **Leaky Bucket** — melhor quando a taxa de saída precisa ser estritamente uniforme (ex: proteção de downstream)

---
*Decisões adiadas: thread-safety, clock skew, estado distribuído (Redis)*
