import logging
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

    file_handler = logging.FileHandler(os.path.join(log_directory, f"{name}.log"))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # 将handlers添加到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
