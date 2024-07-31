import json
import csv
from data import constants
import config
import utils

g_sancai_wuxing_dict = {}
g_words_jianti_dict = {}
g_words_fanti_dict = {}


def get_best_ge_bihua(fan_ti= False, specfic_best = False):
    """
    根据姓氏笔画获取姓名中间和最后一个字的笔画数
    :param strict: 是否严格匹配 严格的话 计算刘字的简体和繁体笔画都计算
    """
    mid_list = []
    mid_last_list = []
    xingshi_bihua = config.LAST_NAME_WRITE_NUM
    if fan_ti:
        xingshi_bihua = config.LAST_NAME_WRITE_NUM_FANTI
    liu_best = [
        {"mid": 9, "last": 23},
        {"mid": 10, "last": 7},
        {"mid": 9, "last": 7},
        {"mid": 22, "last": 15},
        {"mid": 2, "last": 14},
        {"mid": 20, "last": 4},
        {"mid": 8, "last": 24},
        {"mid": 3, "last": 14},
    ]
    if specfic_best == True:
        return liu_best
    # 人格
    for i in range(config.MIN_SINGLE_NUM, config.MAX_SINGLE_NUM):
        if xingshi_bihua + i in constants.best_num_set:
            mid_list.append(i)
    # print(mid_list)
    # 地格
    for i in range(config.MIN_SINGLE_NUM, config.MAX_SINGLE_NUM):
        # print(i)
        for mid in mid_list:
            last = mid + i
            if last in constants.best_num_set:
                mid_last_list.append({'mid': mid, 'last': i})
    # print(mid_list)
    print('只计算名字第一个第二个字，人格 地格后 匹配数量：{}'.format(len(mid_last_list)))
    # print(mid_last_list)
    mid_last_list_all_ok = []
    # 总格 外格
    for name in mid_last_list:
        mid = name['mid']
        last = name['last']

        tian_ge = xingshi_bihua + 1
        ren_ge = xingshi_bihua + mid
        di_ge = mid + last

        zong_ge = xingshi_bihua + mid + last
        wai_ge = zong_ge - ren_ge + 1

        if zong_ge not in constants.best_num_set:
            continue
        if wai_ge not in constants.best_num_set:
            continue

        # 判断三才
        sancai, sancai_result, sancai_evaluate = calSancai(tian_ge, ren_ge, di_ge)
        # print(sancai, sancai_result, sancai_evaluate)
        if '凶' in sancai_result or sancai_result == constants.RESULT_UNKNOWN:
            # print('过滤判断为凶或未知的三才：', sancai, sancai_result)
            continue
        if config.SELECTED_SANCAI and sancai_result not in config.SELECTED_SANCAI:  # 必须要非常旺的才要
            continue

        # mid_last_list_all_ok.append({'mid': mid, 'last': last, 'zong_ge': zong_ge, 'wai_ge': wai_ge})
        mid_last_list_all_ok.append({'mid': mid, 'last': last, 'sancai': sancai})
    print('计算总格 外格 三才后 匹配数量：{}'.format(len(mid_last_list_all_ok)))

    # 刘姓适合的笔画
    # for mid_last_ok in mid_last_list_all_ok:
    #     mid = mid_last_ok['mid']
    #     last = mid_last_ok['last']
    #     for liu in liu_best:
    #         if liu['mid'] == mid and liu['last'] == last:
    #             print('找到最佳匹配:', mid, last)
    #             return mid, last
    print(mid_last_list_all_ok)
    return mid_last_list_all_ok


def get_word_by_bihua(bihua_spec, wuxing_spec=None, fan_ti=False):
    """
    读取wendang/wuxing_dict.json根据笔画数获取字
    """
    if fan_ti:
        with open('data/wuxing_dict_fanti.json', 'r', encoding='utf-8') as f:
            wuxing_dict = json.load(f)
    else:
        with open('data/wuxing_dict_jianti.json', 'r', encoding='utf-8') as f:
            wuxing_dict = json.load(f)

    word_list = []
    for wuxing in wuxing_dict:
        if wuxing == wuxing_spec:
            for bihua in wuxing_dict[wuxing]:
                if bihua == bihua_spec:
                    word_list = wuxing_dict[wuxing][bihua]
            break
        else:
            for bihua in wuxing_dict[wuxing]:
                if bihua == bihua_spec:
                    word_list += wuxing_dict[wuxing][bihua]
    return word_list


def get_word_by_wuxing(wuxing_spec):
    """
    读取wendang/wuxing_dict_jianti.json根据五行获取字
    不再根据笔画，直接列出所有字
    """
    with open('data/wuxing_dict_jianti.json', 'r', encoding='utf-8') as f:
        wuxing_dict = json.load(f)

    word_list = []
    for wuxing in wuxing_dict:
        if wuxing_spec == wuxing:
            for bihua in wuxing_dict[wuxing]:
                word_list += wuxing_dict[wuxing][bihua]
            break
    return word_list

def getSancaiWuxing(x_ge):
    """
    根据天格、人格、地格计算得出五行属性
    尾数为1，2五行为木；尾数为3，4五行为火；尾数为5，6五行为土；尾数为7，8五行为金；尾数为9，0五行为水
    :param x_ge: x格
    :return: 五行
    """
    wuxing = ''
    if (x_ge % 10) in [1, 2]:
        wuxing = '木'
    elif (x_ge % 10) in [3, 4]:
        wuxing = '火'
    elif (x_ge % 10) in [5, 6]:
        wuxing = '土'
    elif (x_ge % 10) in [7, 8]:
        wuxing = '金'
    elif (x_ge % 10) in [9, 0]:
        wuxing = '水'
    return wuxing


