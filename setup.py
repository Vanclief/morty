from setuptools import setup

setup(  name='Morty',
        version='0.2',
        description='Time to get Schwifty!',
        url='http://github.com/vanclief/morty',
        author='Franco Valencia, Ruben Stranders',
        packages=['morty'],
        entry_points= {
            'console_scripts': [
                'backtest=morty.backtest:main',
                'papertrade=morty.papertrade:main',
                'livetrade=morty.livetrade:main'
                ]
            },
        install_requires=[
            'requests',
            'configparser',
            'pandas'
            ],
        dependency_links=[
            # 'http://github.com/???/???'
            ],
        zip_safe=False)
