from collections import defaultdict
from urllib import parse
import re
import requests
from data import constants, wuxing_dict as fwd
import config
from config import MIN_SINGLE_NUM, MAX_SINGLE_NUM, SEX, THRESHOLD_SCORE
import urllib
from http import cookiejar
from urllib import request

TESTED_FILE = 'generated_names/bak/name_tested.txt'  # 已经在网站测试过的名字
RESULT_FILE = 'generated_names/bak/name_liu_6bihua.txt'  # 结果算到的好名字
SANCAI_FILE = 'data/sancai.txt'  # 三才五行参考结语
BAIJIAXING_FILE = 'data/baijiaxing.txt'  # 百家姓最佳搭配

word_wuxing_dict = dict()


def getTestedDict():
    """
    获取已经测试过的列表
    """
    already_tested_dict = dict()
    with open(TESTED_FILE, 'r', encoding='utf8') as f:
        # print(f.readline().strip())
        while True:
            line = f.readline().strip()
            lineData = line.split(',')
            if len(lineData) == 2:
                already_tested_dict[line.split(',')[0]] = line.split(',')[1]
            else:
                already_tested_dict[line.split(',')[0]] = 0
            if not line:
                break
    return already_tested_dict


def getFullWordcountDict():
    """获得每个字的实际笔画数量"""
    full_word_count_dict = dict()
    for wuxing_dict in [fwd.jin_dict, fwd.mu_dict, fwd.huo_dict, fwd.shui_dict, fwd.tu_dict]:
        for num, word_list in wuxing_dict.items():
            for word in word_list:
                full_word_count_dict[word] = num
    return full_word_count_dict


FULL_WORD_COUNT_DICT = getFullWordcountDict()


def getWordWriteCountWugeCombination():
    """
    根据笔画数量，预先算出还可以的看看，一般般，还过得去
    :return: [(mid_num, last_num)]
    """
    # last_name_write_num = FULL_WORD_COUNT_DICT[config.LAST_NAME]
    last_name_write_num = config.LAST_NAME_WRITE_NUM

    name_num_backup_list = []  # 根据天地人算的还可以的笔画数
    for best_ge in constants.best_num_set:
        mid_num = best_ge - last_name_write_num  # 姓名中间的字
        if mid_num < MIN_SINGLE_NUM or mid_num > MAX_SINGLE_NUM:
            continue
        for best_last_ge in constants.best_num_set:
            last_num = best_last_ge - mid_num  # 姓名最后的字
            if last_num < MIN_SINGLE_NUM or last_num > MAX_SINGLE_NUM:
                continue
            name_num_backup_list.append((mid_num, last_num))
    return name_num_backup_list


def writeDown(result, file_name):
    """
    写入文件
    :param result: 记录
    :param file_name: 文件名
    :return:
    """
    with open(file_name, 'a', encoding='utf8') as f:
        f.write(result)
        f.write('\n')
    return True


def getCookie(url):
    cj = cookiejar.LWPCookieJar()
    handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    r = urllib.request.Request(url)
    result = opener.open(r)
    print(result.read())

    ret = ''
    if cj:
        for ck in cj:
            print(ck.name, ck.value)
            ret = (ck.name + "=" + ck.value) + ";" + ret
        return ret
    else:
        return 'no cookie founded'


def getHtml(url, req_params=None, req_headers=None):
    if req_headers is None:
        req_headers = {}
    if req_params is None:
        req_params = {}

    try:
        common_params = dict(timeout=5, headers=req_headers)
        if req_params and req_headers:
            r = requests.get(url, params=req_params, **common_params)
        else:
            r = requests.get(url, **common_params)

        # print(r.text, )
        # print(r.url, r.encoding, r.status_code, r.headers)
        r.raise_for_status()

        return r.text
        # return response.decode('gb2312', 'ignore')
    except requests.RequestException:
        print('Oops! Timeout Error! Sorry!')


