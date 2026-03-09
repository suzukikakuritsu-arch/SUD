import numpy as np

class SUDv35:
    def __init__(self, e=0.43, tau=0.50, eta=0.07, delay=1000, dt=0.02, R0=1.618):
        self.phi = (1 + np.sqrt(5)) / 2
        self.e, self.tau, self.eta = e, tau, eta
        self.delay, self.dt, self.R0 = delay, dt, R0

    def dynamics(self, R, R_delay):
        force = (self.e * (self.phi - R) + 
                 self.tau * (R_delay - R) + 
                 self.eta * np.sin(np.pi * R))
        return R + self.dt * force

    def run_analysis(self, steps=30000, burn_in=5000):
        delta0 = 1e-8
        R1, R2 = self.R0, self.R0 + delta0
        h1, h2 = [R1], [R2]
        inst_lambdas = []
        
        for i in range(steps + burn_in):
            d1 = h1[-self.delay] if len(h1) > self.delay else R1
            d2 = h2[-self.delay] if len(h2) > self.delay else R2
            
            R1_next = self.dynamics(R1, d1)
            R2_next = self.dynamics(R2, d2)
            
            if i >= burn_in:
                dist = abs(R2_next - R1_next)
                if dist < 1e-18: dist = delta0
                
                # Lyapunov exponent normalized by dt
                gamma = np.log(dist / delta0) / self.dt
                inst_lambdas.append(gamma)
                
                # Benettin renormalization
                R2_next = R1_next + delta0 * (R2_next - R1_next) / dist
            
            R1, R2 = R1_next, R2_next
            h1.append(R1)
            h2.append(R2)
            
        return np.array(inst_lambdas)

# Execution
model = SUDv35()
data = model.run_analysis()

mean_lambda = np.mean(data)
peak_lambda = np.percentile(data, 99.9)

print(f"Mean Lyapunov Exponent: {mean_lambda:.4f}")
print(f"Peak Lyapunov Exponent: {peak_lambda:.4f}")
