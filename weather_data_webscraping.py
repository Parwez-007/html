from bs4 import BeautifulSoup

import io

import numpy as np
import pandas as pd

import requests
import re

# url of data source
URL = 'https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data'

# to get location of weather station
TITLE_PATTERN = re.compile("View (?P<location_>.*) data")

# to set up the dataframe for the data
colNames = ('year', 'month', 'tempMax', 'tempMin', 'airFrost', 'rainfall', 'sunshine')
commentLines = 5
header = 2


def get_soup(link: str) -> BeautifulSoup:
    with requests.get(link, headers={'User-Agent': 'requests', "Accept-Encoding": 'gzip'}) as r:
        _page_soup = BeautifulSoup(r.content, "html.parser")
    return _page_soup


def get_details(_soup: BeautifulSoup) -> list:
    _details = []
    _container = _soup.find(class_='article-body')

    _cards = _container.findAll('a')

    for _card in _cards:
        m = TITLE_PATTERN.match(_card.get('title'))
        _location = m.group('location_')
        _url = _card.get('href')
        _details.append((_location, _url))
    return _details


def clean_and_parse_data(link: str) -> pd.DataFrame:
    _file = io.StringIO(requests.get(link).text)

    df = pd.read_csv(_file,
                     skiprows=commentLines + header,
                     header=None,
                     names=colNames,
                     delimiter=' ',
                     skipinitialspace=True)
    df = df.replace('---', np.nan).replace(r'\*', '', regex=True)
    df['sunshine'] = df['sunshine'].replace(r'\W+', '', regex=True)

    return df


def weather_data(link: str):
    soup_ = get_soup(link)

    details_list = get_details(soup_)

    for _detail in details_list:
        print(f"This is for the region: {_detail[0]}")
        _df = clean_and_parse_data(_detail[1])
        print(_df)
        print()
    return


# print(weather_data(URL))


# to run the code for each station separately
def station_details(link: str) -> list:
    soup_ = get_soup(link)

    details_list = get_details(soup_)

    return details_list


def get_weather_data(detail: tuple) -> pd.DataFrame:
    print(f"This is for the region {detail[0]}")
    _df = clean_and_parse_data(detail[1])
    print(_df)
    print()
    return


# example
details = station_details(URL)

for i in details:
    get_weather_data(i)

































#
# excelfile_ = pd.read_csv("https://environment.data.gov.uk/flood-monitoring/archive/readings-full-2021-01-23.csv",
#                          usecols=['dateTime', 'date', 'stationReference', 'parameter', 'unitName', 'valueType', 'value'])
#
# df = excelfile_.loc[excelfile_['parameter'] == 'rainfall']
# df = df.loc[df['stationReference'] != '3404']
# # df = df.drop(df.loc[df['stationReference'] != '3404'], inplace=True)
#
# df = df.sort_values(by=['stationReference'])
# # if [df['stationReference'] != '3404']:
# df = df.astype({'value': 'float64'})
# # df = df['value'].to_numeric()
# # print(type(df))
# # print(df)
# # print(df.columns)
# df1 = df.groupby(['stationReference']).value.sum()
#
# pd.set_option('display.max_columns', None)
#
# print(df1)
# # print(df.dtypes)
# #
# # # print()
# # print(df1)
