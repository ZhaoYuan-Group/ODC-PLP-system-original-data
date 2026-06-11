import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ======================
# 1. 全局样式设置
# ======================
# 全局字体设置（多备选方案）
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

# 定义颜色列表
colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#9467bd']

# 定义文件名范围
start_num = 12
end_num = 36

data_list = []
time_ns_list = []
rmsd_list = []
file_names = []
file_count = 0

# 循环处理文件，每五个文件绘制一个图形
for i in range(start_num, end_num + 1):
    for j in range(6):
        filename = f'{i}-{j}.dat'
        try:
            data = np.loadtxt(filename, comments=['#', '%'])
            time_ns = data[:, 0] / 125  # 帧数转ns
            rmsd = data[:, 1]  # RMSD值

            data_list.append(data)
            time_ns_list.append(time_ns)
            rmsd_list.append(rmsd)
            # 去除.dat后缀并将 - 替换为 .，同时添加单位 Å
            label_name = filename.replace('.dat', '').replace('-', '.') + ' Å'
            file_names.append(label_name)
            file_count += 1

            if file_count % 5 == 0:
                # 创建图形
                fig, ax = plt.subplots(figsize=(15, 6))
                fig.set_facecolor('white')  # 设置图形背景色

                # 绘制曲线
                for k in range(len(data_list)):
                    ax.plot(time_ns_list[k], rmsd_list[k],
                            color=colors[k % len(colors)],  # 使用颜色列表中的颜色
                            linewidth=3.0,  # 线宽
                            solid_capstyle='round',  # 线端圆角
                            label=file_names[k])

                # 坐标轴设置
                min_time = min([t.min() for t in time_ns_list])
                max_time = max([t.max() for t in time_ns_list])
                max_rmsd = max([r.max() for r in rmsd_list])

                ax.set_xlim(min_time - 3, max_time + 3)
                ax.set_ylim(0, max_rmsd + 1)
                ax.set_xlabel("Time (ns)", fontsize=18, fontweight='bold', labelpad=8)
                ax.set_ylabel("RMSD (Å)", fontsize=18, fontweight='bold', labelpad=8)

                # 刻度设置
                ax.tick_params(
                    axis='both',
                    which='major',
                    labelsize=18,
                    width=1.5,  # 刻度线宽度
                    length=5  # 刻度线长度
                )
                # 单独设置刻度标签加粗
                for label in ax.get_xticklabels() + ax.get_yticklabels():
                    label.set_fontweight('bold')

                # 图例设置（无边框+内部右上角）
                legend = ax.legend(
                    fontsize=14,
                    frameon=False,  # 关闭边框
                    loc='upper right',  # 图形内部右上角
                    bbox_to_anchor=(0.98, 0.98),  # 微调位置（靠近右上角）
                    handletextpad=0.5,  # 图例句柄与文本间距
                    borderaxespad=0.5  # 图例与边框间距
                )
                # 手动设置图例字体加粗
                for text in legend.get_texts():
                    text.set_fontweight('bold')

                # 边框设置
                for spine in ax.spines.values():
                    spine.set_linewidth(3.0)  # 统一设置所有边框为2.0磅

                # 网格设置
                ax.grid(
                    True,
                    linestyle=':',  # 虚线
                    linewidth=0.8,  # 线宽
                    alpha=0.4,  # 透明度
                    color='gray'  # 网格颜色
                )

                # 布局调整
                plt.subplots_adjust(
                    left=0.1,  # 左边距
                    right=0.85,  # 为图例留出空间
                    bottom=0.12,
                    top=0.95
                )

                # 输出
                output_filename = f'rmsd_comparison_{i}-{j}.png'
                plt.savefig(
                    output_filename,
                    dpi=300,
                    bbox_inches='tight',
                    facecolor='white'
                )
                plt.show()

                # 清空列表以处理下一组五个文件
                data_list = []
                time_ns_list = []
                rmsd_list = []
                file_names = []

        except FileNotFoundError:
            print(f"File {filename} not found. Skipping...")

# 处理剩余不足五个文件的情况
if data_list:
    # 创建图形
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.set_facecolor('white')  # 设置图形背景色

    # 绘制曲线
    for k in range(len(data_list)):
        ax.plot(time_ns_list[k], rmsd_list[k],
                color=colors[k % len(colors)],  # 使用颜色列表中的颜色
                linewidth=3.0,  # 线宽
                solid_capstyle='round',  # 线端圆角
                label=file_names[k])

    # 坐标轴设置
    min_time = min([t.min() for t in time_ns_list])
    max_time = max([t.max() for t in time_ns_list])
    max_rmsd = max([r.max() for r in rmsd_list])

    ax.set_xlim(min_time - 3, max_time + 3)
    ax.set_ylim(0, max_rmsd + 1)
    ax.set_xlabel("Time (ns)", fontsize=18, fontweight='bold', labelpad=8)
    ax.set_ylabel("RMSD (Å)", fontsize=18, fontweight='bold', labelpad=8)

    # 刻度设置
    ax.tick_params(
        axis='both',
        which='major',
        labelsize=18,
        width=1.5,  # 刻度线宽度
        length=5  # 刻度线长度
    )
    # 单独设置刻度标签加粗
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')

    # 图例设置（无边框+内部右上角）
    legend = ax.legend(
        fontsize=14,
        frameon=False,  # 关闭边框
        loc='upper right',  # 图形内部右上角
        bbox_to_anchor=(0.98, 0.98),  # 微调位置（靠近右上角）
        handletextpad=0.5,  # 图例句柄与文本间距
        borderaxespad=0.5  # 图例与边框间距
    )
    # 手动设置图例字体加粗
    for text in legend.get_texts():
        text.set_fontweight('bold')

    # 边框设置
    for spine in ax.spines.values():
        spine.set_linewidth(3.0)  # 统一设置所有边框为2.0磅

    # 网格设置
    ax.grid(
        True,
        linestyle=':',  # 虚线
        linewidth=0.8,  # 线宽
        alpha=0.4,  # 透明度
        color='gray'  # 网格颜色
    )

    # 布局调整
    plt.subplots_adjust(
        left=0.1,  # 左边距
        right=0.85,  # 为图例留出空间
        bottom=0.12,
        top=0.95
    )

    # 输出
    output_filename = f'rmsd_comparison_remaining.png'
    plt.savefig(
        output_filename,
        dpi=300,
        bbox_inches='tight',
        facecolor='white'
    )
    plt.show()
