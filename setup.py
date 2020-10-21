import os
import setuptools


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setuptools.setup(
    author="Zagaran, Inc.",
    author_email="info@zagaran.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Simple tool to SSH into an Elastic Beanstalk server using AWS SSM.",
    entry_points={
        "console_scripts": ["eb-ssm=ssm.ssm:main"],
    },
    install_requires=["awsebcli"],
    keywords="aws eb ssm elastic beanstalk systems manager agent ssh",
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="eb-ssm",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    url="https://github.com/zagaran/eb-ssm",
    version="1.0.3",
)
