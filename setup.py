from setuptools import setup, find_packages

setup(
    name="demo",
    version='0.1.0',
    author='Base2Services R&D',
    author_email='itsupport@base2services.com',
    url='http://github.com/base2Services/demo-sam-package',
    packages=find_packages(),
    python_requires='>=3.6',
    setup_requires=["pytest-runner"],
    tests_require=["pytest","pytest_env"]
    )
