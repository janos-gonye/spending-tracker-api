from app.categories.models import Category
from app.transactions.models import Transaction


def min_(iterable):
    if len(iterable) == 0: return 0
    return min(iterable)


def max_(iterable):
    if len(iterable) == 0: return 0
    return max(iterable)


def count(iterable):
    return len(iterable)


def mean(iterable):
    if len(iterable) == 0: return 0
    return sum(iterable) / len(iterable)


MAPPER = {
    'min': min_,
    'max': max_,
    'sum': sum,
    'mean': mean,
    'count': count,
}


def get_statistics(user):
    categories = Category.query.filter_by(user_id=user.id,
                                          parent_id=None).all()
    statistics = []
    for category in categories:
        statistics.append(_get_statistics(category=category))
    return statistics


def _get_statistics(category):
    data = {}
    data[category.title] = {}
    calculations = _calculate(category)
    for key, value in calculations.items():
        data[category.title][key] = value
    data[category.title]['children'] = []
    for child in category.children:
        data[category.title]['children'].append(_get_statistics(category=child))
    return data


def _get_transactions(category):
    transactions = Transaction.query.filter_by(category_id=category.id).all()
    for child in category.children:
        transactions += _get_transactions(category=child)
    return transactions


def _calculate(category):
    transactions = _get_transactions(category=category)
    transactions = list(map(lambda t: t.amount, transactions))
    result = {}
    for key, func in MAPPER.items():
        result[key] = func(transactions)
    return result
