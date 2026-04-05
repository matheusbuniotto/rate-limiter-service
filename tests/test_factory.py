import pytest

from src.factory import create_limiter
from src.sliding_window import SlidingWindowStore
from src.token_bucket import TokenBucketStore


def test_factory_create_tb():
    limiter = create_limiter("token_bucket", capacity=10, refill_rate=1)
    assert isinstance(limiter, TokenBucketStore)


def test_factory_create_sw():
    limiter = create_limiter("sliding_window", capacity=10, window_seconds=60)
    assert isinstance(limiter, SlidingWindowStore)


def test_factory_invalido():
    with pytest.raises(ValueError):
        create_limiter("invalido")
