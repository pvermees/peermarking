# Ranked peer marking

The purpose of these Python scripts is to:

1. Optimally allocate peer marking assignments using John Talbot's block designs

2. Randomly rename the pieces of coursework so as to ensure anonymity

3. Include marking instructions and a feedback form with the peer ranking assignments

4. Parse the completed feedback forms and extract the ranked assignments from them

5. Cast the rankings in a .pgf format and feed them into [Raman and Joachims'](http://peergrading.org/) peer ranking algorithm.

6. Collate the peer feedback for each student

Steps 1-3 are complete. The rest remains to be done.

To run the code, you must have Python3 installed on your system. Then you can either download this GitHub repository as a zip archive, or clone it on your system:

```
git clone https://github.com/pvermees/peermarking
```

This repository contains two Python scripts and five folders:

* `peermarking.py`: This code allocates the peer marking assignments (steps 1-3 above)

* `1-submissions`: This is where you must place the assessments. This folder is currently populated by a scientific writing exercise from GEOL001

* `2-peerassignments`: This folder is automatically populated by `peermarking.py`

* `3-reviews`: This folder contains the completed feedback forms from each student

* `4-feedback`: This folder will be automatically populated by `peermarking.py` to complete steps 4-6 above.

* `peerGrader.py`: A copy of [Raman and Joachims'](http://peergrading.org/) peer ranking algorithm. To by called from future versions of `peermarking.py`.

* `peergrader`: Helper code for [Raman and Joachims'](http://peergrading.org/) peer ranking module.

To execute the code, change your path to the main directory of the GitHub repository, then run

```
python3 peermarking.py
```

at the console.