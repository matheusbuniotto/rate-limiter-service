import random

from src.factory import create_limiter


def simulate(algorithm: str, n_users: int, n_requests: int, limit: int, seed: int = 42):
    rng = random.Random(seed)
    limiters = {
        user_id: create_limiter(algorithm, capacity=limit, refill_rate=1 / 60)
        if algorithm == "token_bucket"
        else create_limiter(algorithm, capacity=limit, window_seconds=60)
        for user_id in range(n_users)
    }

    total_req = total_ok = total_block = 0
    for user_id, limiter in limiters.items():
        n = rng.randint(1, n_requests)
        allowed_number = 0
        for _ in range(n):
            allowed = limiter.is_allowed(user_id)
            allowed_number += allowed
        total_req += n
        total_ok += allowed_number
        total_block += n - allowed_number

    return {
        "algorithm": algorithm,
        "total_req": total_req,
        "ok": total_ok,
        "blocked": total_block,
    }


def compare(n_users: int = 100, n_requests: int = 20, limit: int = 10, seed: int = 42):
    algorithms = ["token_bucket", "sliding_window"]
    results = [simulate(algo, n_users, n_requests, limit, seed) for algo in algorithms]

    print(f"\n{'=' * 55}")
    print(f"  Comparativo — {n_users} usuários, limite {limit} req/min")
    print(f"{'=' * 55}")
    print(
        f"{'Algoritmo':<20} {'Requests':>8} {'OK':>8} {'Bloqueado':>10} {'Block%':>7}"
    )
    print(f"{'-' * 55}")
    for r in results:
        pct = r["blocked"] / r["total_req"] * 100
        print(
            f"{r['algorithm']:<20} {r['total_req']:>8} {r['ok']:>8} {r['blocked']:>10} {pct:>6.1f}%"
        )
    print(f"{'=' * 55}\n")


if __name__ == "__main__":
    compare()
