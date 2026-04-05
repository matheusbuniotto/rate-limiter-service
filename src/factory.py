from src.sliding_window import SlidingWindowStore
from src.token_bucket import TokenBucketStore


def create_limiter(algorithm: str, **kwargs):
    limiters = {
        "token_bucket": TokenBucketStore,
        "sliding_window": SlidingWindowStore,
    }

    limiter_class = limiters.get(algorithm)
    if limiter_class is None:
        raise ValueError(
            f"Algoritmo '{algorithm}' não encontrado. Opções: {list(limiters.keys())}"
        )

    return limiter_class(**kwargs)
