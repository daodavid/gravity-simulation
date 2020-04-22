import setuptools

with open("README.md",'r')  as fh:
    long_description = fh.read()

print(long_description)    
#https://www.codementor.io/@ajayagrawal295/how-to-publish-your-own-python-package-12tbhi20tf
setuptools.setup(
   name="gravity-simulation",
   version="2.0.1",
   description ="calculation and visualization of n-bodies gravity",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/daodavid/gravity-simulation",
   author_email= "dstankov1993@gmail.com",
   license="MIT",
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   packages=["gravity_simulation"],
   include_package_data=True
)
