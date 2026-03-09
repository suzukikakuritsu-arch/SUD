import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# Golden ratio hierarchy
# ==========================================

phi  = (1 + np.sqrt(5)) / 2
phi2 = phi**2
phi3 = phi**3
phi4 = phi**4

# ==========================================
# SUD map
# ==========================================

def sud_step(R, r, w, f, sigma=0.03):

    noise = np.random.normal(0, sigma)

    dR = (
        w * abs(R - phi) * (phi - R) +
        r * np.sin(np.pi * R) -
        0.8 * (R**2) / phi +
        0.15 * f +
        noise
    )

    dr = 0.2*(phi - R) - 0.1*r
    dw = 0.3*R - 0.05*w
    df = 0.4*(R**2) - 0.2*f

    return dR, dr, dw, df


# ==========================================
# simulation
# ==========================================

steps = 100000
dt = 0.01

R,r,w,f = 1.2,0.5,1.0,0.4

R_series=[]
F_series=[]

for i in range(steps):

    dR,dr,dw,df = sud_step(R,r,w,f)

    R += dR*dt
    r += dr*dt
    w += dw*dt
    f += df*dt

    R_series.append(R)
    F_series.append(f)

R_series=np.array(R_series)

# ==========================================
# Lyapunov calculation
# ==========================================

def lyapunov():

    R1=1.2
    R2=R1+1e-9

    lam=0
    N=40000

    for i in range(N):

        d1,_ ,_,_ = sud_step(R1,0.5,1,0.4,0)
        d2,_ ,_,_ = sud_step(R2,0.5,1,0.4,0)

        R1 += d1*dt
        R2 += d2*dt

        dist=abs(R2-R1)

        lam += np.log(dist/1e-9)

        R2 = R1 + 1e-9

    return lam/N

lam = lyapunov()

print("Lyapunov exponent =",lam)

# ==========================================
# bifurcation diagram
# ==========================================

param=np.linspace(0.1,1.5,600)

bx=[]
by=[]

for e in param:

    R=1.2

    for i in range(2000):

        dR = abs(R-phi)*(phi-R) - e*(R**2)/phi

        R += dR*0.02

        if i>1500:
            bx.append(e)
            by.append(R)

# ==========================================
# plots
# ==========================================

plt.figure(figsize=(16,10))

# time series
plt.subplot(2,2,1)
plt.plot(R_series,lw=0.6)
plt.axhline(phi,color="orange")
plt.axhline(phi2,color="red")
plt.axhline(phi3,color="purple")
plt.title("SUD time series")

# histogram
plt.subplot(2,2,2)
plt.hist(R_series,bins=150)
plt.axvline(phi)
plt.axvline(phi2)
plt.axvline(phi3)
plt.title("state density")

# phase space
plt.subplot(2,2,3)
plt.plot(R_series,F_series,lw=0.3)
plt.title("phase attractor (R,f)")

# bifurcation
plt.subplot(2,2,4)
plt.plot(bx,by,'.',markersize=0.3)
plt.title("bifurcation diagram")

plt.tight_layout()
plt.show()
