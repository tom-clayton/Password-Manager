
from setuptools import setup

setup(
    name='passwordmanager',
    version='0.1.0',
    description='Tkinter Password Manager',
    author='Tom Clayton',
    author_email='clayton_tom@yahoo.com',
    url='https://github.com/Tom-Clayton/Password-Manager',
    packages=['passwordmanager'],
    install_requires=[
        'pyperclip',
        'pycryptodome',
    ],
    entry_points={
        'console_scripts':['pman=passwordmanager.controller:main']
    },
)

