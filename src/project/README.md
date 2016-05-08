# Why Python
Python was selected for this course because it is a language both primary [contributors](../../AUTHORS.md) are familiar with. Python is a mature, simple, and expressive programming language. Python also has a large body of public prior work, that we leverage to decrease development release time.

Although most work is done in python3, there is some legacy python2.7 code that we will tend to as needed. We strongly encourage the use of python3 at this point. [Here](https://www.webucator.com/blog/2016/03/still-using-python-2-it-is-time-to-upgrade/) is a nice article about adoption of python3.

To help with this course, the complete playlist of python tutorial videos can be found [here](https://www.youtube.com/playlist?list=PL96V6k-MWWMhAXQmH0AJDKM6WnfpaCx4S). This will be broken into smaller topical lists on the youtube channel [here](https://www.youtube.com/channel/UC-EKRSRFcQ1Uda8oGVVZl7Q).

# Install lamplibs
Libraries we developed can be installed using pip as designated below:
```
pip install --upgrade git+https://github.com/probinso/color-polution.git@master#subdirectory=src/project
```
Once installed, commands and subcommands can be run, as described, using:
```
lamp --help
```
To uninstall
```
pip uninstall lamplibs
```

# What it do?
This program has a few goals:
1. yield informative visualizations for communicating about light sources
2. yield a `spectral simplex` for every lamp in a sample image
3. classify types of light sources using their `spectral simplex` as a feature vector
4. allow for use of a shared database for all the above operations

## What is a spectral simplex?
Most digital images are stored as an array of pixels, each with a red, green, and blue channel. The spectral simplex is the percent of high intensity red, green, and blue for a given area.

# How it do?
## Libraries
- PonyORM :: pythonic object relational model
- Pillow, imread :: Reading and writing images
- matplotlib ::