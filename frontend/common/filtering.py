import re
import pandas as pd

from typing import Tuple, Callable


infra_strings = ["ЕВН", "Община Пловдив", "Електроразпределение",
                 "БТК", "МЕГАЛАН"]

infra_dec = ["ел", "вик", "кабелни мрежи", "топл", "топлопровод",
             "елзахранване", "топлоснабдяване", "газоснабдяване", "водопровод",
             "пътна", "ЕЛЕКТРОЗАХРАНВАНЕ", "улица", "канал", "пътища",
             "кабелна мрежа", "оптични мрежи"]


def infra_filter(row: pd.Series) -> bool:
    if type(row["Възложител"]) == str:
        for string in infra_strings:
            hit = re.search(rf"{string}", row["Възложител"], re.IGNORECASE)
            if hit:
                return True
    if type(row["Име на обект"]) == str:
        for string in infra_dec:
            hit = re.search(rf"{string}", row["Име на обект"], re.IGNORECASE)
            if hit:
                return True
    return False


def municipality_filter(row: pd.Series) -> bool:
    if type(row["Възложител"]) == str:
        hit = re.search(rf"община пловдив", row["Възложител"], re.IGNORECASE)
        if hit:
            return True
    return False


def apply_filter_to_df(input_df: pd.DataFrame,
                       filter_func: Callable) -> pd.DataFrame:
    filtered_column = input_df.apply(filter_func, axis=1)
    return filtered_column


def get_infra_other_split(input_df: pd.DataFrame,
                          start_date: str,
                          end_date: str,
                          filter_func: Callable) -> Tuple[pd.DataFrame,
                                                          pd.DataFrame]:
    term_df = input_df[(input_df['Дата'] > start_date) &
                       (input_df['Дата'] < end_date)]
    filtered = apply_filter_to_df(input_df, filter_func)

    infra_df = term_df[filtered]
    others = term_df[~filtered]
    return infra_df, others