def calSancai(tian_ge, ren_ge, di_ge):
    """
    三才五行吉凶计算
    :return:
    :param tian_ge:  天格
    :param ren_ge:  人格
    :param di_ge:  地格
    :return:
    """
    sancai = getSancaiWuxing(tian_ge) + getSancaiWuxing(ren_ge) + getSancaiWuxing(di_ge)
    if sancai in g_sancai_wuxing_dict:
        data = g_sancai_wuxing_dict[sancai]
        return sancai, data['result'], data['evaluate']
    else:
        return sancai, constants.RESULT_UNKNOWN, None


def get_common_name_words():
    """
    获取女孩名字常用字
    @visit https://github.com/wainshine/Chinese-Names-Corpus
    """
    common_name_words = set()
    with open('data/Chinese_Names_Corpus_Gender（120W）.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # 跳过前4行
            line_list = line.strip().split(',')
            # print(line_list)
            # return 0
            if line_list[1] == '女':
                for index, word in enumerate(line_list[0]):
                    # 跳过第一个
                    if index == 0:
                        continue
                    common_name_words.add(word)
                # common_name_words.update(line_list[0][0], line_list[0][1])
    return common_name_words


def filter_by_shengdiao(name_list, shengdiao_mid, shengdiao_last):
    """
    根据声调过滤名字
    """
    # 导入 xinhua.csv 汉字作为key 声调作为value
    words_dict = {}
    with open('data/xinhua.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows:
        if len(row) == 4:
            words_dict[row[0]] = row[3]

    new_name_list = []
    for name in name_list:
        if len(name) != 3 or name[1] not in words_dict or name[2] not in words_dict:
            continue

        # print(name)
        mid_tone = get_tone(words_dict[name[1]])
        last_tone = get_tone(words_dict[name[2]])

        if mid_tone == shengdiao_mid and last_tone == shengdiao_last:
            new_name_list.append(name)

    return new_name_list

def get_tone(pinyin):
    tones = {
        'ā': 1, 'á': 2, 'ǎ': 3, 'à': 4,
        'ē': 1, 'é': 2, 'ě': 3, 'è': 4,
        'ī': 1, 'í': 2, 'ǐ': 3, 'ì': 4,
        'ō': 1, 'ó': 2, 'ǒ': 3, 'ò': 4,
        'ū': 1, 'ú': 2, 'ǔ': 3, 'ù': 4,
        'ǖ': 1, 'ǘ': 2, 'ǚ': 3, 'ǜ': 4
    }
    for char in pinyin:
        if char in tones:
            return tones[char]
    return 1  # 默认返回一声


def check_sancai_wuge(name):
    """
    检测给定的名字的三才五格的吉凶
    """
    # 简体
    tian_ge = int(g_words_jianti_dict[name[0]]) + 1
    ren_ge = int(g_words_jianti_dict[name[0]]) + int(g_words_jianti_dict[name[1]])
    di_ge = int(g_words_jianti_dict[name[1]]) + int(g_words_jianti_dict[name[2]])
    zong_ge = int(g_words_jianti_dict[name[0]]) + di_ge
    wai_ge = zong_ge - ren_ge + 1

    # print(tian_ge, ren_ge, di_ge, zong_ge, wai_ge)
    print(name + '-简体笔画计算：')
    chek_sancai_wuge_real(tian_ge, ren_ge, di_ge, zong_ge, wai_ge)
    print("\n")
    # 繁体
    tian_ge = int(g_words_fanti_dict[name[0]]) + 1
    ren_ge = int(g_words_fanti_dict[name[0]]) + int(g_words_fanti_dict[name[1]])
    di_ge = int(g_words_fanti_dict[name[1]]) + int(g_words_fanti_dict[name[2]])
    zong_ge = int(g_words_fanti_dict[name[0]]) + di_ge
    wai_ge = zong_ge - ren_ge + 1
    print(name + '-' + '繁体笔画计算：')
    chek_sancai_wuge_real(tian_ge, ren_ge, di_ge, zong_ge, wai_ge)
    print("\n\n")


def chek_sancai_wuge_real(tian_ge, ren_ge, di_ge, zong_ge, wai_ge):
    if tian_ge in constants.best_num_set:
        print(f"天格：{tian_ge} 【吉】")
    else:
        print(f"天格：{tian_ge} 【不在好数字里】")

    if ren_ge in constants.best_num_set:
        print(f"人格：{ren_ge} 【吉】")
    else:
        print(f"人格：{ren_ge} 【不在好数字里】")

    if di_ge in constants.best_num_set:
        print(f"地格：{di_ge} 【吉】")
    else:
        print(f"地格：{di_ge} 【不在好数字里】")

    if zong_ge in constants.best_num_set:
        print(f"总格：{zong_ge} 【吉】")
    else:
        print(f"总格：{zong_ge} 【不在好数字里】")

    if wai_ge in constants.best_num_set:
        print(f"外格：{wai_ge} 【吉】")
    else:
        print(f"外格：{wai_ge} 【不在好数字里】")

    sancai, sancai_result, sancai_evaluate = calSancai(tian_ge, ren_ge, di_ge)
    print(sancai, sancai_result, sancai_evaluate)

def start():
    """
    开始
    """
    global g_sancai_wuxing_dict
    global g_words_jianti_dict
    global g_words_fanti_dict

    g_sancai_wuxing_dict = utils.getSancaiData()

    # 简体字典
    with open('data/xinhua.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows:
        if len(row) == 4:
            g_words_jianti_dict[row[0]] = row[2]

    # 繁体字典
    g_words_fanti_dict = utils.getFullWordcountDict()


start()
