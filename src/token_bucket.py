from dataclasses import dataclass, field
from time import time

from src.rate_limiter import RateLimiter


@dataclass
class TokenBucket(RateLimiter):
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

    @property
    def available_tokens(self) -> float:
        return self.tokens

    def is_allowed(self) -> bool:
        """Verifica tokens disponíveis. Consome 1 tiver"""
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def _refill(self) -> None:
        """Calcula quantos tokens foram gerados desde o último refil"""
        now = time()
        new_tokens = (now - self.last_refill) * self.refill_rate
        self.tokens += new_tokens
        if self.tokens >= self.capacity:
            self.tokens = self.capacity
        self.last_refill = now


class TokenBucketStore:
    def __init__(self, capacity: int, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets = {}

    def is_allowed(self, identifier: str):
        if identifier not in self._buckets:
            bucket = TokenBucket(self.capacity, self.refill_rate)
            self._buckets[identifier] = bucket
        return self._buckets[identifier].is_allowed()
