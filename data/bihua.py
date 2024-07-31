import csv
import json


def fix_xinhua_csv():
    """
    补全新华字典的csv文件中的笔画数
    """
    # 读取 word.json 写入到 汉字和笔画字典
    words_dict = dict()
    with open('docs/word.json', 'r', encoding='utf-8') as f:
        words = json.load(f)
    for word in words:
        words_dict[word['word']] = word['pinyin']
        words_dict[word['oldword']] = word['pinyin']
    # print(words_dict)
    print(len(words_dict))

    # 补全csv中汉字的笔画
    with open('docs/xinhua.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows:
        if len(row) == 3:
            print(row[0])
            if row[0] in words_dict:
                # row[2] = words_dict[row[0]]
                row.append(words_dict[row[0]])
        if len(row) == 3:
            row.append('error')

        #     # 删除当前行
        #     print(row)
        #     rows.remove(row)

    # return 0
    with open('docs/xinhua.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(len(rows))


def generate_wuxing_bihua_words():
    """
    根据wendant/gsc_pinyin.csv生成五行笔画字典
    """
    with open('docs/gsc_pinyin.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    wuxing_dict = dict()
    for row in rows:
        # 跳过第一行
        if row[0] == 'num':
            continue
        if row[5] == '金':
            if 'jin' not in wuxing_dict:
                print('not in ')
                wuxing_dict['jin'] = {}
            if int(row[4]) in wuxing_dict['jin']:
                wuxing_dict['jin'][int(row[4])].append(row[1])
            else:
                wuxing_dict['jin'][int(row[4])] = []
                wuxing_dict['jin'][int(row[4])].append(row[1])
        elif row[5] == '水':
            if 'shui' not in wuxing_dict:
                wuxing_dict['shui'] = {}
            if int(row[4]) in wuxing_dict['shui']:
                wuxing_dict['shui'][int(row[4])].append(row[1])
            else:
                wuxing_dict['shui'][int(row[4])] = []
                wuxing_dict['shui'][int(row[4])].append(row[1])
        elif row[5] == '木':
            if 'mu' not in wuxing_dict:
                wuxing_dict['mu'] = {}
            if int(row[4]) in wuxing_dict['mu']:
                wuxing_dict['mu'][int(row[4])].append(row[1])
            else:
                wuxing_dict['mu'][int(row[4])] = []
                wuxing_dict['mu'][int(row[4])].append(row[1])
        elif row[5] == '火':
            if 'huo' not in wuxing_dict:
                wuxing_dict['huo'] = {}
            if int(row[4]) in wuxing_dict['huo']:
                wuxing_dict['huo'][int(row[4])].append(row[1])
            else:
                wuxing_dict['huo'][int(row[4])] = []
                wuxing_dict['huo'][int(row[4])].append(row[1])
        elif row[5] == '土':
            if 'tu' not in wuxing_dict:
                wuxing_dict['tu'] = {}
            if int(row[4]) in wuxing_dict['tu']:
                wuxing_dict['tu'][int(row[4])].append(row[1])
            else:
                wuxing_dict['tu'][int(row[4])] = []
                wuxing_dict['tu'][int(row[4])].append(row[1])
        else:
            print('error:'+row[1])
            continue

    print(wuxing_dict)
    print(len(wuxing_dict))
    # wuxing_dict 写入到文件
    with open('docs/wuxing_dict_jianti.json', 'w', encoding='utf-8') as f:
        json.dump(wuxing_dict, f, ensure_ascii=False)
    print('success')


if __name__ == '__main__':
    fix_xinhua_csv()
    # generate_wuxing_bihua_words()
