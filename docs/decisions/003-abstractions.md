# Abstrações — RateLimiter ABC e Factory
> 2026-04-05

## Contexto
Com dois algoritmos implementados e um terceiro planejado, precisamos de uma forma de:
1. Garantir que todos os algoritmos respeitem a mesma interface
2. Permitir trocar o algoritmo sem alterar o código que o usa

## Decisões

### 1. RateLimiter — Abstract Base Class

```python
class RateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, identifier: str) -> bool: ...
```

`identifier` é a chave de isolamento: por usuário, por IP, por API key. O algoritmo não sabe o que é — só usa para separar estado.

**Por que ABC e não Protocol?**

| | ABC | Protocol |
|---|---|---|
| Enforcement | Em tempo de instanciação | Em tempo de checagem estática |
| Herança explícita | Obrigatória | Não — duck typing |
| Erro em runtime | Sim, se método não implementado | Não — falha silenciosamente |

ABC foi escolhido porque queremos erro em runtime claro se um novo algoritmo esquecer de implementar `is_allowed`. Protocol seria mais flexível, mas menos seguro para um projeto de aprendizado onde erros explícitos têm valor pedagógico.

### 2. Store — estado por usuário

Cada algoritmo tem duas classes: o algoritmo puro (ex: `TokenBucket`) e o store (ex: `TokenBucketStore`). O Store mantém um dict `identifier → instância` e delega para a instância correta.

```
TokenBucketStore
└── {user_id: TokenBucket, ...}
        └── is_allowed() → verifica e atualiza tokens
```

**Por que separar Store do algoritmo?**

- O algoritmo (`TokenBucket`) é testável em isolamento — sem dict, sem estado compartilhado
- O Store é o ponto de entrada da interface pública (`RateLimiter`)
- Facilita substituir a estratégia de armazenamento (dict → Redis) sem tocar no algoritmo

### 3. Factory — create_limiter()

```python
def create_limiter(algorithm: str, **kwargs) -> RateLimiter:
    limiters = {
        "token_bucket": TokenBucketStore,
        "sliding_window": SlidingWindowStore,
    }
    limiter_class = limiters.get(algorithm)
    if limiter_class is None:
        raise ValueError(f"Algoritmo '{algorithm}' inválido. Opções: {list(limiters.keys())}")
    return limiter_class(**kwargs)
```

**Por que dict em vez de if/elif?**

- Adicionar novo algoritmo = adicionar uma entrada no dict, não modificar a lógica de seleção
- Segue Open/Closed: aberto para extensão, fechado para modificação
- Lookup O(1) independente do número de algoritmos

**Por que `**kwargs` em vez de parâmetros fixos?**

Cada algoritmo tem parâmetros diferentes (`capacity + refill_rate` vs `capacity + window_seconds`). `**kwargs` passa tudo para o construtor sem a factory precisar conhecer os detalhes de cada um. A validação fica no `__init__` de cada classe — onde pertence.

## Trade-offs aceitos

- `**kwargs` perde type safety — erros de parâmetro aparecem em runtime, não no editor
- ABC exige herança explícita — menos flexível que Protocol para tipos externos
- Store em memória não é thread-safe — decisão adiada

---
*Próxima decisão: Leaky Bucket — como encaixar taxa de saída uniforme nessa interface*
