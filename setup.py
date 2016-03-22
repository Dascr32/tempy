from setuptools import setup, find_packages

setup(
    name="tempy",
    version="0.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "Prettytable"
    ],
    entry_points='''
        [console_scripts]
        tempy=tempy.app:cli
    ''',
    # Metadata for PyPi
    author="Daniel Aguilar S",
    author_email="dasgaskl@gmail.com",
    description="CLI for cleaning Windows temporary files",
    keywords="cli temp windows clean delete",
    url="https://github.com/Dascr32/tempy"
)
