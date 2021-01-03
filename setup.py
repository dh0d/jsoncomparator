from setuptools import setup
import jsoncomparator
setup(
    name='jsoncomparator',
    packages=['jsoncomparator'],
    version='0.1.0',
    description='Utility for JSON comparsion',
    author='Dmitry Khodatsky',
    license='Apache Software License',
    install_requires=['multimethod'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    keywords=['json', 'comparsion', 'compare', 'diff'],
)
