from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = [
    'flowkit',
    'numpy',
    'pandas',
    'scipy',
    'matplotlib'
]

setup(
    name='FlowQC',
    version='0.1',
    packages=find_packages(),
    description='A Python library for detecting anomalous events in flow cytometry data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Scott White",
    license='BSD',
    url="https://github.com/whitews/flowqc",
    ext_modules=[],
    install_requires=reqs,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6'
    ]
)
