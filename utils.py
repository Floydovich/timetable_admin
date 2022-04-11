import requests
# from datetime import datetime

from constants import TERMS, DAYS

weeks = {f"Н{i}": f"Неделя {i}" for i in range(1, 3)}
days = {f"Д{i}": DAYS[i - 1].strip() for i in range(1, 6)}
classes = {f"П{i}": f"{i} занятие" for i in range(1, 7)}

trans_table = {
    "ро": "r",
    "(ро)": "r",
    "ко": "k",
    "(ко)": "k",
    "(1 подгруппа)": "s1",
    "(2 подгруппа)": "s2",
    "(архитек.)": "a",
    "(графики)": "g",
    "(промыш.)": "p"
}


def current_term():
    """
    Get the current month and use it to determine the term. Reverse the term order, so the months in second half
    of the year belong to the 1st term and the months in the first half belong to the 2nd term.
    :return: str
    """
    # current_month = datetime.now().month
    # term = TERMS[::-1][current_month // 6]
    term = TERMS[0]  # leave only the first term for now
    return term


def has_internet_connection():
    url = 'http://www.google.com/'
    timeout = 10
    try:
        requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError as ex:
        print(ex)
        return False
