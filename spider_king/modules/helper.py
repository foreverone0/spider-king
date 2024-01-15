
def get_size_str(size: int):
    """获取文件大小字符串

    Args:
        size (int): 文件大小

    Returns:
        str: 文件大小字符串
    """
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f}KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / 1024 / 1024:.2f}MB"
    else:
        return f"{size / 1024 / 1024 / 1024:.2f}GB"
