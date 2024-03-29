import numpy as np
import matplotlib.pyplot as plt
from math import copysign
from scipy.optimize import brenth
from scipy.optimize import fmin_l_bfgs_b,fmin_cg,fminbound


"""
sign of the number
"""
def sign(x):
    if x==0:
        return 0
    else:
        return copysign(1,x)

"""
if function f can't be computed, return None
"""
def f_None(f,x):
    try:
        return f(x)
    except:
        return None

"""
if the bound was touched returns None

L is the level of the function f
"""
def correct(x,y,f,L):
    eps=10e-5
    if abs(f(x,y)-L)>eps:
        return None
    else:
        return y

"""
if output can't be produced, return 0, if there's division by zero, then it looks for the limit and returns it
"""
def _(f,*x):
    try:
        out=f(*x)
        if out is None:
            return float("inf")
        else:
            return out
    except ZeroDivisionError:
        l = len(x)
        eps = abs(f(*[1e-02]*l) - f(*[1e-04]*l))
        # if converges
        if abs(f(*[1e-04]*l) - f(*[1e-06]*l)) < eps and abs(f(*[1e-06]*l)-f(*[1e-08 ]*l)) < eps:
            return f(*[1e-10]*l)
        else:
            return sign(f(*[1e-10]*l)) * float("inf")

"""
produces the array of the first items of the element of the array
"""
def fst(X):
    return list(map(lambda x: x[0],X))
"""
produces the array of the second items of the element of the array
"""
def snd(X):
    return list(map(lambda x: x[1],X))

"""
unpacks [(X_1,Y_1),...,(X_k,Y_k),...,(X_n,Y_n)] into [(X_1,...,X_k,...,X_n),(Y_1,...,Y_k,...,Y_n)]
"""
def unpack(X):
    return [fst(X),snd(X)]

"""
find the root of the function. If the ends of the interval have the same signs, try to make it smaller
"""
def rootalt(f,a,b):
    eps=(b-a)/64.0
    turn=0
    N_iter=10
    while abs(a-b)>eps and N_iter > 0:
        N_iter-=1
        try:
            #return fmin_cg(f,(a+b)/2.0)[0]
            return brenth(f,a,b)
        except ValueError:
            if turn==0:
                a=a+eps
                turn=1
            else:
                b=b+eps
                turn=0
    #return root2(f,a,b)
    return None

def root(f,a,b):
    a_init=a
    b_init=b
    eps=(b-a)/16.0
    turn=0
    N_iter=12
    while abs(a-b)>eps and N_iter > 0 and f(a)*f(b)>0:
        N_iter-=1
        if turn==0:
            a=a+eps
            turn=1
        else:
            b=b-eps
            turn=0
    try:
        return brenth(f,a,b)
    except ValueError:
        return fminbound(f,a_init,b_init)

    
     

def root2(f,a,b):
    return fmin_cg(f,(a+b)/2.0,disp=False)[0]

def root3(f,a,b):
    return fmin_l_bfgs_b(func=f,x0=(a+b)/2,bounds=[a,b])

"""
2-point numerical derivative
"""
def prime(f,dt=10e-3):
    return lambda x: (f(x+dt)-f(x-dt))/(2*dt)

"""
Marginal rate of substitution of a utility function u(.)
"""
def MRS(u):
    u_x=lambda x,y: prime(lambda z: u(z,y))(x)
    u_y=lambda x,y: prime(lambda z: u(x,z))(y)
    return lambda x,y: u_x(x,y)/u_y(x,y)

"""
Edgeworth Box parameter determine that to show on the plot
"""

class EdgeBoxParameter:
    #def __init__(self,pareto,core,U1,U2,endow,walras,budget,N):
        #boll_array=[pareto,core,U1,U2,endow,walras,budget]
    def __init__(self,N,pareto=True,core=True,eq=True,budget=True):
        self.N=N
        self.pareto=pareto
        self.core=core
        self.eq=eq
        self.budget=budget
        
defaultEBP=EdgeBoxParameter(100)        

