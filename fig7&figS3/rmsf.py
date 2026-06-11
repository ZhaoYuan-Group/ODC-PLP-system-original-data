import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ======================
# 1. 全局样式（和你RMSD脚本完全一致）
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

# 配色（和你原图一样）
colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#9467bd']

# ======================
# 2. 你的数据范围（13-0 → 35-0，共44组）
# ======================
start_num = 13
end_num = 35
sub_fix = 0          # 固定后缀 0
file_suffix = '_rmsf.dat'
GROUP_SIZE = 4       # 每4个文件一张图

# 存储列表
data_list = []
residue_list = []
rmsf_list = []
file_names = []
file_count = 0

# ======================
# 3. 循环读取 + 每4个绘图
# ======================
for i in range(start_num, end_num + 1):
    # 文件名：13-0_rmsf.dat, 14-0_rmsf.dat ... 35-0_rmsf.dat
    filename = f'{i}-{sub_fix}{file_suffix}'
    
    try:
        # 读取 RMSF 数据
        data = np.loadtxt(filename, comments=['#', '%'])
        residues = data[:, 0]   # 第1列：残基编号
        rmsf = data[:, 1]       # 第2列：RMSF值

        data_list.append(data)
        residue_list.append(residues)
        rmsf_list.append(rmsf)
        
        # 图例名称（13.0 Å）
        label_name = f'{i}.{sub_fix} Å'
        file_names.append(label_name)
        file_count += 1

        # ======================
        # 每 4 个文件画一张图
        # ======================
        if file_count % GROUP_SIZE == 0:
            fig, ax = plt.subplots(figsize=(15, 6))
            fig.set_facecolor('white')

            # 绘图
            for k in range(len(data_list)):
                ax.plot(residue_list[k], rmsf_list[k],
                        color=colors[k % len(colors)],
                        linewidth=3.0,
                        solid_capstyle='round',
                        label=file_names[k])

            # 坐标轴范围
            min_res = min([r.min() for r in residue_list])
            max_res = max([r.max() for r in residue_list])
            max_rmsf = max([r.max() for r in rmsf_list])

            ax.set_xlim(min_res - 5, max_res + 5)
            ax.set_ylim(0, max_rmsf + 0.5)
            ax.set_xlabel("Residue Number", fontsize=18, fontweight='bold', labelpad=8)
            ax.set_ylabel("RMSF (Å)", fontsize=18, fontweight='bold', labelpad=8)

            # 刻度
            ax.tick_params(axis='both', which='major', labelsize=18, width=1.5, length=5)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontweight('bold')

            # 图例
            legend = ax.legend(fontsize=14, frameon=False, loc='upper right', bbox_to_anchor=(0.98, 0.98))
            for text in legend.get_texts():
                text.set_fontweight('bold')

            # 边框
            for spine in ax.spines.values():
                spine.set_linewidth(3.0)

            # 网格
            ax.grid(True, linestyle=':', linewidth=0.8, alpha=0.4, color='gray')

            # 布局
            plt.subplots_adjust(left=0.1, right=0.85, bottom=0.12, top=0.95)

            # 输出图片
            start_idx = file_count - GROUP_SIZE + 1
            end_idx = file_count
            output_filename = f'rmsf_group_{start_idx}-{end_idx}.png'
            plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor='white')
            plt.show()

            # 清空
            data_list = []
            residue_list = []
            rmsf_list = []
            file_names = []

    except FileNotFoundError:
        print(f"缺失文件: {filename}，跳过")

# ======================
# 4. 剩余文件绘图
# ======================
if data_list:
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.set_facecolor('white')

    for k in range(len(data_list)):
        ax.plot(residue_list[k], rmsf_list[k],
                color=colors[k % len(colors)],
                linewidth=3.0,
                solid_capstyle='round',
                label=file_names[k])

    min_res = min([r.min() for r in residue_list])
    max_res = max([r.max() for r in residue_list])
    max_rmsf = max([r.max() for r in rmsf_list])

    ax.set_xlim(min_res - 5, max_res + 5)
    ax.set_ylim(0, max_rmsf + 0.5)
    ax.set_xlabel("Residue Number", fontsize=18, fontweight='bold', labelpad=8)
    ax.set_ylabel("RMSF (Å)", fontsize=18, fontweight='bold', labelpad=8)

    ax.tick_params(axis='both', which='major', labelsize=18, width=1.5, length=5)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')

    legend = ax.legend(fontsize=14, frameon=False, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    for text in legend.get_texts():
        text.set_fontweight('bold')

    for spine in ax.spines.values():
        spine.set_linewidth(3.0)

    ax.grid(True, linestyle=':', linewidth=0.8, alpha=0.4, color='gray')
    plt.subplots_adjust(left=0.1, right=0.85, bottom=0.12, top=0.95)

    plt.savefig('rmsf_group_remaining.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

print("✅ 全部 RMSF 图绘制完成！")