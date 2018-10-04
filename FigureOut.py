# -*- coding:utf-8 -*-
import numpy as np, pylab
import scipy.optimize as opt


class Myfigure(object):

    count = 0

    def __init__(self, R2 = 4.89E-3, C2 = 13.2E-3, L2 = 1.5E-9, R1 = 4.89e-3, L1 = 1.5E-9, Name = 'Name', Num = 0):
        self.R1, self.L1 = R1, L1
        self.R2, self.C2, self.L2 = R2, C2, L2
        self.Name = Name
        self.Num = Num
        #Myfigure.count += 1

    def impendenceMin(self, w):
        a = self.R1 + complex(0, self.L1)*w
        b = self.R2 + complex(0, self.L2)*w + 1/(complex(0, self.C2)*w)

        return abs(a*b/(a+b))

    def impendenceMax(self, w):
        a = self.R1 + complex(0, self.L1)*w
        b = self.R2 + complex(0, self.L2)*w + 1/(complex(0, self.C2)*w)

        return -abs(a*b/(a+b))

    def error(self,err=1000):

        a = opt.fminbound(self.impendenceMin, 0.2*min(1/(self.L2*self.C2)**0.5,1/(self.L1*self.C2)**0.5), 1.2*max(1/(self.L2*self.C2)**0.5,1/(self.L1*self.C2)**0.5))
        b = opt.fminbound(self.impendenceMax, 0.2*min(1/(self.L2*self.C2)**0.5,1/(self.L1*self.C2)**0.5), 1.2*max(1/(self.L2*self.C2)**0.5,1/(self.L1*self.C2)**0.5))

        aa = self.impendenceMin(a)
        bb = self.impendenceMin(b)
        now_error1=((abs(aa-self.R1) + abs(bb-self.R1))/self.R1*100)
        if float(now_error1) <= float(err):
          return ((abs(aa-self.R1) + abs(bb-self.R1))/self.R1*100,a,b)
        else:
          return False

    def figure(self,err=1e5):
        now_error, Minb, Maxa = self.error()

        if float(now_error) <= err:
            self.freq = np.linspace(100, 100/np.sqrt(self.C2*self.L2), 1E6)
            a = self.R1 + self.freq*complex("j")*self.L1
            b = self.R2 + self.freq*complex("j")*self.L2 + 1/(self.freq*complex("j")*self.C2)
            self.impedance = abs(a*b/(a+b))

            pylab.plot(self.freq, self.impedance)
            pylab.semilogx(self.freq, self.impedance)
            pylab.xlabel("Freq", color = "red")
            pylab.ylabel("Impedance", color = "red")
            pylab.text(1000, self.impendenceMin(max(Minb,Maxa)),'Combination='+self.Name)
            pylab.text(Minb, self.impendenceMin(Minb),'Min')
            pylab.text(Maxa, self.impendenceMin(Maxa), 'Max')
            pylab.text((Maxa+Minb)/1000, 10*self.impendenceMin(max(Minb,Maxa)), 'wave propagation = %s' %str(abs(self.impendenceMin(Maxa)-self.impendenceMin(Minb))))
            pylab.title("Error: %s%%" % now_error, color = "black")
            pylab.gca().spines['right'].set_color('none')
            pylab.gca().spines['top'].set_color('none')
            #pylab.savefig('figure_test\Nums-%s and Name-(%s).png' % (self.Num, self.Name))
            pylab.show()
            #pylab.clf()
            return float(now_error)
        else:
            return False

    def error2(self,err=1000):
        '''the error : sum(random freq value - standard)'''

        w = np.linspace(0.3*min(1/(self.L2*self.C2)**0.5, 1/(self.L1*self.C2)**0.5), 3*max(1/(self.L2*self.C2)**0.5, 1/(self.L1*self.C2)**0.5),20)

        now_error2 = sum(abs(abs(self.impendenceMin(w)-self.R1))/self.R1*100)/20
        # return  error

        if float(now_error2) <= float(err):
            return sum(abs(abs(self.impendenceMin(w)-self.R1))/self.R1*100)/20
        else:
            return False
    def figure2(self,err=1e5):
        now_error = self.error2()

        if float(now_error) <= err:
            self.freq = np.linspace(100, 100 / np.sqrt(self.C2 * self.L2), 1E6)
            a = self.R1 + self.freq * complex("j") * self.L1
            b = self.R2 + self.freq * complex("j") * self.L2 + 1 / (self.freq * complex("j") * self.C2)
            self.impedance = abs(a * b / (a + b))

            pylab.plot(self.freq, self.impedance)
            pylab.semilogx(self.freq, self.impedance)
            pylab.xlabel("Freq", color="red")
            pylab.ylabel("Impedance", color="red")
            pylab.text(1000, self.impendenceMin(1E7), 'Combination=' + self.Name)
            pylab.title("Error: %s%%" % now_error, color="black")
            pylab.gca().spines['right'].set_color('none')
            pylab.gca().spines['top'].set_color('none')
            #pylab.savefig('figure_test2\Nums-%s and Name-(%s).png' % (self.Num, self.Name))
            pylab.show()
            pylab.clf()
            return float(now_error)
        else:
            return False

# a = Myfigure(R2 = 0.005755, C2 = 5.5E-05, L2 = 1.75E-10, Name='1')
# b = a.figure()
# a = Myfigure().figure()
# b = Myfigure(L2 = 1.5E-9, R1 = 4.89e-3, L1 = 315E-8, Name='2').figure()
# c = Myfigure(L2 = 1.5E-9, R1 = 4.89e-3, L1 = 315E-9, Name='3').figure()
# d = Myfigure(L2 = 1.5E-9, R1 = 4.89e-3, L1 = 315E-8, Name='4').figure()

