from dataclasses import dataclass, field
from time import time


@dataclass
class TokenBucket:
    """Token Bucket rate limiter.

    Gera tokens a uma taxa constante. Requisições consomem tokens.
    Se vazio => rejeita.
    """

    capacity: int
    refill_rate: float
    tokens: float = field(init=False)
    last_refill: float = field(init=False)

    def __post_init__(self):
        self.tokens = self.capacity
        self.last_refill = time()

    def is_allowed(self) -> bool:
        """Verifica tokens disponíveis. Consome 1 tiver"""
        self._refill()
        if self.tokens > 0:
            self.tokens -= 1
            return True
        else:
            return False

    def _refill(self) -> None:
        """Calcula quantos tokens foram gerados desde o último refill."""
        new_tokens = (time() - self.last_refill) * self.refill_rate
        self.tokens += new_tokens
        if self.tokens >= self.capacity:
            self.tokens = self.capacity
        self.last_refill = time()
