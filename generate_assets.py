"""
Generates the chart assets referenced by pages/bundle_size.py and
pages/adoption.py. Run once, before `arklight build`. Not an ARKlight
module -- ARKlight itself never touches matplotlib; it only ever sees
the finished PNGs under assets/.

Ported from main's generate_assets.py for the SoA (Separation of
Areas) branch: the only change is where the two datasets come from --
main's monolithic data.py doesn't exist here, so BUNDLE_SIZE/SO2025
are imported from their real homes, content/bundle_size.py and
content/adoption.py, same values either way (see content/__init__.py:
"frozen, single-source-of-truth data, one module per domain").
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from content.adoption import SO2025
from content.bundle_size import BUNDLE_SIZE

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.edgecolor": "#444",
    "axes.labelcolor": "#222",
    "text.color": "#222",
    "xtick.color": "#444",
    "ytick.color": "#444",
})

COLOR_ARK = "#7c3aed"
COLOR_OTHER = "#94a3b8"

# ---------------------------------------------------------- Bar chart

names = [n for n, *_ in BUNDLE_SIZE]
mids = [(lo + hi) / 2 for _, lo, hi, _ in BUNDLE_SIZE]
colors = [COLOR_ARK if "ARKlight" in n else COLOR_OTHER for n in names]

order = sorted(range(len(names)), key=lambda i: mids[i])
names = [names[i] for i in order]
mids = [mids[i] for i in order]
colors = [colors[i] for i in order]

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=160)
bars = ax.barh(names, mids, color=colors)
for bar, val in zip(bars, mids):
    ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f} KB", va="center", fontsize=9)
ax.set_xlabel("Gzipped JavaScript, minimal app (KB) -- midpoint of sourced range")
ax.set_title("Shipped JavaScript: ARKlight vs. Traditional Frameworks")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("assets/bundle-size-bar.png")
plt.close(fig)

# ---------------------------------------------------------- Pie chart

pie_names = [n for n, *_ in SO2025]
pie_vals = [pop for _, pop, _, _ in SO2025]
total = sum(pie_vals)
pie_pct = [v / total * 100 for v in pie_vals]
pie_colors = ["#61dafb", "#dd0031", "#42b883", "#ff3e00"]  # React/Angular/Vue/Svelte brand-ish tones

fig, ax = plt.subplots(figsize=(6, 6), dpi=160)
wedges, texts, autotexts = ax.pie(
    pie_pct, labels=pie_names, colors=pie_colors, autopct="%1.0f%%",
    startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)
ax.set_title("Relative Share of Current Use\n(React/Vue/Svelte/Angular only, normalized)")
fig.tight_layout()
fig.savefig("assets/adoption-pie.png")
plt.close(fig)

# --------------------------------------------------- Pipeline diagram

stages = [
    "Python\nSource", "Python\nAST", "ARK\nAST", "Normalize", "Validate",
    "Website\nIR", "HTML/CSS/JS\nBackends", "Static\nFiles",
]
fig, ax = plt.subplots(figsize=(11, 2.2), dpi=160)
x = list(range(len(stages)))
for i, label in enumerate(stages):
    ax.add_patch(plt.Rectangle((i - 0.42, 0), 0.84, 1, fill=True,
                                facecolor="#ede9fe" if i < len(stages) - 1 else "#7c3aed",
                                edgecolor="#7c3aed"))
    ax.text(i, 0.5, label, ha="center", va="center", fontsize=8.5,
             color="#222" if i < len(stages) - 1 else "white")
    if i < len(stages) - 1:
        ax.annotate("", xy=(i + 0.58, 0.5), xytext=(i + 0.42, 0.5),
                     arrowprops=dict(arrowstyle="->", color="#7c3aed"))
ax.set_xlim(-0.6, len(stages) - 0.4)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("ARKlight's Compiler Pipeline -- Nothing to the Right of \"Static Files\" Runs in the Browser", fontsize=10)
fig.tight_layout()
fig.savefig("assets/pipeline-diagram.png")
plt.close(fig)

print("Wrote assets/bundle-size-bar.png, assets/adoption-pie.png, assets/pipeline-diagram.png")
