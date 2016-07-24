# Goal of Talk
In this bootcamp you will be getting exposure to general python and its application to web programming. This is a very small subset of the domains addressed with this language. I am here to talk about a problem that I'm working on in scientific computing, image processing, and machine learning.

# Uses for python
- ROSpy
- MicroPython
- numpy, scipy, sklearn
- django, flask
- pygame
- pyglut
- PyQt, pyGTK
- SQLAlchemy, sqlite3, pony
- ArcPy, geopy, googlemaps
- astropy
- pymc3
- sympy

If you are interested in diverse applications of python, to help inspire your future ventures, checkout `podcast.__init__`.

# Introduction
- I am Philip
- Python 4+ Years
  - Academic
    - Computer Graphics
    - Cryptography
  - Industry
    - Integration Tests - EMC
    - Process Management/Visualization - Galois Inc./Melinae
    - Education - PDXCodeGuild/Melinae/C&W Energy USA
    - Scientific/Data Analytic/Engineering/Visualisation - C&W Energy USA

# Project What/Why
- Develop low cost tools to quantitatively study light pollution
- Describe human eye response to light
- Describe how light pollution effects terrestrial telescopes
- Talk about turtles

# Problem Statement
Current measures for 'lighting needs' disregard metrics like 'blue light content'. Since 'blue light content' critically impacts many industries and habitats we hope to motivate a change in industry measurement standards. From nighttime photographs of lit street lamps, can we classify the type of bulb by approximating spectral profile?

# How are digital photo images made?
- Silicon sensor system
- RGBA
- Consequences of file formats

# Aurora Bore-ales

# Strategy for Analytics
- Standardize/Sanitize input image
- Identify/Locating light sources
- Extract RGB features from each lamp
  - Area of red green blue content
  - PDF fitting
- Store approximate spectral profile and position of lamps
- Classify lamps

# Tools used so far
- GitHub
  - Version Control
  - ZenHub
  - Jupyter and Markdown Rendering
- Amazon Web Services (AWS)
- ~1200 lines Python
  - imread, imhdr, Pillow
  - sklearn, scipy, numpy, matplotlib
  - PonyORM
- Jupyter
- Google Hangouts

# Technical goals
### Met goals
- Work must be reproducible
- Don't waste compute time
- Easily swap feature extraction strategy
- Simple CLI

### In progress
- Simple install
- Yield usable visualizations
- Conveniences must not increase complexity

### Not started
- Simplified automatic db versioning
- Simple user accounts
- Web UI / REST API
