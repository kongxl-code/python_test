def process_components(components):
    # 创建一个字典来存储每个component的信息，包括其依赖和group
    component_info = {}
    # 创建一个字典来按group分组存储component
    group_components = {}
    
    # 初始化数据结构
    for item in components:
        component = item['component']
        group = item['group']
        dependency = item['dependency']
        
        component_info[component] = {
            'group': group,
            'dependency': dependency,
            'resolved': False,
            'i': -1,  # 初始化为-1，表示未确定
            'j': -1
        }
        
        if group not in group_components:
            group_components[group] = []
        group_components[group].append(component)
    
    # 确定每个component的层级(i)
    changed = True
    current_level = 0
    
    while changed:
        changed = False
        # 找出所有未解析且依赖已解析或无依赖的组件
        for component, info in component_info.items():
            if not info['resolved']:
                dependency = info['dependency']
                # 检查依赖是否满足
                if not dependency or (dependency in component_info and component_info[dependency]['resolved']):
                    info['i'] = current_level
                    info['resolved'] = True
                    changed = True
        
        if changed:
            current_level += 1
    
    # 处理无依赖但未解析的组件（可能是孤立的或循环依赖外的组件）
    for component, info in component_info.items():
        if not info['resolved']:
            info['i'] = current_level
            current_level += 1
    
    # 按group和层级对组件进行排序以确定j位置
    # 首先按group分组，然后在每个group内按层级和字母顺序排序
    for group, comp_list in group_components.items():
        # 对组内组件按层级(i)和组件名排序
        sorted_components = sorted(comp_list, key=lambda x: (component_info[x]['i'], x))
        
        # 分配j值
        for j, component in enumerate(sorted_components):
            component_info[component]['j'] = j
    
    # 构建结果列表
    result = []
    for component, info in component_info.items():
        result.append({
            'group': info['group'],
            'component': component,
            'i': info['i'],
            'j': info['j']
        })
    
    return result
