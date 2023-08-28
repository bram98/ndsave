# ndsave
Have you ever wanted to save multidimensional numpy arrays and found that it was just a little awkward to do with numpy? Then this package is just for you!

## How to use it
 This package creates three functions. `ndsavetxt`, `ndloadtxt` and `ndgenfromtxt`. These functions work almost identically to their `numpy` counterparts, but they conveniently allow for saving and loading multidimensional arrays and they also keep track of any axis data. For example, if one axis represents time, you can easily store an array containing time data and a label showing the contents of that axis.

```python
ndsave.savetxt(fname, X, fmt='%.18e',
              delimiter=' ', newline='\n', comments='# ', 
              axisdata=None, axisnames=None,
              header='', footer='')
```
#### parameters
- `fname` File name. Where to save the file. `.txt` is added automatically.
- `X` Multidimensional array
- `axisdata` List of arrays. The i-th entry corresponds to the i-th axis in `X`. One should have `len( axisdata[i] ) == X.shape[i] `. For each axisdata entry that is missing, a `np.arange` with corresponding length is used.
- `axisnames` List of axis names (strings). For each axisname that is missing, the corresponding axis is used as a string
- `header` The header is used like in `np.savetxt`, but since the shape, axisnames and axisdata are saved like a header, the header is not at the top of the document.

```python
ndsave.loadtxt(fname, **kwargs)
ndsave.genfromtxt(fname, **kwargs)
```
#### parameters
- `fname` File name. Where to load the file from.
- `kwargs` See [https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html](https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html) and [https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html](https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html)
#### returns
- `(X, axisdata, axisnames)` tuple containing the n-dimensional np-array (`X`), the axisdata as list and the axisnames as list of strings.


## Example
```python
import numpy as np
import ndsave

shape = (5,3,4)
X = np.arange(np.product(shape)).reshape( shape )

time = [10.0, 10.1, 10.2, 10.3, 10.4]
height = [110, 115, 120]

ndsave.savetxt('test.txt', X, fmt='%i', axisdata=[time, height], axisnames=['time (s)', 'height (cm)', 'sample'])

X, axisdata, axisnames = ndsave.loadtxt('test.txt', dtype=np.uint32)
```
#### test.txt
```
# (5, 3, 4)
# axis 0 (time (s))
# [10. ,10.1,10.2,10.3,10.4]
# axis 1 (height (cm))
# [110,115,120]
# axis 2 (sample)
# [0,1,2,3]
0 1 2 3 
4 5 6 7 
8 9 10 11 

12 13 14 15 
16 17 18 19 
20 21 22 23 

24 25 26 27 
28 29 30 31 
32 33 34 35 

36 37 38 39 
40 41 42 43 
44 45 46 47 

48 49 50 51 
52 53 54 55 
56 57 58 59  
```
