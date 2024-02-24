import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
from rich.console import Console
import os

console = Console(force_terminal=True, color_system="truecolor")


def get_logger(name: str):
    # 创建一个logger
    logger = logging.getLogger(name)

    # 设置日志级别
    logger.setLevel(logging.DEBUG)

    # 创建一个用于控制台输出的 RichHandler
    console_handler = RichHandler(rich_tracebacks=True, level=logging.INFO, console=console)
    console_handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))

    # 创建一个用于文件输出的 FileHandler
    log_directory = "log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    file_handler = logging.FileHandler(os.path.join(log_directory, f"{name}.log"), encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # 将handlers添加到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def config_logger(path, name):
    """
    配置日志
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    # 配置日志
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler = RotatingFileHandler(
        os.path.join(path, f'{name}.log'),
        maxBytes=1024 * 1024 * 100,
        backupCount=20,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logging.getLogger('httpx').setLevel(logging.ERROR)
    logging.getLogger('httpcore').setLevel(logging.ERROR)

    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
