import re
import requests

import pandas as pd

from datetime import datetime


main_url = "http://isut.plovdiv.bg:998/" \
           "user/classes/__regs_list_sr.php?submode=5&userid=8"


def download_dataset() -> None:
    df = get_all_data()
    persist_df(df)


def get_all_data() -> pd.DataFrame:
    print(f"Fetching main url..")
    response = requests.get(main_url)
    pages = get_all_pages(response.text)
    print(f"All available pages: {pages}")
    page_dfs = list()
    for page in pages:
        print(f"Processing page {str(page)}...")
        page_html = get_page_contents(page)
        df = extract_df_from_page(page_html)
        page_dfs.append(df)
        print("Done.")
    df = pd.concat(page_dfs, ignore_index=True)
    return df


def get_all_pages(page_html: str) -> set:
    matches = re.findall(r"selectPage\((\d+)\)", page_html)
    pages = set([int(m) for m in matches])
    pages.update({1})  # main_url default to page 1 and not shown in the list
    return pages


def get_page_contents(page: int = 1) -> str:
    headers = {"Origin": "http://isut.plovdiv.bg:998",
               "Referer": "http://isut.plovdiv.bg:998/"
                          "registers.php?currentpage=3&submode=5",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept": "*/*",
               "User-Agent": "Chrome/36.500"
               }
    body = f"&page={str(page)}"
    response = requests.post(main_url, headers=headers, data=body)
    response.encoding = "utf-8"
    return response.text


def extract_df_from_page(page_html: str) -> pd.DataFrame:
    df = pd.read_html(page_html)[0]
    return df


def persist_df(df: pd.DataFrame, name: str = "isut-df") -> None:
    timestamp = datetime.now().strftime("%d%m%Y-%H-%M")
    df.to_pickle(f"{name}-{timestamp}.pkl")
