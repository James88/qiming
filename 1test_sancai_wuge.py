#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = 'HaoHao de Father'
import traceback
from collections import defaultdict
import config
from data import constants, wuxing_dict_self_lmy2 as w
from config import LAST_NAME, SELECTED_SANCAI, SELECTED_XITONGSHEN
import utils
import time

g_sancai_wuxing_dict = {}
g_baijiaxing_dict = {}  # 百家姓最佳搭配
g_selected_write_dict = {
    '水': w.shui_dict,
    '火': w.huo_dict,
    '木': w.mu_dict,
    '金': w.jin_dict,
    '土': w.tu_dict
}

g_last_name_write_num = config.LAST_NAME_WRITE_NUM
g_last_name_write_num_fanti = config.LAST_NAME_WRITE_NUM_FANTI


def calHaohaoWuge(verbose=True):
    """
    方法二：
    三才五格 最适合的计算
    配置在constants.py中，根据个人情况配置
    只考虑名字三个字的情况

    三才五格计算公式参考： http://www.360doc.com/content/18/0521/14/1654071_755714474.shtml
    根据笔画查字 ref：http://www.zdic.net/z/kxzd/zbh/
    :param verbose 展示参考的笔画数量
    :return:
    """
    write_num_set = set()  # 展示参考的笔画数量
    name_num_backup_list = utils.getWordWriteCountWugeCombination()

    # 结果总格和外格计算
    best_wuge_combination = []
    for (mid_num, last_num) in name_num_backup_list:
        tian_ge = g_last_name_write_num + 1
        zong_ge = g_last_name_write_num + mid_num + last_num
        ren_ge = g_last_name_write_num + mid_num
        di_ge = mid_num + last_num
        wai_ge = zong_ge - ren_ge + 1
        # FIXME 这里真的有必要把总格和外格过滤？？
        if zong_ge not in constants.best_num_set or wai_ge not in constants.best_num_set:
            continue
        # 计算三才
        sancai, sancai_result, sancai_evaluate = calHoahaoSancai(tian_ge, ren_ge, di_ge)
        if '凶' in sancai_result or sancai_result == constants.RESULT_UNKNOWN:
            # print('过滤判断为凶或未知的三才：', sancai, sancai_result)
            continue
        if SELECTED_SANCAI and sancai_result not in SELECTED_SANCAI:  # 必须要非常旺的才要
            continue
        # 计入结果
        best_wuge_combination.append((mid_num, last_num, sancai, sancai_result))
        write_num_set.add(mid_num)
        write_num_set.add(last_num)

    if verbose:
        output_num_list = list(write_num_set)
        output_num_list.sort()
        print('**好好五格名字笔画数量：', len(best_wuge_combination), '\n笔画组合如下所示：')
        for o in best_wuge_combination:
            print('\t', o)
        print('\t名字中乾隆字典笔画包括：', output_num_list)

    return best_wuge_combination


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


def calHoahaoSancai(tian_ge, ren_ge, di_ge):
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


def getWriteNumDict():
    """
    根据五行找字典中的字。如果配置为None则全部都选。
    :return:
    """
    if SELECTED_XITONGSHEN:
        return g_selected_write_dict[SELECTED_XITONGSHEN]
    else:
        write_num_dict = defaultdict(list)
        for _, wdict in g_selected_write_dict.items():
            for num, word_list in wdict.items():
                write_num_dict[num] += word_list
        return write_num_dict


def getSancaiWugeSelection(best_combination):
    """
    通过三才五格算出的笔画数，找出匹配的名字清单
    :param best_combination:
    :return:
    """
    write_num_dict = getWriteNumDict()
    name_set = set()
    for best in best_combination:
        mid_write_num = best[0]
        last_write_num = best[1]
        if mid_write_num not in write_num_dict or last_write_num not in write_num_dict:
            # 假如找不到这个笔画，跳过处理
            continue
        mid_selection_list = write_num_dict[mid_write_num]
        last_selection_list = write_num_dict[last_write_num]

        if config.debug:
            # 仅仅测试下笔画配比
            name_set.add(LAST_NAME + mid_selection_list[0] + last_selection_list[0])
        else:
            # 所有名字都测试下
            for m in mid_selection_list:
                for l in last_selection_list:
                    name_set.add(LAST_NAME + m + l)  # 反过来的话人格和地格就不对了
    print('三才五格待测试名字列表：', len(name_set), name_set)
    return name_set


