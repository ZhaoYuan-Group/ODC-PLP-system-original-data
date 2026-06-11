import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# ======================
# 1. 全局样式设置（沿用RMSD脚本的科研风格）
# ======================
font_options = [
    'Times New Roman',
    'Times',
    'Liberation Serif',
    'DejaVu Serif',
    'serif'
]
rcParams['font.family'] = font_options
rcParams['mathtext.fontset'] = 'stix'
rcParams['font.weight'] = 'bold'

# 科研配色（匹配截图中的颜色：绿、蓝、橙、红紫）
colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#9467bd']
linewidth = 3.0

# ======================
# 2. 数据参数配置（仅提取 13-0,19-0,21-0,25-0,31-0）
# ======================
# 固定需要提取的 主数字-子数字 组合
TARGET_GROUPS = [(13, 0), (19, 0), (21, 0), (25, 0), (31, 0)]

file_suffix = '_rmsf.dat'
residue_col = 0       # 残基编号列
rmsf_col = 1          # RMSF值列

# 固定纵坐标最大值（仅修改这里）
Y_MAX_FIXED = 6.0

# 初始化数据存储
data_list = []
residue_list = []
rmsf_list = []
file_names = []

# ======================
# 3. 仅读取指定的5个文件
# ======================
for main_num, sub_num in TARGET_GROUPS:
    filename = f"{main_num}-{sub_num}{file_suffix}"
    if os.path.exists(filename):
        # 读取数据
        data = np.loadtxt(filename, comments=['#', '%'])
        residues = data[:, residue_col]
        rmsf_vals = data[:, rmsf_col]
        
        data_list.append(data)
        residue_list.append(residues)
        rmsf_list.append(rmsf_vals)
        file_names.append(f'{main_num}.{sub_num} Å')

# ======================
# 4. 绘制一张图（包含5条曲线）
# ======================
if data_list:
    # 创建超宽画布（20英寸宽，避免曲线拥挤）
    fig, ax = plt.subplots(figsize=(20, 6))
    fig.set_facecolor('white')

    # 绘制5条曲线
    for k in range(len(data_list)):
        ax.plot(
            residue_list[k], rmsf_list[k],
            color=colors[k % len(colors)],
            linewidth=linewidth,
            solid_capstyle='round',
            label=file_names[k]
        )

    # 坐标轴范围设置（仅固定纵轴，横轴保持自动计算）
    min_res = min([r.min() for r in residue_list])
    max_res = max([r.max() for r in residue_list])
    ax.set_xlim(min_res - 10, max_res + 10)
    ax.set_ylim(0, Y_MAX_FIXED)  # 固定纵轴到6.0

    # 坐标轴标签（加大字号）
    ax.set_xlabel("Residue Number", fontsize=20, fontweight='bold', labelpad=12)
    ax.set_ylabel("RMSF (Å)", fontsize=20, fontweight='bold', labelpad=12)

    # 刻度设置
    ax.tick_params(
        axis='both',
        which='major',
        labelsize=18,
        width=1.5,
        length=6,
        pad=8
    )
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')

    # ====================== 统一注释样式（所有图完全一致） ======================
    annot_y_start = 0.95
    annot_y_step = 0.08
    annot_fontsize = 14
    for idx, name in enumerate(file_names):
        annot_text = f'● {name}'
        ax.text(0.98, annot_y_start - idx * annot_y_step, annot_text,
                transform=ax.transAxes, fontsize=annot_fontsize, fontweight='bold',
                color=colors[idx % len(colors)], ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8,
                          edgecolor='gray', linewidth=1))
    # ============================================================================

    # 边框设置
    for spine in ax.spines.values():
        spine.set_linewidth(3.0)

    # 网格设置
    ax.grid(
        True,
        linestyle=':',
        linewidth=0.8,
        alpha=0.4,
        color='gray'
    )

    # 调整布局（为右侧注释留出空间）
    plt.subplots_adjust(
        left=0.05,
        right=0.92,
        bottom=0.12,
        top=0.95
    )

    # 保存最终图片
    output_filename = f'rmsf_selected_groups.png'
    plt.savefig(
        output_filename,
        dpi=300,
        bbox_inches='tight',
        facecolor='white'
    )
    plt.close(fig)

print("✅ 5组指定片段 RMSF 图绘制完成！")