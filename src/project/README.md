# Lamp (work in progress)
This is a program to automatically identify light source types from photographs taken at night. The program uses data smoothing and unsupervised learning techniques to classify light sources. 

Examples of light types:
- Moon
- Cool White LEDs
- Warm White LEDs
- High Pressure Sodium
- Low Pressure Sodium

### Current Status
This program takes as input night time images of lit street lamps. Presently, the yield is approximate spectral profile of each lamp and it's location.

This project is still a work in progress. The end product uses unsupervised classification techniques to label types of lamps (high pressure sodium vs cool white LED vs ect.). Every computationally expensive task's result will be cached in a database using methods transparent to the user.

# Run without install of lamplibs
The program requires the following libraries to run:
- appdirs
- argcomplete
- argparse
- imread
- matplotlib
- numpy
- Pillow
- pony
- scipy
- scikit-learn

To run the program without installation replace `lamp` with `./lamp-runner.py` in the examples, and ignore the Install section.

# Install lamplibs
Libraries we developed can be installed using pip as designated below:
```
$ pip install --upgrade git+https://github.com/probinso/color-polution.git@master#subdirectory=src/project
```
Or if downloaded locally
```
$ pip install --upgrade .
```
To uninstall
```
$ pip uninstall lamplibs
```

# What it do?
Once installed, commands and subcommands can be run, as described, using
```
$ lamp --help
```
The `topograph` subcommand produces a topographical leveling of an input image. This is used to standardize yield accross multiple input's with lossy compression filetypes. This intermediate step always yields a png (because it's lossless) that is cached in a database, to prevent repeat work.

The `cluster` subcommand identifies lamps by using **dbscan** in each color channel (red-green-blue) over high intensity values. The area of each cluster represents the measured output of a lamp in each channel. **Lamps** are grouped clusters from each channel who share the most overlapping area. The **location** of a lamp is the **medoid** of it's smallest cluster. This command yields a *splat image* to help visualize lamps, and prints **location** and **approximate spectral simplex** of lamps.
```
$ lamp topograph ./input_image.jpg . --step 10              # produces output.png
$ lamp cluster   ./output.png      . --size 20 --radius 30  # replaces output.png
```

The `purge` subcommand purges your system of the existing caching database.
```bash
$ ./lamp purge
are you sure you want to purge? (y/n): y
store purged
```

# Why Python
Python was selected for this course because it is a language both primary [contributors](../../AUTHORS.md) are familiar with. Python is a mature, simple, and expressive programming language. Python also has a large body of public prior work, that we leverage to decrease development release time.

Although most work is done in python3, there is some legacy python2.7 code that we will tend to as needed. We strongly encourage the use of python3 at this point. [Here](https://www.webucator.com/blog/2016/03/still-using-python-2-it-is-time-to-upgrade/) is a nice article about adoption of python3.

To help with this course, the complete playlist of python tutorial videos can be found [here](https://www.youtube.com/playlist?list=PL96V6k-MWWMhAXQmH0AJDKM6WnfpaCx4S). This will be broken into smaller topical lists on the youtube channel [here](https://www.youtube.com/channel/UC-EKRSRFcQ1Uda8oGVVZl7Q).

# How it do?
