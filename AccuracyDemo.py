# -*- coding:utf-8 -*-

'''
程序遵循python3编写，如使用python2运行，请自行按注释替换相应代码
'''

import os

SEPARATOR = ','


def load_file(path):
    map = {}
    if not os.path.exists(path):
        print(u'文件%s不存在!' % path)
        exit(1)
    with open(path, 'r') as f:
        count = 1
        for line in f:
            # 读取每行，第一列验证码编号作为key，第二列识别结果作为value
            cols = line.split(SEPARATOR, 2)
            key = cols[0].strip()
            value = cols[1].strip()
            # if map.has_key(key):
            if map.__contains__(key):
                print(u'警告：第%d行验证码编号%s已经加载过' % (count, key))
            map[key] = value
            count += 1
    return map


if __name__ == '__main__':
    # 1.用来检验的识别结果
    test_mappings = load_file('test-mappings.txt')

    # 2.正确的识别结果
    correct_mappings = load_file('mappings.txt')

    # 3.用来存放识别错误结果的文件
    with open('failures.txt', 'w') as f:
        # 4.计算识别准确率
        correct = 0  # 识别正确数量
        fail = 0  # 识别错误数量
        missing = 0  # 未识别数量
        total = 0
        for key in correct_mappings.keys():
            # if test_mappings.has_key(key):
            if test_mappings.__contains__(key):
                test_value = test_mappings[key]
                correct_value = correct_mappings[key]
                if correct_value.upper() == test_value.upper():
                    correct += 1
                else:
                    # 识别错误的验证码
                    f.write('%s,%s\n' % (key, test_value))
                    fail += 1
            else:
                # 未能识别的验证码
                f.write('%s,null\n' % key)
                missing += 1
            total += 1

    # 5.输出结果
    accur = float(correct) / total if total > 0 else 0.0
    print(u'识别率: %f' % accur)
    print(u'总计: %d, 正确: %d, 错误: %d, 未识别: %d\n' % (total, correct, fail, missing))
