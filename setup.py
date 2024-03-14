from setuptools import setup
import re
import os


if os.path.exists("requirements.txt"):
    with open("requirements.txt", encoding="utf-8") as r:
        requires = [i.strip() for i in r]
else:
    requires = ["ffmpeg-python==0.2.0"]

with open("RCutter/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

setup(
    name="RCutter",
    version=version,
    install_requires=requires,
    author="surena",
    author_email="ram3a1999.info@gmail.com",
    url="https://github.com/r3a70/cutter"
)
