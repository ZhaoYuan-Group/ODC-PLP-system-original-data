import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import glob
import re
import matplotlib

# ===================== 全局设置：所有字体统一为 Arial =====================
plt.rcParams['font.family'] = 'Arial'  # 全局字体
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['Arial']  # 无衬线字体强制Arial

# ===================== 颜色 =====================
colors = [
    "#f8f9fa",    # 0 None
    "#b3d9ff",    # 1 Ext
    "#80bfff",    # 2 Bridge
    "#4da6ff",    # 3 3-10
    "#1a8cff",    # 4 Alpha
    "#0066cc",    # 5 Pi
    "#004c99",    # 6 Turn
    "#003366"     # 7 Bend
]
cmap = ListedColormap(colors)
norm = plt.Normalize(0, 7)

# ===================== 读取第一帧（修复版） =====================
def load_first_frame(gnu_file):
    res_list = []
    ss_list = []
    in_data = False
    
    with open(gnu_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if "splot" in line:
                in_data = True
                continue
            if line == "end" or line.startswith("pause"):
                break
            if in_data and line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 3:
                    frame = float(parts[0])
                    if frame == 1.0:
                        try:
                            resid = int(float(parts[1]))
                            ss = int(float(parts[2]))
                            res_list.append(resid)
                            ss_list.append(ss)
                        except:
                            continue

    return np.array(res_list), np.array(ss_list)

# ===================== 自动匹配文件 =====================
files = sorted(glob.glob("[123][0-9]-[05].gnu"))
files = [f for f in files if 13 <= int(f.split('-')[0]) <= 35]

print("正在绘图文件：")
for f in files:
    print(f"✅ {f}")

# ===================== 绘图 =====================
fig, ax = plt.subplots(figsize=(30, 14))

for y_idx, fname in enumerate(files):
    res, ss = load_first_frame(fname)
    
    if len(res) == 0 or len(ss) == 0:
        print(f"⚠️ {fname} 无有效第一帧数据")
        continue

    y = np.full_like(res, y_idx + 1)

    # 热图方块大小（可自行调整：25/35/45）
    ax.scatter(res, y, c=ss, cmap=cmap, norm=norm, s=25, marker='s', edgecolors='none')

# ===================== 全部字体已自动为 Arial =====================
# 总标题
ax.set_title("Secondary Structure (First Frame Only)", fontsize=24, weight='bold')

# X 轴标签
ax.set_xlabel("Residue", fontsize=18, weight='bold')

# Y 轴标签
ax.set_ylabel("System", fontsize=18, weight='bold')

# Y 轴刻度标签
ax.set_yticks(range(1, len(files)+1))
ax.set_yticklabels([f.replace(".gnu","") for f in files], fontsize=14)
ax.set_ylim(0.5, len(files)+0.5)

# X 轴刻度字体（也强制 Arial）
ax.tick_params(axis='x', labelsize=14)

# 色条 + 色条字体
cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.6)
cbar.set_ticks([0,1,2,3,4,5,6,7])
cbar.set_ticklabels(["None","Ext","Bridge","3-10","Alpha","Pi","Turn","Bend"])
cbar.ax.tick_params(labelsize=14)

plt.tight_layout()
plt.savefig("first_frame_clean_Arial.png", dpi=300, bbox_inches='tight')
plt.close()

print("\n🎉 绘图完成：first_frame_clean_Arial.png（全图字体 = Arial）")