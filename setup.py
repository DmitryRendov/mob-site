try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Игровой сервер minecraft.of.by',
    'author': 'Dmitry Vl.Rendov',
    'url': 'http://minecraft.of.by',
    'author_email': 'drendov@gmail.com',
    'version': ''
               '0.1',
    'install_requires': ['nose'],
    'packages': ['mob'],
    'scripts': [],
    'name': 'mob'
}

setup(**config)
