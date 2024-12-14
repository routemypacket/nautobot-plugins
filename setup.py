import os
from setuptools import setup, find_packages

setup(
    name='nautobot-update-github',
    version='0.1.0',
    description='Nautobot plugin to update a GitHub repository.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Rafay Rasool',
    author_email='rafay_rasool30@hotmail.com',
    url='https://github.com/routemypacket/nautobot-plugins.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'nautobot>=1.0.0',
        'GitPython',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)