def getScore(name, score=None):
    """
    远程请求计算姓名的得分
    :param name:  姓名
    :return: 得分
    """
    # try:
    #     surname = parse.quote(name[0:1].encode('gb2312'))
    #     lastname = parse.quote(name[1:].encode('gb2312'))
    # except UnicodeEncodeError as e:
    #     print(name, '出错：', str(e))
    #     return
    # s = parse.quote(SEX.encode('gb2312'))
    surname = parse.quote(name[0:1])
    lastname = parse.quote(name[1:])
    s = parse.quote(SEX)
    detail_url = "http://www.qimingzi.net/nameReportpc.aspx?surname=" + surname + "&name=" + lastname + "&sex=" + s + "&year=2024&month=07&day=03&hour=12&minute=48"

    if score is None:
        # detail_url = "http://www.qimingzi.net/simpleReport.aspx?surname=" + surname + "&name=" + lastname + "&sex=" + s
        # print(detail_url)
        # return 0
        html = getHtml(detail_url)
        # 去除html标签之间的的所有空格和空行
        html = re.sub(r'>\s+<', '><', html)
        # 去除html标签之间的的所有空行
        html = re.sub('\n', '', html)
        # html = html.replace(' ', '').replace('\n', '')
        first_tag = '<div class="fenshu">'
        last_tag = '</div><a name="zhuanye">'
        # print(html)
        score = html[html.index(first_tag) + len(first_tag): html.index(last_tag)]
        writeDown("{},{}".format(name, score), TESTED_FILE)
        print('from remote web request:')

    print("名字：{}  分数：{}".format(name, score))
    if score and int(score) >= THRESHOLD_SCORE:
        # 符合阈值要求的结果记录到结果文本
        result = ','.join([name, score, detail_url])
        writeDown(result, RESULT_FILE)
    return score


def getBaijiaxingData():
    """
    百家姓以及第二字和第三字笔画数最佳搭配
    另一个版本可以参考 http://www.360doc.com/content/18/0414/14/4153217_745576219.shtml
    """
    baijiaxing_sancaiwuge_dict = defaultdict(list)
    with open(BAIJIAXING_FILE, 'r', encoding='utf8') as f:
        xing_line = []
        for linecnt, line in enumerate(f):
            line = line.strip()
            if linecnt % 3 == 0:
                xing_line = line
            elif linecnt % 3 == 1:
                combination_list = []
                combinations = line.split(',')
                for c in combinations:
                    tmp = c.split('+')
                    combination_list.append((int(tmp[0]), int(tmp[1])))
                for xing in xing_line:
                    baijiaxing_sancaiwuge_dict[xing] = combination_list
            else:
                continue  # 空行
    return baijiaxing_sancaiwuge_dict


def getSancaiData():
    """
    整理三才数理的数据

    备注：金金木重复了，被我删了
    来源百度百科：https://baike.baidu.com/item/%E4%B8%89%E6%89%8D%E6%95%B0%E7%90%86/2086868
    :return: [key: dict(    # key为天格+人格+地格
                result='',  # 吉凶结果
                evaluate='' # 评价
            ), ...]
    """
    sancai_wuxing_dict = dict()
    with open(SANCAI_FILE, 'r', encoding='utf8') as f:
        line = f.readline()
        wuxing_comb = line[:3]
        if wuxing_comb not in sancai_wuxing_dict:
            sancai_wuxing_dict[wuxing_comb] = dict(
                result='',  # 吉凶结果
                evaluate=''  # 评价
            )

        is_next_new = False
        while True:
            line = f.readline().strip()
            if is_next_new:
                wuxing_comb = line[:3]
                if wuxing_comb not in sancai_wuxing_dict:
                    sancai_wuxing_dict[wuxing_comb] = dict(
                        result='',  # 吉凶结果
                        evaluate=''  # 评价
                    )
                else:
                    print(wuxing_comb, '重复了？？')
                is_next_new = False
            else:
                if line.startswith('【'):
                    result = line[line.index('【') + 1: line.index('】')]
                    sancai_wuxing_dict[wuxing_comb]['result'] = result
                    is_next_new = True
                else:
                    sancai_wuxing_dict[wuxing_comb]['evaluate'] += line.strip()
                    is_next_new = False

            if not line:
                break
    # print('三才吉凶判断结果：', sancai_wuxing_dict)
    return sancai_wuxing_dict


def getNameWuxing(name):
    global word_wuxing_dict
    if len(word_wuxing_dict) == 0:
        word_wuxing_dict = getWordWuxingDict()
    # print(word_wuxing)
    name_wuxing = ''
    for word in name:
        name_wuxing += word_wuxing_dict[word]
    return name_wuxing


def getWordWuxingDict():
    """
    据wuxing_dict_self_lmy2.py中的数据，获取到指定汉字的五行
    """
    full_word_wuxing_dict = dict()
    for index, wuxing_dict in enumerate([fwd.jin_dict, fwd.mu_dict, fwd.huo_dict, fwd.shui_dict, fwd.tu_dict]):
        if index == 0:
            wuxing = '金'
        elif index == 1:
            wuxing = '木'
        elif index == 2:
            wuxing = '火'
        elif index == 3:
            wuxing = '水'
        else:
            wuxing = '土'
        for num, word_list in wuxing_dict.items():
            for word in word_list:
                full_word_wuxing_dict[word] = wuxing
    # print(full_word_wuxing_dict)
    full_word_wuxing_dict['刘'] = '火'
    return full_word_wuxing_dict