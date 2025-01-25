import random
import string

def generate_unique_dict_list(count):
    all_letters = list(string.ascii_uppercase)
    unique_dicts = []
    # 记录已经生成的字典，用于去重
    generated_dicts = set()

    while len(unique_dicts) < count:
        # 随机选择两个不同的字母
        random.shuffle(all_letters)
        module = all_letters[0]
        dependency = all_letters[1]

        # 构建字典
        new_dict = {'module': module, 'dependency': dependency, 'status': True}

        # 将字典转换为可哈希的元组，以便存储在集合中进行去重检查
        dict_tuple = (module, dependency)

        if dict_tuple not in generated_dicts:
            unique_dicts.append(new_dict)
            generated_dicts.add(dict_tuple)

    return unique_dicts
