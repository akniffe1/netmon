from setuptools import setup

setup(
    name='netmon',
    version='1',
    packages=['package'],
    url='https://github.com/akniffe1/netmon',
    license='MIT',
    author='Adam Kniffen',
    author_email='akniffen@cisco.com',
    description='A simple utility to generate useful average statistics on network interface loads.',
    install_requires=['elasticsearch>=2.0.0'],
    entry_points={
        'console_scripts': [
            'netmon = package.netmon_cli:main'
        ]
    }
)