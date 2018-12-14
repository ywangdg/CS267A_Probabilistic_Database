# CS267A Probabilistic database

## Dependencies
1. python>=3.4.3
2. numpy==1.15.4
3. pandas==0.23.4

These dependencies are in the `requiremens.txt` file.

To install the dependencies, run

`pip install -r requirements.txt` for python2 and `pip3 install -r requirements.txt` for python3

## `main.py`
`main.py` controls the overall logic of the program. The extension is also invoked in the main.py program.

### Files needed for Running `main.py`

1. query file
2. table files
3. `query_parser.py`
4. `lifted_algorithm.py`
5. `file_create.py`
6. `utils.py`


## Sample Command for running main.py
`python qeval.py --q query1.txt -t t1.txt-t t2.txt -t t3.txt -t t4.txt`

## Generating Random Data for Testing

P, Q and R tables and they are similar to the input given in the examples **P(x), Q(x), R(x, y) and T(x,y)**

#### Tables Generated

```
t1.txt
t2.txt
t3.txt
t4.txt
```

## Extension

The implementation of the gibbs sampling extension is located in the `GibbsSampling.py` file. This file is called in the main.py program. You can change the number of steps,`num_step`, for each sampling process in the main.py program. If `num_step` is large, approximation result is closed to the real value, but it might take longer time compute.
