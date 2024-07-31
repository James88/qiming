"""
生成名字
"""
import os
import csv
import helper
import collections


def generate_name(fan_ti=False, specific_best=False):
    """
    生成名字
    :param fan_ti: 繁体
    :specific_best: True 返回指定给出的 刘性默认适合的笔画
    """
    # 获取五格比较好的名字笔画
    global file_name
    liu_best = helper.get_best_ge_bihua(fan_ti, specific_best)

    # # 2格list取交集
    # liu_best = [x for x in liu_best if x in liu_best2]
    # print(liu_best)
    # return 0
    # 常用字
    name_common_words = helper.get_common_name_words()
    print('女名常用字数量：{}'.format(len(name_common_words)))

    mid_wuxing = 'shui'
    last_wuxing = 'jin'
    # 判断文件是否存在，不存在则创建
    fanti_text = '简体'
    if fan_ti:
        fanti_text = '繁体'
    specific_best_text = '计算'
    if specific_best:
        specific_best_text = '默认'
    for x in range(100):
        file_name = f"generated_names/{mid_wuxing}-{last_wuxing}-{fanti_text}-{specific_best_text}-{x}.csv"
        if not os.path.exists(file_name):
            # file_name = 'generated_names/' + str(x) + 'generated_names.csv'
            break

    count_all = 0
    name_list = []
    for mid_last_ok in liu_best:
        # 读取五行笔画字典
        # bihua6 = helper.get_word_by_bihua('6', 'huo')

        word_mid = helper.get_word_by_bihua(f"{mid_last_ok['mid']}", mid_wuxing, fan_ti)
        word_last = helper.get_word_by_bihua(f"{mid_last_ok['last']}", last_wuxing, fan_ti)
        # print(word_mid)
        # print(bihua6)
        # 根据笔画生成名字
        with (open(file_name, 'a', newline='', encoding='utf-8') as f):
            count = 0
            writer = csv.writer(f)
            writer.writerow(['name'])
            for word1 in word_mid:
                # if word1 in config.DONT_NEED_WORD:
                #     continue
                if word1 not in name_common_words:
                    continue
                for word2 in word_last:
                    # if word2 in config.DONT_NEED_WORD:
                    #     continue
                    if word2 not in name_common_words:
                        continue
                    name = '刘' + word1 + word2
                    writer.writerow([name])
                    name_list.append(name)
                    count += 1
                    count_all += 1
                    # print(name)
            writer.writerow([f"{mid_last_ok['mid']} - {mid_last_ok['last']} 生成名字数量：{count}"])
            print(f"{mid_last_ok['mid']} - {mid_last_ok['last']} 生成名字数量：{count}")
    print(f"生成名字总数量：{count_all}")
    generate_html(name_list, file_name)
    generate_html_mobile(name_list, file_name)


def generate_name_by_jianti_wuxing():
    """
    生成名字
    """
    global file_name
    # 常用字
    name_common_words = helper.get_common_name_words()
    print('女名常用字数量：{}'.format(len(name_common_words)))

    mid_wuxing = 'shui'
    last_wuxing = 'jin'
    # 判断文件是否存在，不存在则创建
    for x in range(100):
        file_name = f"generated_names/all-{x}-{mid_wuxing}-{last_wuxing}-generated_names.csv"
        if not os.path.exists(file_name):
            # file_name = 'generated_names/' + str(x) + 'generated_names.csv'
            break

    count_all = 0
    name_list = []

    word_mid = helper.get_word_by_wuxing(mid_wuxing)
    word_last = helper.get_word_by_wuxing(last_wuxing)
    # 根据字生成名字
    with (open(file_name, 'a', newline='', encoding='utf-8') as f):
        count = 0
        writer = csv.writer(f)
        writer.writerow(['name'])
        for word1 in word_mid:
            # if word1 in config.DONT_NEED_WORD:
            #     continue
            if word1 not in name_common_words:
                continue
            for word2 in word_last:
                # if word2 in config.DONT_NEED_WORD:
                #     continue
                if word2 not in name_common_words:
                    continue
                name = '刘' + word1 + word2
                writer.writerow([name])
                name_list.append(name)
                count += 1
                count_all += 1
                # print(name)
        print(f"生成名字总数量：{count_all}")
    generate_html(name_list, file_name)
    generate_html_mobile(name_list, file_name)


