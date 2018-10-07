"""Package BCI Learning Studio"""
import os
import subprocess

import setuptools


def _get_git_hash():
    dir_ = os.path.dirname(__file__)
    hash_ = subprocess.check_output([
        'git', '-C', dir_, 'rev-parse', '--short', 'HEAD'])
    return hash_.strip().decode('utf-8')


def _update_version_string_with_git_hash(path):
    try:
        hash_ = _get_git_hash()
    except Exception:  # pylint: disable=broad-except
        return

    with open(path, 'r') as file_:
        base_version = file_.read().strip().split('-')[0]
        version = '%s-%s' % (base_version, hash_)
    with open(path, 'w') as file_:
        file_.write(version)


def _get_version():
    path = os.path.join(
        os.path.dirname(__file__), 'bci_learning_studio', 'VERSION')

    try:
        _update_version_string_with_git_hash(path)
    except Exception:  # pylint: disable=broad-except
        pass

    with open(path, 'r') as file_:
        return file_.read().strip()


def _get_package_data():
    return ['VERSION']


def _get_long_description():
    with open('README.md', 'r') as fileobj:
        return fileobj.read()


def _set_up():
    setuptools.setup(
        name='bci_learning_studio',
        version=_get_version(),
        author='moto',
        author_email='moto@hellomoto.ai',
        description='Collective tools for train BCI system.',
        long_description=_get_long_description(),
        long_description_content_type='text/markdown',
        url='https://github.com/hellomoto-ai/bci-learning-studio',
        packages=setuptools.find_packages(
            exclude=['tests*'],
        ),
        test_suite='tests',
        install_requires=[
            'openbci_interface'
        ],
        extras_require={
            'dev': [
                'pylint',
                'flake8',
                'flake8-print',
                'pytest',
                'pytest-cov',
                'pytest-mock',
            ],
        },
        package_data={
            'bci_learning_studio': _get_package_data(),
        },
        entry_points={
            'console_scripts': [
                'bci_learning_studio = bci_learning_studio.__main__:main',
            ]
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    )


if __name__ == '__main__':
    _set_up()
