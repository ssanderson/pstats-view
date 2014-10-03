pstatsviewer
=============

A Graphical, Interactive PStats viewer/diff tool for IPython Notebook.

##Examples:
```
v1 = StatsViewer("./naive.stats")
v2 = StatsViewer("./fast.stats")

v1.view(25, 'cumtime')
```
![TableView](img/tableoutput.png)
![GraphView](img/graphoutput.png)
```
v1.interact()
```
![InteractView](img/widgetoutput.png)
```
v1.compare(v2)
```
![DiffTable](img/difftable.png)
![DiffGraph](img/diffgraph.png)

More usage examples can be seen in the [Example Notebook on NBViewer](http://nbviewer.ipython.org/github/ssanderson/pstats-view/blob/master/examples/ExampleView.ipynb)
(note that the interactive widget view will not display on nbviewer).

##Running the Example Notebook
1. Clone this repo.
2. Run `pip install -r requirements.txt`.
3. Run `ipython notebook examples/ExampleView.ipynb`.