def getLastNameWuge(lastname):
    return g_baijiaxing_dict[lastname] if lastname in g_baijiaxing_dict else []
    # return [(3, 14), (4, 14), (4, 7), (11, 20), (11, 4), (3, 17), (3, 7), (11, 14), (19, 12), (11, 10), (4, 17),
    #         (9, 12), (7, 10), (11, 3), (11, 12)]


def mainBestSancaiwuge():
    """
    综合计算
    三才五格 自己算的和网站算的求交集
    :return:
    """
    # 三才五格计算
    best_wuge_combination = calHaohaoWuge()  # 通过三才五格公式自己算的理论值
    # 根据姓氏优秀三才五格配比
    best_dict_combination = getLastNameWuge(config.LAST_NAME)

    # 结合上面的结果晒出列表
    best_list = []
    for best in best_wuge_combination:
        compare_item = (best[0], best[1])
        if compare_item not in best_dict_combination:
            continue
        best_list.append(best)
    if best_list:
        print('综合计算的结果，数量{}, 组合{}'.format(len(best_list), best_list))
    else:
        # 如果实在匹配不到，用理论值替代
        best_list = best_wuge_combination
        print('没有得到最好的三才五格配置，建议适当放宽constants中good_num_list和bad_num_list的要求。')

    sancaiwuge_sel = getSancaiWugeSelection(best_list)
    # 过滤 包含 config.DONT_NEED_WORD list 的名字
    if config.DONT_NEED_WORD:
        sancaiwuge_sel = [x for x in sancaiwuge_sel if not any(word in x for word in config.DONT_NEED_WORD)]

    print('过滤后的名字列表：', len(sancaiwuge_sel), sancaiwuge_sel)


# 根据输入的汉字，通过五行字典找到对应的笔画数

FULL_WORD_COUNT_DICT = utils.getFullWordcountDict()


def getHanziWuxing(name):
    """
    根据输入的汉字，通过五行字典找到对应的五行属性
    :param name: 名字
    :return: 五行
    """
    wuxing = utils.getNameWuxing(name)
    return wuxing
    if wuxing == '火木水':
        return True
    return False


def cal_sancaiwuge(name_set):
    """
    根据名字计算对应的三才五格，并判断数字是否归属best_ge
    :return:
    """
    JIANTI_FANTI_ALL_TEST = False
    # 过滤重复
    name_set = list(set(name_set))
    unknown_word = False
    for name in name_set:
        for word in name:
            if word not in FULL_WORD_COUNT_DICT:
                # print('名字中包含不认识的字：', name)
                unknown_word = True
                break
        if unknown_word:
            unknown_word = False
            continue

        # print(name)
        # 计算名字的笔画数
        name_write_num = sum([FULL_WORD_COUNT_DICT[word] for word in name])
        # 计算名字的三才五格
        tian_ge = g_last_name_write_num + 1
        ren_ge = g_last_name_write_num + FULL_WORD_COUNT_DICT[name[1]]
        di_ge = FULL_WORD_COUNT_DICT[name[1]] + FULL_WORD_COUNT_DICT[name[2]]
        zong_ge = g_last_name_write_num + FULL_WORD_COUNT_DICT[name[1]] + FULL_WORD_COUNT_DICT[name[2]]
        wai_ge = zong_ge - ren_ge + 1
        # 判断 tian_ge ren_ge di_ge zong_ge wai_ge 是否在 best_ge 中
        if ren_ge not in constants.best_num_set or di_ge not in constants.best_num_set or zong_ge not in constants.best_num_set or wai_ge not in constants.best_num_set:
            continue
        # 计算三才
        sancai, sancai_result, sancai_evaluate = calHoahaoSancai(tian_ge, ren_ge, di_ge)
        if '凶' in sancai_result or sancai_result == constants.RESULT_UNKNOWN:
            # print('过滤判断为凶或未知的三才：', sancai, sancai_result)
            continue
        if SELECTED_SANCAI and sancai_result not in SELECTED_SANCAI:  # 必须要非常旺的才要
            continue

        if JIANTI_FANTI_ALL_TEST:
            tian_ge = g_last_name_write_num_fanti + 1
            ren_ge = g_last_name_write_num_fanti + FULL_WORD_COUNT_DICT[name[1]]
            di_ge = FULL_WORD_COUNT_DICT[name[1]] + FULL_WORD_COUNT_DICT[name[2]]
            zong_ge = g_last_name_write_num_fanti + FULL_WORD_COUNT_DICT[name[1]] + FULL_WORD_COUNT_DICT[name[2]]
            wai_ge = zong_ge - ren_ge + 1
            # 判断 tian_ge ren_ge di_ge zong_ge wai_ge 是否在 best_ge 中
            # if tian_ge not in constants.best_num_set or ren_ge not in constants.best_num_set or di_ge not in constants.best_num_set or zong_ge not in constants.best_num_set or wai_ge not in constants.best_num_set:
            if ren_ge not in constants.best_num_set:
                continue
            # 计算三才
            sancai, sancai_result, sancai_evaluate = calHoahaoSancai(tian_ge, ren_ge, di_ge)
            if '凶' in sancai_result or sancai_result == constants.RESULT_UNKNOWN:
                # print('过滤判断为凶或未知的三才：', sancai, sancai_result)
                continue
            if SELECTED_SANCAI and sancai_result not in SELECTED_SANCAI:  # 必须要非常旺的才要
                continue

        wuxing = getHanziWuxing(name)
        if wuxing == '火木水':
            print(name)
            # print('名字：', name, '笔画数：', name_write_num, '三才五格：', sancai, sancai_result, sancai_evaluate)
        else:
            continue
            print(name + "---[" + wuxing + "]")
        # print('名字：', name, '笔画数：', name_write_num, '三才五格：', sancai, sancai_result, sancai_evaluate, '结果：', result)
        # utils.writeDown(name + ',' + result, config.TESTED_NAME_FILE)


