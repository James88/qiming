"""
给定的2个名字中随机天意选择一个
"""
import random

name_list1 = [
    '刘雅文',
]
name_list2 = [
    '刘宣妙',
    '刘思妙',
]
name_list3 = [
    # 水 木
    '刘泽娇',
]
name_for_choose = name_list1 + name_list2 + name_list3
# name_for_choose = ['刘雅文', '刘柚泽']

name_list = []
for i in range(10000):
    name = random.choice(name_for_choose)
    name_list.append(name)

# print(name_list)
name_list_dict = dict()
# 输出name_list中不重复的数据，并计算每个数据出现的次数
name_set = set(name_list)
for name in name_set:
    name_list_dict[name] = name_list.count(name)
    print(f"{name}出现了{name_list.count(name)}次")

# name_list_dict 按次数降序
name_list_dict = sorted(name_list_dict.items(), key=lambda x: x[1], reverse=True)
print(name_list_dict)
