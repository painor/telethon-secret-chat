from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='telethon_secret_chat',
    packages=['telethon_secret_chat'],
    version='0.1.2',
    license='MIT',
    description='Telethon secret chat plugin',
    author='painor',
    long_description=long_description,
    author_email='topcode.softwares@gmail.com',
    url='https://github.com/painor/telethon-secret-chat',
    download_url='https://github.com/painor/telethon-secret-chat/releases',
    keywords=['Telegram', 'Telethon', 'SecretChats', 'Plugin'],
    python_requires='>=3.5',
    install_requires=[
        'telethon',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
