import setuptools

setuptools.setup(
    name='Patterns',
    version='0.1.0',
    author='Pochang Lee',
    author_email='stupidgod08@yahoo.com.tw',
    description='A django package made for handling third party payment',
    long_description='A django package made for handling third party payment',
    long_description_content_type='text/markdown',
    url='https://github.com/pochangl/patterns',
    install_requires=[
        'six',
    ],
    packages=setuptools.find_packages(
        exclude = [
            'test-server'
        ]
    ),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
    ],
)
