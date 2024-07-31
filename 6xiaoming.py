import json
import helper


def generate_xiao_ming(wuxing_spec):
    """
    生成小名
    """
    bi_hua_max = 16
    with open('data/wuxing_dict_jianti.json', 'r', encoding='utf-8') as f:
        wuxing_dict = json.load(f)

    word_list = []
    for wuxing in wuxing_dict:
        if wuxing_spec == wuxing:
            for bihua in wuxing_dict[wuxing]:
                if int(bihua) < bi_hua_max:
                    word_list += wuxing_dict[wuxing][bihua]
            break

    name_list = []
    common_words = helper.get_common_name_words()
    for word in word_list:
        if word in common_words:
            name_list.append('小' + word)

    return name_list


if __name__ == '__main__':
    name_list = generate_xiao_ming('jin')

    print(name_list)