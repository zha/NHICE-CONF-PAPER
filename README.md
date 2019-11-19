# A simple algorithm for calculating overall SHGC and U-factor
* At this moment I only build it such that I can use it for my thesis. More funtionality will come in the future.
* To install:
```
pip install git+https://github.com/zha/window-overall-prop.git
```
## Usage example
```python
from window_overall import WinProp
width = 1
depth = 1
gap  = 'AIR'
out_layer_optical_dir = "./dat/CLEAR_6.DAT"
in_layer_optical_dir = "./dat/CLEAR_6.DAT"
win_obj = WinProp(width, depth, out_layer_optical_dir, in_layer_optical_dir,'AIR')
print(win_obj.overallSHGC)
print(win_obj.overallU)
```
## Demo usage for NHICE conference paper
[Demo file here](demo/example.ipynb)

