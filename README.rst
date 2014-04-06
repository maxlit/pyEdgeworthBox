==============
pyEdgeworthBox
==============

.. image:: https://github.com/maxlit/pyEdgeworthBox/blob/master/ex3.png

How to use it
------------

pyEdgeworthBox provides with a tool to plot the Edgeworth box and calculate equilibrium, core, pareto effective allocation etc in the pure exchange economy.
These are studied in the microeconomics courses.
A pure exchange economy consists of 2 consumers and 2 goods. Each consumer has her own preferences represented by a utility function and provided with some initial endowment of 2 goods (wich, however, could be 0).
The main class is EdgeBox where you need to put the utilities of each consumer and their initial endowments.
Consider an economy where the first consumer has a utility function u(x,y)=x^0.6*y^0.4 and the bundles of goods A and B (10,20), i.e. she prefers the good A over B.
The second consumer has a utility function u(x,y)=x^0.1*y^0.9 and the bundles of goods A and B (20,10), i.e. he prefers the good B over A.
 
This example (it's example 2b from http://www.pitt.edu/~mjl88/docs/1100/Problem_Set_06_Answers.pdf) can be calculated like this:

	#!/usr/bin/env python
	import pyEdgeworthBox as eb
	EB=eb.EdgeBox(u1=lambda x,y: x**0.6*y**0.4,u2=lambda x,y: x**0.1*y**0.9,IE1=[10,20],IE2=[20,10])
	EB.plot()

The functions to be handled over must be lambda expressions. So, the utility function of the first consumer u(x,y)=x^0.6*y^0.4 becomes the parameter u1=lambda x,y: x**0.6*y**0.4
Respectively, the utility function of the second consumer u(x,y)=x^0.1*y^0.9 becomes the parameter u2=lambda x,y: x**0.1*y**0.9
Initial endowments are represented by parameters IE1 and IE2 for the 1-st and the 2-nd consumers respectively.


Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.

How to get the calculated concepts
----------------------------------

* Pareto efficient allocations

The points used to draw the Pareto-efficient allocations are stored in PARETO property.
You should be however careful with questions like "Is the allocation (2,3) a Pareto-efficient one?".
Use the example from the previous chapter:

	import pyEdgeworthBox as eb
	EB=eb.EdgeBox(u1=lambda x,y: x**0.6*y**0.4,u2=lambda x,y: x**0.1*y**0.9,IE1=[10,20],IE2=[20,10])

This would be a false approach:

	(2,3) in EB.PARETO

The correct approach is

	3==EB._pareto(2)

Since the obtained solutions are often calculated to a certain extent of precision a better approach would be:

	abs(3-EB._pareto(2))<10e-6

* Core
The points used to draw the Pareto-efficient allocations are stored in CORE property. Again it contains only some points of the core.
The core contains Pareto-efficient allocations which are better than the initial endowments.

* Eqilibrium
Equilibrium consists of the allocation of goods and the price that supports it. The allocation of the 1-st consumer is store at EQ1 and 
of the 2-nd at EQ2 property respectively. The price of the 2-nd good is normalized to be 1, the price of the 1-st good is in p property.
The prices normalized in the way that their sum is 1 are stored in p_weighted property 

	print EB.EQ1
	>>> [26.307685800107304, 10.363637797581369]
	print EB.EQ2
	>>> [3.692314199892696, 19.63636220241863]
	print EB.p
	>>> 0.590909238781
	print EB.p_weighted
	>>> [0.37142862985297675, 0.6285713701470232]

* Budget line
The points used to draw the budget line str stored in BUDGET property

Plot
----------------------------------

In order to plot the Edgeworth box use the function plot()

	EB.plot()

.. image:: https://github.com/maxlit/pyEdgeworthBox/blob/master/ex1.png

Another example:

	EB2=eb.EdgeBox(u1=lambda x,y: x**2*y,u2=lambda x,y: x+y,IE1=[5,5],IE2=[5,5])
	EB2.plot()

.. image:: https://github.com/maxlit/pyEdgeworthBox/blob/master/ex2.png


Caution
-------
The computation is implemented only for the interior solutions! For "bad" functions solutions could deviate or not be achieved at all.

To Do's:
-------
...
