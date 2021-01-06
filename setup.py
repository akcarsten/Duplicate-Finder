import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Duplicate-Finder',
    version='1.0.1',
    url='https://github.com/akcarsten/duplicates.git',
    license='MIT License',
    author='Carsten Klein',
    author_email='',
    description='Package to find duplicate files in and across folders',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
