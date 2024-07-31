import helper


def check(name):
    helper.check_sancai_wuge(name)


if __name__ == '__main__':
    name_list = [
        # 水 木
        '刘泽娇',
        '刘子菡',
        '刘子玉',
        '刘润佳',
        '刘润欣',
        '刘惠颜',
    ]
    for name in name_list:
        check(name)
