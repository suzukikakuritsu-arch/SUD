import numpy as np
import matplotlib.pyplot as plt

class SUDv34:

    def __init__(self,e=0.43,tau=0.50,eta=0.07,delay=1000,dt=0.02,R0=1.2):

        self.phi=(1+np.sqrt(5))/2

        self.e=e
        self.tau=tau
        self.eta=eta

        self.delay=delay
        self.dt=dt

        self.R0=R0

    def dynamics(self,R,R_delay):

        force=(
            self.e*(self.phi-R)
            +self.tau*(R_delay-R)
            +self.eta*np.sin(np.pi*R)
        )

        return R+self.dt*force


    def simulate(self,steps=8000,burn=2000):

        R=self.R0
        history=[R]

        for i in range(steps+burn):

            if len(history)>self.delay:
                R_delay=history[-self.delay]
            else:
                R_delay=R

            R=self.dynamics(R,R_delay)

            history.append(R)

        return np.array(history[burn:])


    def lyapunov(self,steps=10000):

        delta0=1e-8

        R1=self.R0
        R2=self.R0+delta0

        h1=[R1]
        h2=[R2]

        lam=0

        for i in range(steps):

            d1=h1[-self.delay] if len(h1)>self.delay else R1
            d2=h2[-self.delay] if len(h2)>self.delay else R2

            R1=self.dynamics(R1,d1)
            R2=self.dynamics(R2,d2)

            dist=abs(R2-R1)

            if dist==0:
                dist=delta0

            lam+=np.log(dist/delta0)

            # renormalize
            R2=R1+delta0*(R2-R1)/dist

            h1.append(R1)
            h2.append(R2)

        return lam/steps


    def fixed_point_stability(self):

        derivative=1+self.dt*(
            -(self.e+self.tau)
            +self.eta*np.pi*np.cos(np.pi*self.phi)
        )

        return abs(derivative)<1,derivative
