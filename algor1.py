# !/usr/bin/env python
# coding=utf-8
# from functools import reduce
# import json
# import os
# import numpy as np
import pytz
import datetime

fixLen = 0

XTIMES = {
    8: [6000, 9999, 1],
    9: [10000, 12999, 1],
    10: [13000, 14999, 0],
    13: [15000, 19999, 0],
    15: [20000, 24999, 0],
    17: [25000, 29999, 0],
    19: [30000, 34999, 0],
    21: [35000, 39999, 1],
}

def main():
    # A = {'407.07964602': 9, '53.09745133': 10, '725.66371681': 10, '371.68141593': 12, '752.21238938': 12,
    #      '469.02654867': 13, '230.08849558': 14, '325.66371681': 14, '398.2300885': 15, '336.28318584': 15,
    #      '309.73451327': 16, '170.79646018': 18, '104.42477876': 18, '95.575221239': 18, '159.2920354': 18,
    #      '517.69911504': 18, '256.63716814': 20, '353.98230088': 20}

    # B = [3074.34, 1879.65, 4659.29, 4955.75, 4601.77, 4460.18, 5132.74, 2867.26, 7256.64, 4659.29, 3663.72,
    #      4559.29, 5973.45, 7079.65, 3221.24, 1720.35, 5044.25, 6097.35, 9026.55, 530.97]

    # fixLen = max(map(lambda x: len(x.partition('.')[2]), A.keys()))

    # def acc(d, k):
    #     d[k[0] + k[2].ljust(fixLen, '0')] = A[''.join(k)]
    #     return d
    # _A = reduce(acc, map(lambda x: x.partition('.'), A.keys()), {})
    # print(_A)
    tz = pytz.timezone('Asia/Shanghai')
    local_time_str = datetime.datetime.now(tz).strftime("%H")
    print(local_time_str)
    time_bj = datetime.datetime.today() + datetime.timedelta(hours=8)
    now = time_bj.strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    xtime = None
    if XTIMES.keys().__contains__(xtime):
        print(hour, XTIMES[hour][0])

def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
