#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
あまりに暑いので，140年分の気温をProphetで分析した
https://qiita.com/haltaro/items/9c68f0914677bb3a629c

で使用する気象データをダウンロードするスクリプトを作成
"""

from datetime import date
import urllib.request
import lxml.html


def encode_data(data):
    return urllib.parse.urlencode(data).encode(encoding='ascii')

def get_phpsessid():
    URL="http://www.data.jma.go.jp/gmd/risk/obsdl/index.php"
    xml = urllib.request.urlopen(URL).read().decode("utf-8")
    tree = lxml.html.fromstring(xml)
    return tree.cssselect("input#sid")[0].value

def download_hourly_csv(phpsessid, begin_date, end_date):
    params = {
        "PHPSESSID": phpsessid,
        # 共通フラグ
        "rmkFlag": 1,        # 利用上注意が必要なデータを格納する
        "disconnectFlag": 1, # 観測環境の変化にかかわらずデータを格納する
        "csvFlag": 1,        # すべて数値で格納する
        "ymdLiteral": 1,     # 日付は日付リテラルで格納する
        "youbiFlag": 0,      # 日付に曜日を表示する
        "kijiFlag": 0,       # 最高・最低（最大・最小）値の発生時刻を表示
        # 時別値データ選択
        "aggrgPeriod": 1,
        "stationNumList": '["s47662"]',      # 東京
        "elementNumList": '[["201",""], ["202",""], ["203",""]]', # 日平均気温、日最高気温、日最低気温
        "ymdList": '["%d", "%d", "%d", "%d", "%d", "%d"]' % (
            begin_date.year,  end_date.year,
            begin_date.month, end_date.month,
            begin_date.day,   end_date.day),       # 取得する期間
        "jikantaiFlag": 0,        # 特定の時間帯のみ表示する
        "jikantaiList": '[]', # デフォルトは全部
        "interAnnualFlag": 1,     # 連続した期間で表示する
        # 以下、意味の分からないフラグ類
        "optionNumList": [],
        "downloadFlag": "true",   # CSV としてダウンロードする？
        "huukouFlag": 0,
    }
    print(params)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    URL="http://www.data.jma.go.jp/gmd/risk/obsdl/show/table"

    req = urllib.request.Request(URL, data=encode_data(params), headers=headers)
    with urllib.request.urlopen(req) as res:
        csv = res.read()
        open("data/raw/data_%s.csv" % begin_date.year, "wb").write(csv)

    
if __name__ == "__main__":
    phpsessid = get_phpsessid()

    ranges = [
        {'s': 1872, 'e': 1879}, # 1870年代は1872年からしかデータがないらしい
        {'s': 1880, 'e': 1889},
        {'s': 1890, 'e': 1899},
        {'s': 1900, 'e': 1909},
        {'s': 1910, 'e': 1919},
        {'s': 1920, 'e': 1929},
        {'s': 1930, 'e': 1939},
        {'s': 1940, 'e': 1949},
        {'s': 1950, 'e': 1959},
        {'s': 1960, 'e': 1969},
        {'s': 1970, 'e': 1979},
        {'s': 1980, 'e': 1989},
        {'s': 1990, 'e': 1999},
        {'s': 2000, 'e': 2009},
        {'s': 2010, 'e': 2017}, # 
    ]
    for val in ranges:
        download_hourly_csv(phpsessid, date(val['s'], 1, 1), date(val['e'], 12, 31))

    