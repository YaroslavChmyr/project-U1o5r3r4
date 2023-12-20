from setuptools import setup, find_namespace_packages

setup(
    name='personal_assistant',
    version='1.0',
    packages=find_namespace_packages(),
    install_requires=[
        'prettytable'
    ],
    entry_points={
        'console_scripts': [
            'personal_assistant=personal_assistant:main',
        ],
    }
)