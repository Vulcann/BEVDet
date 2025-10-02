import pickle

def inspect_pkl(path, max_items=5):
    """通用的pkl文件浏览器
    
    Args:
        path (str): pkl文件路径
        max_items (int): 如果是list/dict，只显示前多少个元素
    """
    with open(path, "rb") as f:
        try:
            data = pickle.load(f)
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            return

    print(f"✅ 成功读取: {path}")
    print(f"数据类型: {type(data)}")

    if isinstance(data, dict):
        print(f"字典大小: {len(data)}，展示前 {max_items} 个 key:")
        for i, (k, v) in enumerate(data.items()):
            if i >= max_items:
                break
            print(f"  {i+1}. {k} -> {type(v)} | {str(v)[:20000]}")
    elif isinstance(data, list):
        print(f"列表长度: {len(data)}，展示前 {max_items} 个元素:")
        for i, item in enumerate(data[:max_items]):
            print(f"  {i+1}. {type(item)} | {str(item)[:500]}")
    else:
        print("内容预览:", str(data)[:500])

    return data

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python check_pkl.py <pkl文件路径>")
    else:
        inspect_pkl(sys.argv[1])# -*- coding: utf-8 -*-
