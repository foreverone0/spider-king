from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='spider_king',  # 项目名称
    version='0.2.7',  # 项目版本
    packages=find_packages(),  # 自动发现项目中的包
    description='spider core',  # 项目简介
    install_requires=requirements,  # 项目依赖
)
