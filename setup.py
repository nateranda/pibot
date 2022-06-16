from setuptools import setup

setup(
    name='pibot',
    version='0.1.0',
    py_modules=['pibot'],
    install_requires=[
        'click',
        'feedparser',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'pibot = pibot:main',
        ],
    },
)