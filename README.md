[![Build Status](https://travis-ci.org/PNProductions/video-seam-merging.svg?branch=master)](https://travis-ci.org/PNProductions/video-seam-merging)

Video Seam Merging
======
This is a Python implementation of [IMAGE RESIZING USING IMPROVED SEAM MERGING](http://www.mirlab.org/conference_papers/International_Conference/ICASSP%202012/pdfs/0001261.pdf) method.

Requirements
------------------
To run this code you need the following packages:

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [OpenCV](http://opencv.org/)
* [Numpy](http://www.numpy.org/)
* [Cython](https://github.com/pmneila/PyMaxflow)
* [numexpr](https://github.com/pydata/numexpr)

Maybe it should work also on other version of python, but it's untested.

**Everything but OpenCV can be installed via `pip install -r requirements`**

Installation
-----------------
To install everything just run:

```shell
python setup.py install
```

Maybe you have to run it with `sudo`.

Testing
-----------------
Test are provided via [`unittest`](https://docs.python.org/2/library/unittest.html).

To run them all:

```shell
nosetests
```

Examples
-----------------

```python
from seam_merging import SeamMergingWithDecomposition, importance_map, cartoon_image

# Setup
image = imread('your_image.png')
cartoon = cartoon_image(image) # TODO!!!
importance = importance_map(image) # TODO!!!
number_of_pixels = 100

# Start algorithm
result = seam_merging(image, cartoon, importance, number_of_pixels)
imwrite('result.png', result)
```

The parameter `number_of_pixels` should be `-image_size < number_of_pixels < ∞`.


Final Notes
-----------------
This library is already in development, so don't use it for __real__ purposes.
