from bobotinho.utils.time import datetime, timeago


def test_timeago_with_minimum_short() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 12, 30, 12, 0, 0), now=now).humanize(minimum="d", short=True) == "1d"
    assert timeago(datetime(2022, 12, 31, 11, 0, 0), now=now).humanize(minimum="h", short=True) == "1h"
    assert timeago(datetime(2022, 12, 31, 11, 59, 0), now=now).humanize(minimum="min", short=True) == "1min"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59), now=now).humanize(minimum="s", short=True) == "1s"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59, 999), now=now).humanize(minimum="s", short=True) == "pouco tempo"


def test_timeago_with_minimum_full() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 12, 30, 12, 0, 0), now=now).humanize(minimum="d", short=False) == "1 dia"
    assert timeago(datetime(2022, 12, 31, 11, 0, 0), now=now).humanize(minimum="h", short=False) == "1 hora"
    assert timeago(datetime(2022, 12, 31, 11, 59, 0), now=now).humanize(minimum="min", short=False) == "1 minuto"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59), now=now).humanize(minimum="s", short=False) == "1 segundo"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59, 999), now=now).humanize(minimum="s", short=True) == "pouco tempo"


def test_timeago_with_minimum_plural() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 12, 29, 12, 0, 0), now=now).humanize(minimum="d", short=False) == "2 dias"
    assert timeago(datetime(2022, 12, 31, 10, 0, 0), now=now).humanize(minimum="h", short=False) == "2 horas"
    assert timeago(datetime(2022, 12, 31, 11, 58, 0), now=now).humanize(minimum="min", short=False) == "2 minutos"
    assert timeago(datetime(2022, 12, 31, 11, 59, 58), now=now).humanize(minimum="s", short=False) == "2 segundos"


def test_timeago_with_minimum() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(minimum="d") == "77 dias"
    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(minimum="h") == "77 dias"
    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(minimum="min") == "77 dias"
    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(minimum="s") == "77 dias"

    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(minimum="d") == "pouco tempo"
    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(minimum="h") == "8 horas"
    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(minimum="min") == "8 horas"
    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(minimum="s") == "8 horas"

    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(minimum="d") == "pouco tempo"
    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(minimum="h") == "pouco tempo"
    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(minimum="min") == "11 minutos"
    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(minimum="s") == "11 minutos"

    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(minimum="d") == "pouco tempo"
    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(minimum="h") == "pouco tempo"
    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(minimum="min") == "pouco tempo"
    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(minimum="s") == "38 segundos"

    assert timeago(datetime(2022, 12, 31, 12, 0, 0), now=now).humanize() == "pouco tempo"
    assert timeago(datetime.utcnow()).humanize() == "pouco tempo"


def test_timeago_with_precision_short() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 12, 30, 12, 0, 0), now=now).humanize(precision=1, short=True) == "1d"
    assert timeago(datetime(2022, 12, 31, 11, 0, 0), now=now).humanize(precision=1, short=True) == "1h"
    assert timeago(datetime(2022, 12, 31, 11, 59, 0), now=now).humanize(precision=1, short=True) == "1min"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59), now=now).humanize(precision=1, short=True) == "1s"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59, 999), now=now).humanize(precision=1, short=True) == "pouco tempo"


def test_timeago_with_precision_full() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 12, 30, 12, 0, 0), now=now).humanize(precision=1, short=False) == "1 dia"
    assert timeago(datetime(2022, 12, 31, 11, 0, 0), now=now).humanize(precision=1, short=False) == "1 hora"
    assert timeago(datetime(2022, 12, 31, 11, 59, 0), now=now).humanize(precision=1, short=False) == "1 minuto"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59), now=now).humanize(precision=1, short=False) == "1 segundo"
    assert timeago(datetime(2022, 12, 31, 11, 59, 59, 999), now=now).humanize(precision=1, short=True) == "pouco tempo"


def test_timeago_with_precision_plural() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 12, 29, 12, 0, 0), now=now).humanize(precision=1, short=False) == "2 dias"
    assert timeago(datetime(2022, 12, 31, 10, 0, 0), now=now).humanize(precision=1, short=False) == "2 horas"
    assert timeago(datetime(2022, 12, 31, 11, 58, 0), now=now).humanize(precision=1, short=False) == "2 minutos"
    assert timeago(datetime(2022, 12, 31, 11, 59, 58), now=now).humanize(precision=1, short=False) == "2 segundos"


def test_timeago_with_precision() -> None:
    now = datetime(2022, 12, 31, 12, 0, 0)

    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(precision=1) == "77 dias"
    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(precision=2) == "77 dias 1 hora"
    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(precision=3) == "77 dias 1 hora 29 minutos"
    assert timeago(datetime(2022, 10, 15, 10, 30, 59), now=now).humanize(precision=4) == "77 dias 1 hora 29 minutos 1 segundo"

    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(precision=1) == "8 horas"
    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(precision=2) == "8 horas 11 minutos"
    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(precision=3) == "8 horas 11 minutos 38 segundos"
    assert timeago(datetime(2022, 12, 31, 3, 48, 22), now=now).humanize(precision=4) == "8 horas 11 minutos 38 segundos"

    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(precision=1) == "11 minutos"
    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(precision=2) == "11 minutos 38 segundos"
    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(precision=3) == "11 minutos 38 segundos"
    assert timeago(datetime(2022, 12, 31, 11, 48, 22), now=now).humanize(precision=4) == "11 minutos 38 segundos"

    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(precision=1) == "38 segundos"
    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(precision=2) == "38 segundos"
    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(precision=3) == "38 segundos"
    assert timeago(datetime(2022, 12, 31, 11, 59, 22), now=now).humanize(precision=4) == "38 segundos"

    assert timeago(datetime(2022, 12, 31, 12, 0, 0), now=now).humanize() == "pouco tempo"
    assert timeago(datetime.utcnow()).humanize() == "pouco tempo"
