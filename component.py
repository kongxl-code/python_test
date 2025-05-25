"""
问题描述：
    组件依赖关系及坐标确定

"""

import json
def assign_coordinates(components):
    # 收集所有组件名称
    component_names = set()
    dependency_names = set()
    for entry in components:
        component_names.add(entry['component_name'])
        dependency_names.add(entry['dependency_name'])
    all_components = component_names.union(dependency_names)
    print(list(all_components))
    component_dict = dict()
    for component in list(all_components):
        component_dict.update({component: list(all_components).index(component)})
    print(component_dict)
    # 构建反向依赖图
    reverse_deps = {comp: [] for comp in all_components}
    for entry in components:
        dependency = entry['dependency_name']
        component = entry['component_name']
        reverse_deps[dependency].append(component)
    
    # 递归计算每个组件的x值
    cache = {}
    def compute_x(component):
        if component in cache:
            return cache[component]
        max_x = 0
        for dependent in reverse_deps[component]:
            current_x = compute_x(dependent)
            if current_x > max_x:
                max_x = current_x
        x = max_x + 1 if max_x != 0 else 1
        cache[component] = x
        return x
    
    for comp in all_components:
        compute_x(comp)
    
    # 按x值分组，并分配y值
    from collections import defaultdict
    groups = defaultdict(list)
    for comp in all_components:
        x = cache[comp]
        groups[x].append(comp)
    
    # 对每个x层的组件排序，并分配y值
    result = []
    for x in sorted(groups.keys()):
        sorted_components = sorted(groups[x])
        for y, comp in enumerate(sorted_components, 1):
            result.append({
                'component_name': comp,
                'id': component_dict[comp],
                'x': x,
                'y': y
            })
    dependencies = []
    for component in components:
        dependencies.append({
            'source': component_dict[component['component_name']],
            'target': component_dict[component['dependency_name']],
        })

    
    return result, dependencies

# 示例输入
components = [
    {"component_name": "B", "dependency_name": "D"},
    {"component_name": "C", "dependency_name": "D"},
    {"component_name": "A", "dependency_name": "B"},
    {"component_name": "E", "dependency_name": "D"},
    {"component_name": "F", "dependency_name": "D"},
    {"component_name": "G", "dependency_name": "B"},
    {"component_name": "H", "dependency_name": "F"},
]

# 执行函数
result, dependencies = assign_coordinates(components)

# 按component_name排序输出，方便查看
result_sorted = sorted(result, key=lambda x: x['component_name'])
print(json.dumps(result_sorted))
print(json.dumps(dependencies))
