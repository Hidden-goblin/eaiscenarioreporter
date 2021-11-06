# -*- coding: utf-8 -*-
# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="eaiscenarioreporter",
    version="0.0.18",
    description="Turns folder of gherkin feature files into a docx file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Text Processing'

    ],
    install_requires=[
        'behave',
        'python-docx',
        'Pillow'
    ],
    keywords=["BDD", "Gherkin", "behave", "docx"],
    python_requires='>=3.7, !=2.*',
    packages=find_packages(),
    include_package_data=True,
    py_modules=["featurereporter"],
    # packages=['featurereporter'],
    package_dir={'featurereporter': 'featurereporter'},
    package_data={'featurereporter': ['assets/*.png', 'assets/*.txt']},
    author="Eric Aïvayan",
    author_email="eric.aivayan@free.fr",
    url="https://github.com/Hidden-goblin/eaiscenarioreporter.git",
    data_files=[('assets', ['featurereporter/assets/valid.png',
                            'featurereporter/assets/warning.png'])],
    entry_points={"console_scripts": ["featurereporter=featurereporter.featurereporter:main"]}
)
