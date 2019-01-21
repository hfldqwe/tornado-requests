import setuptools
from setuptools import setup

def read(file):
	with open(file,"r") as fn:
		return fn.read()

setup(
	name='tornado-requests',
    version='0.1.2',
    description='对tornado中AsyncHTTPClient的一个简单封装',
	long_description = read("README.md"),
	long_description_content_type="text/markdown",
    url='https://github.com/hfldqwe/tornado-requests.git',
    author='hfldqwe',
    author_email='1941066681@qq.com',
    license='MIT',
    packages=setuptools.find_packages())
