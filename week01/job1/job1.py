#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装并使用 requests、bs4 库，爬取猫眼电影（）的前 10 个电影名称、
电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

import constants


def get_movies_info(url: str, headers: dict, cookies: dict, params: tuple) -> list:
    movies_list = []

    # Use requests and bs4 libraries to parse source code
    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    bs_info = bs(response.text, 'html.parser')

    # Traverse to get movie name, movie type and release time
    movie_nums = 0
    for tag in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
        # Movie details can be obtained directly on the first page
        movie_name = tag.find('span', attrs={'class': 'name'}).text
        release_time = re.sub(r'[^\w-]', '',
                              tag.find('div', attrs={'class': 'movie-hover-brief'}).contents[2])
        movie_type = re.sub(r'[^\w／]', '',
                            tag.find_all('div', attrs={'class': 'movie-hover-title'})[1].contents[2])

        # Only take up to 10 movies
        movie_nums += 1
        movies_list.append((movie_nums, movie_name, movie_type, release_time))
        if movie_nums >= 10:
            break

    return movies_list


def _write_to_csv(movies_list: list):
    movie_info = pd.DataFrame(data=movies_list)
    movie_info.to_csv('./job1_output_maoyan_top10.csv', encoding='utf8',
                      index=False, header=['排名', '电影名称', '电影类型', '上映时间'])


if __name__ == '__main__':
    url_maoyan = "https://maoyan.com/films?showType=3"
    headers = constants.HEADERS
    params = constants.PARAMS
    cookies = constants.COOKIES

    movies_infos = get_movies_info(url_maoyan, headers=headers, cookies=cookies, params=params)
    if movies_infos:
        _write_to_csv(movies_infos)
    else:
        print("No valid information is crawled")
