import re
from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
with open('telethon_secret_chat/version.py', 'r', encoding='utf-8') as f:
    version = re.search(r"^__version__\s*=\s*'(.*)'.*$",
                        f.read(), flags=re.MULTILINE).group(1)

setup(
    name='telethon_secret_chat',
    packages=['telethon_secret_chat'],
    version=version,
    license='MIT',
    description='Telethon secret chat plugin',
    author='painor',
    long_description=long_description,
    author_email='topcode.softwares@gmail.com',
    url='https://github.com/painor/telethon-secret-chat',
    download_url='https://github.com/painor/telethon-secret-chat/releases',
    keywords=['Telegram', 'Telethon', 'SecretChats', 'Plugin'],
    install_requires=[
        'telethon',
    ],

    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ],
)
