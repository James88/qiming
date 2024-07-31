import os
import helper


def get_name_by_spec_tone(filename, shengdiao_mid, shengdiao_last):
    """
    根据声调获取名字
    """
    name_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        # 读取txt
        for line in f:
            # 读取每行的前三个汉字
            name_list.append(line.strip())
    print(f"过滤前名字数量：{len(name_list)}")
    name_filtered = helper.filter_by_shengdiao(name_list, shengdiao_mid, shengdiao_last)

    return name_filtered


if __name__ == '__main__':
    good_tone_list = [
        (4, 2),  # 百度
        (4, 1),
        (4, 3),

        (3, 2),  # 百度
        (3, 4),
        (1, 4),
        (1, 3),
    ]
    # file = 'generated_names/5generated_names.csv'
    file = 'analysis_result/temp.csv'

    file_name_result = 'analysis_result/result.txt'
    # for x in range(100):
    #     if not os.path.exists(f"analysis_result/{x}result.txt"):
    #         file_name_result = 'analysis_result/' + str(x) + 'result.txt'
    #         break

    with open(file_name_result, 'w', encoding='utf-8') as f1:
        f1.write("分析结果：\r\n")
        for good_tone in good_tone_list:
            shengdiao_mid = good_tone[0]
            shengdiao_last = good_tone[1]
            strtext = f"中间声调：{shengdiao_mid}，后面声调：{shengdiao_last}"
            print(strtext)
            f1.write(strtext + "\n")
            name_list = get_name_by_spec_tone(file, shengdiao_mid, shengdiao_last)
            # print list 一行一个
            print(name_list)

            mid = set()
            last = set()
            for name in name_list:
                mid.add(name[1])
                last.add(name[2])

            print(f"中间汉字：{mid}")
            print(f"后面汉字：{last}")
            print(f"中间汉字：{mid}", file=f1)
            print(f"后面汉字：{last}", file=f1)
            # for item in mid:
            #     f1.write(str(item) + "\n")
            # for item in last:
            #     f1.write(str(item) + "\n")
            f1.write(f"过滤后名字数量：{len(name_list)}" + "\n")

            for name in name_list:
                f1.write(name + "\n")

            print(f"过滤后名字数量：{len(name_list)}")
            print("\r\n")
            print("\r\n")
            f1.write("\n\n")
