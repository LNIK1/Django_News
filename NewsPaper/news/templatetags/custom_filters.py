from django import template

register = template.Library()

CENSOR_WORDS = [
    "суета",
    "общества",
    "элементом",
    "концепция",
    "интерпретировать",
    "новость"
]


@register.filter()
def censor(value: str):
    """
    :param value: - строка
    """

    result = ""

    value_split = value.split()

    for val in value_split:
        symbol = ""
        if ',' in val or '.' in val:
            val_ = value[:-1]
            symbol = value[-1]
        else:
            val_ = val

        if val_ in CENSOR_WORDS:
            censored_val = val_[:1] + ("*" * (len(val_) - 1))
            result = result + censored_val + symbol
        else:
            result = result + val_ + symbol

        result = result + " "

    return result[:-1]