class EdgeBox():
    def __init__(self,u1,u2,IE1,IE2,EBP=defaultEBP):
        self.core=0
        self.pareto=0
        self.eq=0
        self.p=[None,1]
        self.p_weighted=[None,None]
        self.u1=u1
        self.u2=u2
        self.IE1=IE1
        self.IE2=IE2
        self.IE=[IE1[0]+IE2[0],IE1[1]+IE2[1]]
        self.u2_compl=lambda x,y: u2(self.IE[0] - x, self.IE[1] - y)
        self.EBP=EBP
        self.dt=min(self.IE)/float(EBP.N)
        self.X=np.linspace(self.dt,self.IE[0]-self.dt,EBP.N)
        self.Y=np.linspace(self.dt,self.IE[1]-self.dt,EBP.N)
        self.calc_init()
        self.calc()

    # set points for a plot
    # e.g. set_points_for_plot('PARETO', self._pareto)
    # then one can use self.PARETO to plot the function self._pareto
    def set_points_for_plot(self, prop, fn, domain = None):
        if domain is None:
            domain = self.X
        points = list(map(fn, domain)) # set of some points from the budget line
        setattr(self, prop, list(zip(domain, points)))
    
    def calc(self):
        """
        calculate all solutions of the box
        """
        self.calc_pareto()
        self.calc_core()
        self.calc_eq()
        self.calc_budget()
    
    def calc_init(self):
        self.u1(*self.IE1)
        self.UIE1=self.u1(*self.IE1) # utility of the 1-st player at her initial endowment
        self.UIE2=self.u2(*self.IE2) # utility of the 2-nd player at her initial endowment
        self.u_ie_1=lambda x: root(lambda y: self.u1(x,y)-self.UIE1,self.Y[0],self.Y[-1]) # utility function at initial endowment of the 1-st participant
        self.u_ie_2=lambda x: root(lambda y: self.u2(x,y)-self.UIE2,self.Y[0],self.Y[-1])  # utility function at initial endowment of the 2-nd participant
        self.u_ie_2_compl=lambda x: -self.u_ie_2(self.IE[0]-x)+self.IE[1]                   # utility function at initial endowment of the 2-nd participant in terms of the 1-st

        #self.set_points_for_plot('U1', lambda x: correct(x, f_None(self.u_ie_1,x), self.u1, self.UIE1))
        #self.set_points_for_plot('U2', lambda x: correct(x, f_None(self.u_ie_2_compl,x), self.u2_compl, self.UIE2))
        U1 = map(lambda x: correct(x, f_None(self.u_ie_1,x), self.u1, self.UIE1), self.X)
        U2 = map(lambda x: correct(x, f_None(self.u_ie_2_compl,x), self.u2_compl, self.UIE2), self.X)
        self.U1 = list(filter(lambda x: x[0] is not None and x[1] is not None,zip(self.X,U1)))
        self.U2 = list(filter(lambda x: x[0] is not None and x[1] is not None,zip(self.X,U2)))
        U1_sort = sorted(self.U1,key=lambda x: x[1])
        U2_sort = sorted(self.U2,key=lambda x: x[1])
        if len(U1_sort)>0:
            self.U1_min=U1_sort[0]
            self.U1_max=U1_sort[-1]
        else:
            self.U1_min=None
            self.U1_max=None
        if len(U2_sort)>0:
            self.U2_min=U2_sort[0]
            self.U2_max=U2_sort[-1]
        else:
            self.U2_min=None
            self.U2_max=None
        # budget constraint with the price of y set to 1 
        # i.e. p*x + y = p*w1 + w2, then solved for y
        # i.e. y = p*(w1 - x) + w2
        self._B=lambda x,y,p: y - (p*(self.IE1[0] - x) + self.IE1[1])
    
    def calc_pareto(self):
        self.MRS1=MRS(self.u1) # marginal rate of substitution of the 1st participant
        self.MRS2=MRS(self.u2) # marginal rate of substitution of the 2nd participant
        # these can be used as offer/deamnd functions
        # MRS solved for p (i.e. not a function x and y, but x and p): x = f(y,p)
        self.pMRS1x = lambda y,p: root(lambda x: self.MRS1(x, y) - p, self.X[0], self.X[-1])
        # same, but y = g(x, p)
        self.pMRS1y = lambda x,p: root(lambda y: self.MRS1(x, y) - p, self.Y[0], self.Y[-1]) 
        # same for the 2nd participant
        self.pMRS2x = lambda y,p: root(lambda x: self.MRS2(x, y) - p, self.X[0], self.X[-1])
        self.pMRS2y = lambda x,p: root(lambda y: self.MRS2(x, y) - p, self.Y[0], self.Y[-1])
        # complementary demand functions for the 2nd participant (to be represented in terms of the 1st participant's goods)
        self.pMRS2x_compl = lambda y,p: root(lambda x: self.MRS2(self.IE[0] - x,  self.IE[1] - y) - p, self.X[0], self.X[-1]) #lambda y,p: self.IE[0] - self.pMRS2x(y,p)
        self.pMRS2y_compl = lambda x,p: root(lambda y: self.MRS2(self.IE[0] - x, self.IE[0] - y) - p, self.Y[0], self.Y[-1]) #lambda x,p: self.IE[1] - self.pMRS2y(x,p)
        #self.pMRS1 = lambda y,p: root(lambda x: self.MRS1(x, y) - p, self.X[0], self.X[-1]) # marginal rate of substitution of the 1st participant in terms of the price
        # ratio of marginal rates of substitution:
        self.mrs_ratio = lambda x,y: self.MRS1(x,y)/self.MRS2(self.IE[0]-x,self.IE[1]-y)
        self._pareto = lambda x: root(lambda y: self.mrs_ratio(x,y) - 1, self.Y[0], self.Y[-1]) # Pareto solutions in functional form
        #self._pareto=lambda x: root(lambda y: _(self.MRS1, x, y)/_(self.MRS2, self.IE[0] - x, self.IE[1] - y) - 1, self.Y[0], self.Y[-1]) # Pareto solutions in functional form
        self.set_points_for_plot('PARETO', lambda x: f_None(self._pareto,x))
        # ---
        # Point where Pareto efficient allocation is equivalent to the initial endowment (their utilities are equal) for the 1st participant
        PU1_X = root(lambda x: _(self._pareto,x) - _(self.u_ie_1,x), self.U1_min[0], self.U1_max[0])
        # Point where Pareto efficient allocation is equivalent to the initial endowment (their utilities are equal) for the 2ns participant
        PU2_X = root(lambda x: _(self._pareto,x) - _(self.u_ie_2_compl,x), self.U2_min[0], self.U2_max[0])
        PU1_Y = self.u_ie_1(PU1_X)
        PU2_Y = self.u_ie_2_compl(PU2_X)
        self.PU1 = [PU1_X,PU1_Y]
        self.PU2 = [PU2_X,PU2_Y]
        # in the budget constraint, replace the price parameter with MRS, thus the price parameter is gone:
        self._Bx = lambda x: root(lambda y: _(self._B,x,y,_(self.MRS1,x,y)),self.Y[0],self.Y[-1])
        
    def calc_core(self):
        CORE_X = filter(lambda x: x>=self.PU1[0] and x<=self.PU2[0], self.X)
        CORE_Y = map(lambda x: self._pareto(x), CORE_X)
        self.CORE = list(zip(CORE_X,CORE_Y)) # set of some solutions in the core (could be one, could be many or none)

    def calc_eq(self):
        EQ_X1=root(lambda x: _(self._pareto, x) - _(self._Bx, x), self.PU1[0], self.PU2[0])
        EQ_Y1=self._pareto(EQ_X1)
        EQ_X2=self.IE[0]-EQ_X1
        EQ_Y2=self.IE[1]-EQ_Y1
        self.EQ1=[EQ_X1,EQ_Y1] # equilibrium solution for the 1st participant
        self.EQ2=[EQ_X2,EQ_Y2] # equilibrium solution for the 2nd participant
        self.p=self.MRS1(*self.EQ1) # price vector
        self.p_weighted=[self.p/(self.p+1),1/(self.p+1)]
        self.UEQ1=self.u1(*self.EQ1) # value of utility function of the 1st participant at her equilibrium point (functional form)
        self.UEQ2=self.u2(*self.EQ2) # value of utility function of the 2nd participant at her equilibrium point (functional form)

        self.u_eq_1=lambda x: root(lambda y: self.u1(x,y)-self.UEQ1,self.Y[0],self.Y[-1]) 
        self.u_eq_2=lambda x: root(lambda y: self.u2(x,y)-self.UEQ2,self.Y[0],self.Y[-1])
        self.u_eq_2_compl=lambda x: -self.u_eq_2(self.IE[0]-x)+self.IE[1]
        
        self.set_points_for_plot('U1_EQ', lambda x: correct(x, f_None(self.u_eq_1,x), self.u1, self.UEQ1))
        self.set_points_for_plot('U2_EQ', lambda x: correct(x, f_None(self.u_eq_2_compl,x), self.u2_compl, self.UEQ2))
        
    def calc_budget(self,price=None):
        if price is None:
            price=self.p
            
        self.Bp=lambda x: price*self.IE1[0]+self.IE1[1]-price*x # budget line (functional form)
        self.set_points_for_plot('BUDGET', self.Bp)        
    
    def plot(self, graphs = ['utility', 'pareto', 'budget', 'core', 'eq'], fname=None, equal_axis=False):
        standard_graphs = ['utility', 'pareto', 'budget', 'core', 'eq']
        plot_endow,=plt.plot(self.IE1[0],self.IE1[1],color="grey",marker="o")
        supply_1 = self.IE1[0] + self.IE2[0]
        supply_2 = self.IE1[1] + self.IE2[1]
        plot_upper_limit, = plt.plot([0, supply_1], [supply_2, supply_2], color="grey", linewidth=.5)
        plot_right_limit, = plt.plot([supply_1, supply_1], [0, supply_2], color="grey", linewidth=.5)
        #plt.annotate("IE", (self.IE1[0], self.IE1[1]), textcoords="offset points", xytext=(5,5), ha='right')
        #m=max(self.IE[0],self.IE[1])
        #plt.axis([0, m, 0, m])
        if equal_axis:
            # Set the aspect ratio to be equal, so that the plot is not skewed
            plt.gca().set_aspect('equal', adjustable='box')
        margin_scale = 1.15
        plt.axis([0, supply_1*margin_scale, 0, supply_2*margin_scale])
        _plots = {}
        if 'utility' in graphs:
            plot_U1,=plt.plot(*unpack(self.U1),color="blue")
            plot_U2,=plt.plot(*unpack(self.U2),color="brown")
            _plots['utility'] = [plot_U1, plot_U2]
        if 'pareto' in graphs:
            plot_pareto,=plt.plot(*unpack(self.PARETO),linewidth=2,color="red")
            _plots['pareto'] = [plot_pareto]
        if 'core' in graphs:
            plot_core,=plt.plot(*unpack(self.CORE),color="orange",linewidth=5)
            _plots['core'] = [plot_core]
        if 'eq' in graphs:
            plot_U1_EQ,=plt.plot(*unpack(self.U1_EQ),ls='--',color="blue")
            plot_U2_EQ,=plt.plot(*unpack(self.U2_EQ),ls='--',color="brown")
            plot_walras,=plt.plot(self.EQ1[0],self.EQ1[1],color="black",marker="o")
            # [p=(%s;1)] % ,self.p
            # Adding the price vector
            plt.quiver(self.EQ1[0], self.EQ1[1], self.p, 1, angles='xy', scale_units='xy', scale=1, color='green')
            # annotation for the vector
            plt.text(self.EQ1[0] + self.p * 1.15, self.EQ1[1] + 1.15, 'p', horizontalalignment='right', verticalalignment='top', fontweight='bold')
            _plots['eq'] = [plot_U1_EQ, plot_U2_EQ, plot_walras]
        if 'budget' in graphs:
            plot_budget,=plt.plot(*unpack(self.BUDGET),color="green")
            #plt.plot(self.PU1[0],self.PU1[1],color="blue",marker="o")
            #plt.plot(self.PU2[0],self.PU2[1],color="brown",marker="o")
            _plots['budget'] = [plot_budget]

        plt.title("Edgeworth Box")
        legends = {
            'pareto': ['Pareto'],
            'utility': ['init. U1', 'init U2'],
            'core': ['Core'],
            'eq': ['U1 at eq.', 'U2 at eq.', 'Walras eq.'],
            'budget': ['Budget line'],
        }

        # Add non-standard graphs, i.e. those that user adds manually (customization)
        non_standard_graphs = [graph for graph in graphs if graph not in standard_graphs]
        for non_standard_graph in non_standard_graphs:
            prop = getattr(self, non_standard_graph, None)
            if prop is not None:
                tmp_plot, = plt.plot(*unpack(prop), label=non_standard_graph)
                _plots[non_standard_graph] = [tmp_plot]
                legends[non_standard_graph] = [non_standard_graph]

        labels = ['init. endow.'] + sum([legends[graph] for graph in graphs if graph in legends], [])
        plots = [plot_endow] + sum([_plots[graph] for graph in graphs if graph in _plots], [])
        plt.legend(plots, labels)
        #Axes Dscription
        plt.xlabel("Units of 1-st good")
        plt.ylabel("Units of 2-nd good")
        plt.grid()
        if fname is not None:
            plt.savefig(fname)
            plt.close()
        else:
            plt.show(block=False)