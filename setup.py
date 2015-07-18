from setuptools import setup, find_packages

setup(
    name='py_backup_pfsense',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'setuptools-lint',
        'pytest',
        'requests',
        'sh',
    ],
    entry_points='''
        [console_scripts]
        py_backup_pfsense=py_backup_pfsense.main:main
    ''',
)
