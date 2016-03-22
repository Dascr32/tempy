from setuptools import setup, find_packages

setup(
    name="tempy",
    version="0.5",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,

    author="Daniel Aguilar S",
    author_email="dasgaskl@gmail.com",
    description="CLI for cleaning Windows temporary files",
    url="https://github.com/Dascr32/tempy",
    keywords="cli temp windows clean delete",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
    ],

    install_requires=[
        "Click",
        "Prettytable"
    ],

    entry_points='''
        [console_scripts]
        tempy=tempy.app:cli
    '''
)
