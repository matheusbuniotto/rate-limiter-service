from abc import ABC, abstractmethod


class RateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, identifier: str) -> bool: ...
