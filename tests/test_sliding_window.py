from src.sliding_window import SlidingWindowStore

store = SlidingWindowStore(capacity=2, window_seconds=60)


def test_permite_dentro_do_limite():
    # Espera True
    assert store.is_allowed("1")
    assert store.is_allowed("2")
    assert store.is_allowed("3")


def test_barra_alem_do_limite():
    store.is_allowed("1")
    store.is_allowed("1")
    assert not store.is_allowed("1")
