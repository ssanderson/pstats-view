pstatsviewer
=============

A Graphical, Interactive PStats viewer/diff tool for IPython Notebook.

```
v1 = StatsViewer("./naive.stats")
v2 = StatsViewer("./fast.stats")

v1.view(25, 'cumtime')
```


To see what the output of `StatsViewer` looks like statically, you can look at 
[NBViewer](http://nbviewer.ipython.org/github/ssanderson/pstats-view/blob/master/examples/ExampleView.ipynb)
(note that the interactive widget will not display on nbviewer).

##Running the Example Notebook
1. Clone this repo.
2. Run `pip install -r requirements.txt`.
3. Run `ipython notebook examples/ExampleView.ipynb`.
