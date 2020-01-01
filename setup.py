import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udidata",
    version="0.0.1",
    author="Udi Yosovzon",
    # author_email="author@example.com",
    description="Tools for manipulating my dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udiy/udidata",
    packages=setuptools.find_packages(),
    install_requires=[
          "numpy",
          "pandas",
          "plotly"
          
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)