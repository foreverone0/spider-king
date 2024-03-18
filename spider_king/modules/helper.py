import re
from urllib import parse
from urllib.parse import urlparse


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

def get_filename_from_cd(cd):
    """从 Content-Disposition 中提取文件名"""
    if not cd:
        return None
    fname = re.findall(r'filename="([^"]+)"', cd)
    if len(fname) == 0:
        # 如果没有找到，尝试提取 filename*= 后的编码文件名
        fname = re.findall(r"filename\*=UTF-8''([^']+)", cd)

    if len(fname) == 1:
        # 对提取到的文件名进行 URL 解码
        return parse.unquote(fname[0])

    return None

def extract_domain(url):
    # 解析URL获取网络位置部分
    netloc = urlparse(url).netloc
    # 分割域名为部分
    parts = netloc.split('.')
    # 仅保留最后两部分（二级域名和顶级域名），并前置一个点构成cookie适用的域名格式
    domain_for_cookie = '.' + '.'.join(parts[-2:])
    return domain_for_cookie