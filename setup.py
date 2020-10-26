import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitlab2mr",
    version="0.1.0",
    author="Jonas Schlagenhauf",
    description="A gitlab-to-myrepo config helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schlagenhauf/gitlab2mr",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['gitlab2mr=gitlab2mr.cli:main']
    },
    license='GNU General Public License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-gitlab',
        'click'
    ],
    python_requires='>=3.6'
)
