# Malagasy (mg) number-to-words normalization for the XTTS tokenizer.
#
# `num2words` does not support Malagasy, so this module provides the same
# role as `zh_num2words.py` for Chinese: it converts digits found in a text
# into Malagasy words (cardinals, ordinals, decimals and common currencies).
#
# Conventions used:
#   - tens and units are joined with "amby" (21 -> "iraika amby roapolo")
#   - hundreds are "<digit>anjato" (200 -> "roanjato"), 100 -> "zato"
#   - 1 000 -> "arivo", 1 000 000 -> "tapitrisa", 1 000 000 000 -> "lavitrisa"
#   - ordinals 1..10 have dedicated forms, larger ones are "faha" + cardinal
#   - decimals are read as "<int part> point <digit> <digit> ..."
#   - $ -> "dolara", EUR -> "euro", GBP -> "paona", Ar/ariary -> "ariary"

import re

_ONES = [
    "aotra",
    "iraika",
    "roa",
    "telo",
    "efatra",
    "dimy",
    "enina",
    "fito",
    "valo",
    "sivy",
]

_TENS = {
    2: "roapolo",
    3: "telopolo",
    4: "efaimpolo",
    5: "dimampolo",
    6: "enimpolo",
    7: "fitopolo",
    8: "valopolo",
    9: "sivifolo",
}

_HUNDREDS = {
    2: "roanjato",
    3: "telonjato",
    4: "efanjato",
    5: "dimanjato",
    6: "eninjato",
    7: "fitonjato",
    8: "valonjato",
    9: "sivinjato",
}

_ORDINALS_1_10 = [
    "voalohany",
    "faharoa",
    "fahatelo",
    "fahaefatra",
    "fahadimy",
    "fahaenina",
    "fahafito",
    "fahavalo",
    "fahasivy",
    "fahafolo",
]

_BIG_UNITS = [
    (10**9, "lavitrisa"),
    (10**6, "tapitrisa"),
    (10**3, "arivo"),
]


def number_to_words(n: int) -> str:
    """Cardinal form of a non-negative integer in Malagasy."""
    n = int(n)
    if n < 0:
        return "miinus " + number_to_words(-n)
    if n < 10:
        return _ONES[n]
    if n < 100:
        t, u = divmod(n, 10)
        if u == 0:
            return "folo" if t == 1 else _TENS[t]
        tens = "folo" if t == 1 else _TENS[t]
        return f"{_ONES[u]} amby {tens}"
    if n < 1000:
        h, rest = divmod(n, 100)
        head = "zato" if h == 1 else _HUNDREDS[h]
        if rest == 0:
            return head
        return f"{head} {number_to_words(rest)}"
    for value, unit in _BIG_UNITS:
        if n >= value:
            q, rest = divmod(n, value)
            head = unit if q == 1 else number_to_words(q) + " " + unit
            if rest:
                return f"{head} {number_to_words(rest)}"
            return head
    raise ValueError(f"Number too large: {n}")


def ordinal_to_words(n: int) -> str:
    """Ordinal form of a positive integer in Malagasy."""
    n = int(n)
    if n <= 0:
        raise ValueError(f"No ordinal for {n}")
    if n <= 10:
        return _ORDINALS_1_10[n - 1]
    return "faha" + number_to_words(n).replace(" ", "")


_comma_number_re = re.compile(r"\b\d{1,3}(,\d{3})+\b")
_dot_number_re = re.compile(r"\b\d{1,3}(\.\d{3})+\b")
_space_number_re = re.compile(r"\b\d{1,3}( \d{3})+\b")
_decimal_re = re.compile(r"\b(\d+)[.,](\d+)\b")
_ordinal_re = re.compile(r"\b([0-9]+)(na|lahy)\b", re.IGNORECASE)
_number_re = re.compile(r"\b[0-9]+\b")

_currency_prefix_re = re.compile(r"(?P<cur>\$|£|€)\s*(?P<amount>[0-9]+(?:[.,][0-9]+)?)", re.IGNORECASE)
_currency_suffix_re = re.compile(r"(?P<amount>[0-9]+(?:[.,][0-9]+)?)\s*(?P<cur>\$|£|€|\bAr\b|\bariary\b)", re.IGNORECASE)

_CURRENCY_WORDS = {
    "$": "dolara",
    "£": "paona",
    "€": "euro",
    "ar": "ariary",
    "ariary": "ariary",
}


def _strip_thousand_separators(text: str) -> str:
    text = _comma_number_re.sub(lambda m: m.group(0).replace(",", ""), text)
    text = _dot_number_re.sub(lambda m: m.group(0).replace(".", ""), text)
    text = _space_number_re.sub(lambda m: m.group(0).replace(" ", ""), text)
    return text


def _expand_decimal(m) -> str:
    int_part, dec_part = m.group(1), m.group(2)
    digits = " ".join(_ONES[int(d)] for d in dec_part)
    return f"{number_to_words(int(int_part))} point {digits}"


def _expand_ordinal(m) -> str:
    return ordinal_to_words(int(m.group(1)))


def _expand_currency(m) -> str:
    cur = m.group("cur").lower()
    amount = m.group("amount")
    if "." in amount or "," in amount:
        int_part, dec_part = re.split(r"[.,]", amount, maxsplit=1)
        digits = " ".join(_ONES[int(d)] for d in dec_part)
        words = f"{number_to_words(int(int_part))} point {digits}"
    else:
        words = number_to_words(int(amount))
    return f" {words} {_CURRENCY_WORDS[cur]} "


class TextNorm:
    """Normalize digits in a Malagasy text to Malagasy words."""

    def __call__(self, text: str) -> str:
        text = _strip_thousand_separators(text)
        text = _currency_suffix_re.sub(_expand_currency, text)
        text = _currency_prefix_re.sub(_expand_currency, text)
        text = _decimal_re.sub(_expand_decimal, text)
        text = _ordinal_re.sub(_expand_ordinal, text)
        text = _number_re.sub(lambda m: number_to_words(int(m.group(0))), text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)
        return text.strip()


def test_mg_num2words():
    tn = TextNorm()
    cases = [
        ("0", "aotra"),
        ("7", "fito"),
        ("10", "folo"),
        ("11", "iraika amby folo"),
        ("21", "iraika amby roapolo"),
        ("99", "sivy amby sivifolo"),
        ("100", "zato"),
        ("205", "roanjato dimy"),
        ("1000", "arivo"),
        ("2500", "roa arivo dimanjato"),
        ("1000000", "tapitrisa"),
        ("Jereo ny 3na andro.", "Jereo ny fahatelo andro."),
        ("Misy 12,5 segondra.", "Misy roa amby folo point dimy segondra."),
        ("Misy $20.", "Misy roapolo dolara."),
        ("Izany dia 20€.", "Izany dia roapolo euro."),
        ("100 000 ariary.", "zato arivo ariary."),
    ]
    for raw, expected in cases:
        out = tn(raw)
        assert out == expected, f"'{raw}' -> '{out}' (expected '{expected}')"
    assert number_to_words(42) == "roa amby efaimpolo"
    assert ordinal_to_words(1) == "voalohany"
    assert ordinal_to_words(2) == "faharoa"
    assert ordinal_to_words(10) == "fahafolo"


if __name__ == "__main__":
    test_mg_num2words()
    print("mg_num2words OK")
