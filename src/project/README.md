# Lamp (Work in Progress)
This program takes as input night time images of lit street lamps. Presently, the yield is approximate spectral profile of each lamp and it's location.

This project is still a work in progress. The end product uses unsupervised classification techniques to label types of lamps (high pressure sodium vs cool white LED vs ect.). Every computationally expensive task's result will be cached in a database using methods transparent to the user.

# What it do?

The `topograph` subcommand produces a topographical leveling of an input image. This is used to standardize yield accross multiple input's with lossy compression filetypes. This intermediate step always yields a png (because it's lossless) that is cached in a database, to prevent repeat work.

The `cluster` subcommand identifies lamps by using **dbscan** in each color channel (red-green-blue) over high intensity values. The area of each cluster represents the measured output of a lamp in each channel. **Lamps** are grouped clusters from each channel who share the most overlapping area. The **location** of a lamp is the **medoid** of it's smallest cluster. This command yields a *splat image* to help visualize lamps, and prints **location** and **approximate spectral simplex** of lamps.
```
lamp topograph ./input_image.jpg . --step 10              # produces output.png
lamp cluster   ./output.png      . --size 20 --radius 30  # replaces output.png
```

# Install lamplibs
Libraries we developed can be installed using pip as designated below:
```
pip install --upgrade --user git+https://github.com/probinso/color-polution.git@master#subdirectory=src/project
```
Or if downloaded locally
```
pip install --upgrade --user .
```

Once installed, commands and subcommands can be run, as described, using:
```
lamp --help
```
To uninstall
```
pip uninstall lamplibs
```
# Why Python
Python was selected for this course because it is a language both primary [contributors](../../AUTHORS.md) are familiar with. Python is a mature, simple, and expressive programming language. Python also has a large body of public prior work, that we leverage to decrease development release time.

Although most work is done in python3, there is some legacy python2.7 code that we will tend to as needed. We strongly encourage the use of python3 at this point. [Here](https://www.webucator.com/blog/2016/03/still-using-python-2-it-is-time-to-upgrade/) is a nice article about adoption of python3.

To help with this course, the complete playlist of python tutorial videos can be found [here](https://www.youtube.com/playlist?list=PL96V6k-MWWMhAXQmH0AJDKM6WnfpaCx4S). This will be broken into smaller topical lists on the youtube channel [here](https://www.youtube.com/channel/UC-EKRSRFcQ1Uda8oGVVZl7Q).

# How it do?
