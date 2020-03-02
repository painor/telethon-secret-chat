from distutils.core import setup

setup(
    name='telethon_secret_chat',
    packages=['telethon_secret_chat'],
    version='0.1',
    license='MIT',
    description='Telethon secret chat plugin',
    author='painor',
    author_email='topcode.softwares@gmail.com',
    url='https://github.com/painor/telethon-secret-chat',
    download_url='https://github.com/painor/telethon-secret-chat/releases',
    keywords=['Telegram', 'Telethon', 'SecretChats', 'Plugin'],
    python_requires='>=3.5',
    install_requires=[  # I get to this in a second
        'telethon',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