def generate_html(name_list, file_name):
    # 分析姓名列表，找出中间字
    middle_chars = collections.defaultdict(list)
    for name in name_list:
        if len(name) == 3:
            middle_char = name[1]
            middle_chars[middle_char].append(name)

    # 生成HTML内容
    html_content = """
    <html>
    <head>
        <title>名字筛选</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .char-list {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                padding: 0;
                list-style: none;
            }
            .char-list li {
                margin: 15px;
            }
            .char-list a {
                text-decoration: none;
                color: white;
                background-color: #007BFF;
                padding: 10px 15px;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .char-list a:hover {
                background-color: #0056b3;
            }
            .name-list {
                display: none;
                list-style: none;
                padding: 0;
                margin-top: 10px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }
            .name-list li {
                margin: 5px;
                color: #333;
            }
        </style>
        <script>
            function toggleNameList(char, that) {
                console.log(that);
                if (that.style.backgroundColor === 'red') {
                    that.style.backgroundColor = '#007BFF';
                } else {
                    that.style.backgroundColor = 'red';
                }
                var lists = document.getElementsByClassName('name-list');
                for (var i = 0; i < lists.length; i++) {
                    lists[i].style.display = 'none';
                }
                var list = document.getElementById(char);
                list.style.display = 'flex';
            }
        </script>
    </head>
    <body>
        <h1>姓名筛选结果</h1>
        <ul class="char-list">
    """

    # 生成中间字和对应名字列表的HTML
    for char, names in middle_chars.items():
        html_content += f'<li><a href="javascript:void(0);" onclick="toggleNameList(\'{char}\', this)">{char}</a></li>'

    html_content += "</ul>"

    for char, names in middle_chars.items():
        html_content += f'<ul id="{char}" class="name-list">'
        for name in names:

            html_content += f'<li>{name[0]}'
            html_content += f'<a href="https://hanyu.baidu.com/zici/s?wd={name[1]}" target="_blank">{name[1]}</a>'
            html_content += f'<a href="https://hanyu.baidu.com/zici/s?wd={name[2]}" target="_blank">{name[2]}</a>'
            html_content += f'</li>'
        html_content += '</ul>'

    html_content += """
    </body>
    </html>
    """

    # .csv更换为.html
    file_name = file_name.replace('.csv', '.html')
    # 保存为HTML文件
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)


def generate_html_mobile(name_list, file_name):
    # 分析姓名列表，找出中间字
    middle_chars = collections.defaultdict(list)
    for name in name_list:
        if len(name) == 3:
            middle_char = name[1]
            middle_chars[middle_char].append(name)

    # 生成HTML内容
    html_content = """
    <html>
    <head>
        <title>名字筛选</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .char-list {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                padding: 0;
                list-style: none;
                margin: 0;
            }
            .char-list li {
                margin: 15px;
            }
            .char-list a {
                text-decoration: none;
                color: white;
                background-color: #007BFF;
                padding: 10px 15px;
                border-radius: 5px;
                transition: background-color 0.3s;
                font-size: 1.2em;
            }
            .char-list a:hover {
                background-color: #0056b3;
            }
            .name-list {
                display: none;
                list-style: none;
                padding: 0;
                margin-top: 10px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }
            .name-list li {
                margin: 5px;
                color: #333;
                background-color: #fff;
                padding: 5px 10px;
                border-radius: 5px;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            }
            @media (max-width: 600px) {
                .char-list a {
                    padding: 8px 12px;
                    font-size: 1em;
                }
                .name-list li {
                    padding: 5px;
                }
            }
        </style>
        <script>
            function toggleNameList(char) {
                var lists = document.getElementsByClassName('name-list');
                for (var i = 0; i < lists.length; i++) {
                    lists[i].style.display = 'none';
                }
                var list = document.getElementById(char);
                list.style.display = 'flex';
            }
        </script>
    </head>
    <body>
        <h1>姓名筛选结果</h1>
        <ul class="char-list">
    """

    # 生成中间字和对应名字列表的HTML
    for char, names in middle_chars.items():
        html_content += f'<li><a href="javascript:void(0);" onclick="toggleNameList(\'{char}\')">{char}</a></li>'

    html_content += "</ul>"

    for char, names in middle_chars.items():
        html_content += f'<ul id="{char}" class="name-list">'
        for name in names:
            html_content += f'<li>{name}</li>'
        html_content += '</ul>'

    html_content += """
    </body>
    </html>
    """
    file_name = file_name.replace('.csv', '_mobile.html')
    # 保存为HTML文件
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)


# fanti = False
# specific_best = False
# generate_name(fanti, specific_best)
#
# fanti = False
# specific_best = True
# generate_name(fanti, specific_best)
#
# fanti = True
# specific_best = False
# generate_name(fanti, specific_best)
#
# fanti = True
# specific_best = True
# generate_name(fanti, specific_best)

generate_name_by_jianti_wuxing()