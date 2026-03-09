import numpy as np
import matplotlib.pyplot as plt

class SUDv34:
    def __init__(self, e=0.43, tau=0.50, eta=0.07, delay=1000, dt=0.02, R0=1.2):
        self.phi = (1 + np.sqrt(5)) / 2
        self.e, self.tau, self.eta = e, tau, eta
        self.delay, self.dt, self.R0 = delay, dt, R0

    def dynamics(self, R, R_delay):
        # 決定論的力学（Lyapunov計算用）
        force = (self.e * (self.phi - R) 
                 + self.tau * (R_delay - R) 
                 + self.eta * np.sin(np.pi * R))
        return R + self.dt * force

    def run_analysis(self, steps=10000):
        # 1. 軌道シミュレーション
        R = self.R0
        history = [R]
        for i in range(steps):
            d = history[-self.delay] if len(history) > self.delay else R
            R = self.dynamics(R, d)
            history.append(R)
        
        # 2. 厳密リヤプノフ指数（ベネティン法）
        delta0 = 1e-8
        R1, R2 = self.R0, self.R0 + delta0
        h1, h2 = [R1], [R2]
        lam_sum = 0
        
        for i in range(steps):
            d1 = h1[-self.delay] if len(h1) > self.delay else R1
            d2 = h2[-self.delay] if len(h2) > self.delay else R2
            
            R1_next = self.dynamics(R1, d1)
            R2_next = self.dynamics(R2, d2)
            
            dist = abs(R2_next - R1_next)
            if dist == 0: dist = delta0
            
            lam_sum += np.log(dist / delta0)
            
            # 再規格化
            R1, R2 = R1_next, R1_next + delta0 * (R2_next - R1_next) / dist
            h1.append(R1); h2.append(R2)
            
        return np.array(history), lam_sum / (steps * self.dt)

# 解析実行
model = SUDv34()
trajectory, lyapunov_exp = model.run_analysis()

print(f"--- SUD v3.4 Analysis Result ---")
print(f"Lyapunov Exponent (λ): {lyapunov_exp:.6f}")
print(f"Final State (R): {trajectory[-1]:.6f} (Target φ: {model.phi:.6f})")
