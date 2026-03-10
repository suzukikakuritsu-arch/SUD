# generate_video.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from sud62_module import SUD6_2_Verified

# SUD6.2シミュレーション
sud62 = SUD6_2_Verified(n_dim=200)
history, final_os = sud62.run_verified_simulation(steps=150)

# アニメーション準備
fig, ax = plt.subplots(figsize=(10,6))
line, = ax.plot([], [], lw=4, color='green', label='<R(t)>')
ax.axhline(sud62.phi, color='gold', lw=3, ls='--', label='φ=1.618')
ax.set_xlim(0, len(history))
ax.set_ylim(0.5, 2.0)
ax.set_title("SUD6.2 φ収束アニメーション")
ax.set_xlabel("Time step")
ax.set_ylabel("<R(t)>")
ax.grid(True)
ax.legend()

mean_r = np.mean(history, axis=1)

def init():
    line.set_data([], [])
    return (line,)

def update(frame):
    line.set_data(np.arange(frame), mean_r[:frame])
    return (line,)

anim = FuncAnimation(fig, update, frames=len(mean_r), init_func=init, blit=True, interval=50)

# iPhoneでも簡単にGIF出力
anim.save("sud62_phi_convergence.gif", writer=PillowWriter(fps=20))
print("🎬 GIF生成完了: sud62_phi_convergence.gif")
