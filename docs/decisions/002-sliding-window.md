# Sliding Window Log
> 2026-04-05

## Contexto
Token Bucket controla volume médio, mas permite burst. Quando precisamos garantir que o cliente não ultrapasse o limite dentro de qualquer janela de tempo (não só em média), um algoritmo com memória de timestamps é melhor.

## Decisão
Sliding Window: registra o timestamp/now() de cada request aceito. A cada novbo request, descarta os timestamps fora da janela e conta os que restam. Se a contagem estiver abaixo do limite, aceita e registra.

```
janela = [agora - window_seconds, agora]
requests_válidos = timestamps dentro da janela
aceita se len(requests_válidos) < capacity
```

## Trade-offs

### Vantagens
- Sem burst: o limite é exato dentro de qualquer janela de `window_seconds`
- Histórico auditável — os timestamps ficam registrados
- Comportamento previsível e fácil de raciocinar

### Desvantagens
- Memória cresce com o volume de requests (O(n) por usuário)
- Mais caro por request do que Token Bucket (limpeza + contagem a cada chamada)
- Não distingue "limite atingido agora" de "limite atingido há 59s" — o retry não é óbvio para o cliente

## Quando usar
- Quando burst é inaceitável — ex: APIs de pagamento, envio de e-mail, operações com custo fixo por chamada
- Quando precisamos de auditoria de acesso por janela de tempo
- Quando a precisão do limite importa mais que o custo de memória

## Quando NÃO usar
- Sistemas com volume muito alto de requests por usuário — a lista de timestamps cresce indefinidamente
- Quando a latência por request precisa ser mínima — a limpeza da janela tem custo
- Quando o limite é em taxa de saída uniforme, não em contagem — use Leaky Bucket

## Comparação com Token Bucket

| | Token Bucket | Sliding Window Log |
|---|---|---|
| Burst permitido | Sim | Não |
| Memória por usuário | O(1) | O(n) — cresce com requests |
| Custo por request | O(1) | O(n) — limpeza da janela |
| Auditável por timestamp | Não | Sim |
| Limite exato por janela | Não (média) | Sim |

## Onde vive no sistema
Mesmo problema do Token Bucket: estado em memória não funciona em múltiplos workers. Em produção, os timestamps precisariam ser armazenados em Redis com TTL igual a `window_seconds`.

---
*Decisões adiadas: compressão de timestamps, fixed window como alternativa mais barata, estado distribuído*
