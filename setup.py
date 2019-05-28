import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def test_requirements():
    requirements = []
    for line in read(os.path.join('tests', 'requirements.txt')).split('\n'):
        if "coveralls" not in line:
            requirements.append(line)

    return requirements


setup(
    name="CombCov",
    version="0.0.1",
    author="Permuta Triangle",
    author_email="permutatriangle@gmail.com",
    description="Searching for combinatorial covers.",
    license="GPL-3",
    keywords="combinatorics covers automatic discovery",
    url="https://github.com/PermutaTriangle/CombCov",
    project_urls={
        'Source': 'https://github.com/PermutaTriangle/CombCov',
        'Tracker': 'https://github.com/PermutaTriangle/CombCov/issues'
    },
    packages=find_packages(),
    long_description=read('README.md'),
    setup_requires=['pytest-runner'],
    tests_require=test_requirements(),
    python_requires='>=3.5',
    classifiers=[
        'Development Status ::  2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
