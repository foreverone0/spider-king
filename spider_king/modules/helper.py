
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


def cookies_to_dict(cookies):
    """
    将cookies字符串转换为字典

    :param cookies:
    :return:
    """
    cookies = cookies.split(";")
    cookies = [cookie.strip() for cookie in cookies]
    cookies = [cookie.split("=", 1) for cookie in cookies]
    cookies = {cookie[0]: cookie[1] for cookie in cookies if len(cookie) == 2}
    return cookies