try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'maze solver',
    'author': 'jyk',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['MAZE'],
    'scripts': [],
    'name': 'maze-solver'
}

setup(**config)