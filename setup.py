try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Игровой сервер minecraft.of.by',
    'author': 'Dmitry Rendov',
    'url': 'https://minecraft.of.by',
    'author_email': 'drendov@gmail.com',
    'version': '1.1',
    'install_requires': ['nose'],
    'packages': ['mob'],
    'scripts': [],
    'name': 'mob'
}

setup(**config)