def start():
    # 开始执行
    global g_sancai_wuxing_dict
    global g_baijiaxing_dict
    g_sancai_wuxing_dict = utils.getSancaiData()
    g_baijiaxing_dict = utils.getBaijiaxingData()
    # print(g_baijiaxing_dict)
    full_word_wuxing = utils.getWordWuxingDict()
    try:
        # 适用于普遍的情况下
        # mainBestSancaiwuge()
        # 读取tested/7.txt中的名字，并返回列表
        name_set = []
        which = 3
        if 1 == which:
            mid = []
            last = []
            with open('tested/1.txt', 'r', encoding='utf8') as f:
                while True:
                    line = f.readline()
                    mid.append(line[:1])
                    last.append(line[1:2])
                    if not line:
                        break
            # mid last 过滤重复
            mid = list(set(mid))
            last = list(set(last))
            # 判断l和m是否在wuxing_dict中，不在则显示出来
            for m in mid:
                if m not in full_word_wuxing:
                    del mid[mid.index(m)]
            for l in last:
                if l not in full_word_wuxing:
                    del last[last.index(l)]
            # 根据mid 和 last 生成名字
            for m in mid:
                for l in last:
                    if m != '' and l != '':
                        name_set.append('刘' + m + l)
        if 2 == which:
            with open('tested/1.txt', 'r', encoding='utf8') as f:
                while True:
                    line = f.readline()
                    if line and line != '\t':
                        if line[:1] in full_word_wuxing and line[1:2] in full_word_wuxing:
                            name_set.append('刘' + line[:2])
                    if not line:
                        break
        if 3 == which:
            # 读取csv新华字典找到三点水的字
            import csv
            shui = []
            mu = []
            with open('data/xinhua.csv', 'r', encoding='utf8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] not in FULL_WORD_COUNT_DICT:
                        continue
                    if row[1] == '氵':
                        # print(row[0])
                        shui.append(row[0])
                        name_set.append('刘柚' + row[0])
                    if row[1] == '木':
                        # print(row[0])
                        renge = config.LAST_NAME_WRITE_NUM + FULL_WORD_COUNT_DICT[row[0]]
                        renge2 = config.LAST_NAME_WRITE_NUM_FANTI + FULL_WORD_COUNT_DICT[row[0]]

                        if renge in constants.best_num_set and renge2 in constants.best_num_set:
                            mu.append(row[0])
            print(mu)
            # return 0
            # for m in mu:
                # for s in shui:
                    # name_set.append('刘' + m + s)
        print(len(name_set))
        print(name_set)
        # 过滤
        name_set = [x for x in name_set if not any(word in x for word in config.DONT_NEED_WORD)]
        name_set = list(set(name_set))
        print(len(name_set))
        # with open('tested/9.txt', 'r', encoding='utf8') as f:
        #     # 获取每行的前三个汉字
        #     while True:
        #         line = f.readline()
        #         # print(line)
        #         if line and line != '\t':
        #             name_set.append(line[:3])
        #         if not line:
        #             break
        cal_sancaiwuge(name_set)
        # 适用于姓名第二个字根据族谱的情况，或者孩子父母有个字特别喜欢的情况
        # calFixWord(again=True)
    except Exception as e:
        traceback.print_exc()
        print('Have a rest, then continue...')
        print('Error:', str(e))
        time.sleep(5)


if __name__ == '__main__':
    start()
