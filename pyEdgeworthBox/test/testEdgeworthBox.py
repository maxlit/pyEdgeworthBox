import unittest
import pyEdgeworthBox as eb
from math import exp as e, sin, sqrt
# python -m unittest discover project_directory '*_test.py'
# cd Dropbox/scripts/edgeworth/pyEdgeworthBox
# python -m unittest testEdgeworthBox

class TestCF(unittest.TestCase):
    #cf=cf1+cf2        EB4=eb.EdgeBox(u2=lambda x,y: x**0.6*y**0.4,u1=lambda x,y: x**0.1*y**0.9,IE2=[10,20],IE1=[20,10])
    def setUp(self):
        self.u1=lambda x: x
        self.u2=lambda x: x
        self.tolerance=0.00001
        self.assertEqual(True,True)

    def pest_(self):
        l1=lambda x: sin(x)/x
        l2=lambda x: 1/x
        self.assertEqual(eb._(l1,0),1)
        self.assertEqual(eb._(l2,0),float("Inf"))

    def testRoot(self):
        f=lambda x: x**2-2*x+1
        self.assertAlmostEqual(eb.root(f,0,10),1)

    def testBoundedRoot(self):
        pass

    def testPrime(self):
        f=lambda x: x**2
        g=lambda x: sqrt(x)
        self.assertAlmostEqual(eb.prime(f)(1),2,4)
        self.assertAlmostEqual(eb.prime(g)(2),0.5/sqrt(2),4)

    def testSign(self):
        self.assertEqual(eb.sign(5),1)
        self.assertEqual(eb.sign(-5),-1)

    def testMRS(self):
        """Test marginal rate of substitution"""
        u1=lambda x,y: x*y 
        mrs1=eb.MRS(u1)
        self.assertAlmostEqual(mrs1(1,2),2)
        
        uCD1=lambda x,y: (x**0.5)*(y**0.5) # Cobb-Douglas utility
        mrs_uCD1=eb.MRS(uCD1)
        self.assertAlmostEqual(mrs_uCD1(1,2),2,3)
        self.assertAlmostEqual(mrs_uCD1(1,1),1,3)
        
        uCD2=lambda x,y: x**(1/3.0)*y**(2/3.0) # Cobb-Douglas utility
        mrs_uCD2=eb.MRS(uCD2)
        self.assertAlmostEqual(mrs_uCD2(1,2),1,3)
        self.assertAlmostEqual(mrs_uCD2(1,1),0.5,3)

    def testEB(self):
        """Test Cobb-Douglas utility"""
        EB=eb.EdgeBox(u1=lambda x,y: x**0.6*y**0.4,u2=lambda x,y: x**0.1*y**0.9,IE1=[10,20],IE2=[20,10])
        self.assertAlmostEqual(EB.EQ1[0],26.31,2)
        self.assertAlmostEqual(EB.EQ1[1],10.36,2)

    def testLogEB(self):
        """Test log utility"""
        from math import log
        u = lambda x,y: x*y
        EB = eb.EdgeBox(u1 = u, u2 = u, IE1=[10,20], IE2=[20,10])
        logEB = eb.EdgeBox(u1 = lambda x,y: log(u(x,y)), u2 = lambda x,y: log(u(x,y)), IE1=[10,20], IE2=[20,10])
        self.assertAlmostEqual(EB.EQ1[0], 15, 2)
        self.assertAlmostEqual(EB.EQ1[1], 15, 2)
        self.assertAlmostEqual(logEB.EQ1[0], 15, 2)
        self.assertAlmostEqual(logEB.EQ1[1], 15, 2)

    def testFlip(self):
        """Test the reverse of participants"""
        EB=eb.EdgeBox(u1=lambda x,y: x**0.6*y**0.4,u2=lambda x,y: x**0.1*y**0.9,IE1=[10,20],IE2=[20,10])
        EB_rev=eb.EdgeBox(u2=lambda x,y: x**0.6*y**0.4,u1=lambda x,y: x**0.1*y**0.9,IE2=[10,20],IE1=[20,10])
        self.assertAlmostEqual(EB.EQ2[0], 30 - 26.31, 2)
        self.assertAlmostEqual(EB.EQ2[1], 30 - 10.36, 2)

    def testUIE(self):
        """Test the utility of initial endowment"""
        EB=eb.EdgeBox(u1=lambda x,y: x**0.6*y**0.4,u2=lambda x,y: x**0.1*y**0.9,IE1=[4,10],IE2=[6,10])
        EB_rev=eb.EdgeBox(u2=lambda x,y: x**0.6*y**0.4,u1=lambda x,y: x**0.1*y**0.9,IE2=[4,10],IE1=[6,10])
        self.assertAlmostEqual(EB.UIE1, 5.770799623628854)
        self.assertAlmostEqual(EB_rev.UIE2, 5.770799623628854)
        
        

def main():
    unittest.main()

if __name__=='__main__':
    main()
