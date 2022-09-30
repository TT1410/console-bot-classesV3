from setuptools import setup, find_namespace_packages


setup(
    name='console_bot',
    version='3.0.0',
    description='Консольний бот',
    url='https://github.com/TT1410/console-bot-classesV3',
    author='Plaksii Taras',
    author_email='test@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['console-bot&classes = console_bot:main']}
)
