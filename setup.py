from setuptools import setup

setup(
    name='duplicates',
    version='0.0.1',
    packages=['tests', 'duplicates'],
    url='https://github.com/akcarsten/duplicates.git',
    license='MIT License',
    author='Carsten Klein',
    author_email='',
    description='Package to find duplicate files in and across folders',
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
