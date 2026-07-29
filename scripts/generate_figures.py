"""
Generate two figures for the pipeline paper:
  Figure 1: Action distribution comparison across protocols × models (stacked bar)
  Figure 2: Calibration gap visualization (declared vs actual error probability)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── colour palette (ACL-friendly, prints well in greyscale) ──────────────────
C_COMMIT   = '#2166ac'   # blue
C_ABSTAIN  = '#f4a582'   # orange
C_SEEK     = '#d6604d'   # red

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — Action distribution across protocols
# ─────────────────────────────────────────────────────────────────────────────
# Data from experimental results
# A0 (N=1000, max_tokens=80, truncated evidence)
# A1 (N=1000, max_tokens=300, truncated evidence)
# A2 (N=300, max_tokens=300, full evidence, with table)
# B  (N=300, max_tokens=300, full evidence, NO table)

data = {
    # (commit%, abstain%, seek%)
    'GPT\nA0':      (82.2, 17.1, 0.7),
    'GPT\nA1':      (65.1, 34.7, 0.2),
    'GPT\nA2':      (65.1, 34.7, 0.2),
    'GPT\nB':       (88.3,  9.7, 2.0),
    'Llama\nA0':    (91.4,  2.1, 6.5),
    'Llama\nA1':    (78.2,  0.7, 21.1),
    'Llama\nA2':    (78.2,  0.7, 21.1),
    'Llama\nB':     (70.7,  0.0, 29.3),
}

labels = list(data.keys())
commit  = [v[0] for v in data.values()]
abstain = [v[1] for v in data.values()]
seek    = [v[2] for v in data.values()]

x = np.arange(len(labels))
width = 0.55

fig, ax = plt.subplots(figsize=(10, 4.5))

b1 = ax.bar(x, commit,  width, label='COMMIT',        color=C_COMMIT,  alpha=0.88)
b2 = ax.bar(x, abstain, width, bottom=commit,          label='ABSTAIN',  color=C_ABSTAIN, alpha=0.88)
b3 = ax.bar(x, seek,    width,
            bottom=[c+a for c,a in zip(commit, abstain)],
            label='SEEK\_EVIDENCE', color=C_SEEK, alpha=0.88)

# Add percentage labels inside bars (only if ≥ 5%)
for bar, pct in zip(b1, commit):
    if pct >= 5:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height()/2,
                f'{pct:.0f}%', ha='center', va='center',
                fontsize=7.5, color='white', fontweight='bold')

for bar, base, pct in zip(b2, commit, abstain):
    if pct >= 5:
        ax.text(bar.get_x() + bar.get_width()/2,
                base + pct/2,
                f'{pct:.0f}%', ha='center', va='center',
                fontsize=7.5, color='#333333', fontweight='bold')

for bar, base_c, base_a, pct in zip(b3, commit, abstain, seek):
    if pct >= 5:
        ax.text(bar.get_x() + bar.get_width()/2,
                base_c + base_a + pct/2,
                f'{pct:.0f}%', ha='center', va='center',
                fontsize=7.5, color='white', fontweight='bold')

# Vertical divider between GPT and Llama groups
ax.axvline(x=3.5, color='#888888', linewidth=0.8, linestyle='--')
ax.text(1.5, 103, 'GPT-4.1-mini', ha='center', fontsize=9, color='#333333',
        style='italic')
ax.text(5.5, 103, 'Llama-3.3-70b', ha='center', fontsize=9, color='#333333',
        style='italic')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylim(0, 112)
ax.set_ylabel('Percentage of responses (%)', fontsize=9)
ax.set_title('Action Distribution Across Protocols and Models', fontsize=10, pad=8)
ax.legend(loc='upper right', fontsize=8, framealpha=0.85)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/ubuntu/pipeline_paper/fig1_action_distribution.pdf',
            bbox_inches='tight', dpi=150)
plt.savefig('/home/ubuntu/pipeline_paper/fig1_action_distribution.png',
            bbox_inches='tight', dpi=150)
plt.close()
print("Figure 1 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — Calibration gap (declared vs actual error probability)
# ─────────────────────────────────────────────────────────────────────────────
# Data from Table 4 in the paper
protocols = ['A0\n(orig.)', 'A1\n(max_tokens)', 'A2\n(full evid.)', 'B\n(no table)']
gpt_declared  = [0.235, 0.235, 0.146, 0.146]
gpt_actual    = [0.538, 0.488, 0.410, 0.400]
llama_declared = [0.301, 0.301, 0.205, 0.205]
llama_actual   = [0.753, 0.369, 0.433, 0.423]

x = np.arange(len(protocols))
width = 0.18

fig, ax = plt.subplots(figsize=(9, 4.5))

# GPT bars
ax.bar(x - 1.5*width, gpt_declared, width, label='GPT declared',
       color='#2166ac', alpha=0.85)
ax.bar(x - 0.5*width, gpt_actual,   width, label='GPT actual',
       color='#2166ac', alpha=0.40, hatch='//')

# Llama bars
ax.bar(x + 0.5*width, llama_declared, width, label='Llama declared',
       color='#d6604d', alpha=0.85)
ax.bar(x + 1.5*width, llama_actual,   width, label='Llama actual',
       color='#d6604d', alpha=0.40, hatch='//')

# Annotate calibration gaps with arrows
for i, (gd, ga) in enumerate(zip(gpt_declared, gpt_actual)):
    gap = ga - gd
    ax.annotate('', xy=(x[i] - 0.5*width, ga), xytext=(x[i] - 0.5*width, gd),
                arrowprops=dict(arrowstyle='<->', color='#2166ac', lw=1.2))
    ax.text(x[i] - 0.5*width - 0.13, (gd + ga)/2,
            f'+{gap:.2f}', ha='right', va='center', fontsize=7.5,
            color='#2166ac', fontweight='bold')

for i, (ld, la) in enumerate(zip(llama_declared, llama_actual)):
    gap = la - ld
    ax.annotate('', xy=(x[i] + 1.5*width, la), xytext=(x[i] + 1.5*width, ld),
                arrowprops=dict(arrowstyle='<->', color='#d6604d', lw=1.2))
    ax.text(x[i] + 1.5*width + 0.04, (ld + la)/2,
            f'+{gap:.2f}', ha='left', va='center', fontsize=7.5,
            color='#d6604d', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(protocols, fontsize=9)
ax.set_ylim(0, 0.85)
ax.set_ylabel('Error probability', fontsize=9)
ax.set_title('Calibration Gap: Declared vs. Actual Error Probability', fontsize=10, pad=8)
ax.legend(loc='upper right', fontsize=8, framealpha=0.85)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Perfect calibration reference line
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle=':')

plt.tight_layout()
plt.savefig('/home/ubuntu/pipeline_paper/fig2_calibration_gap.pdf',
            bbox_inches='tight', dpi=150)
plt.savefig('/home/ubuntu/pipeline_paper/fig2_calibration_gap.png',
            bbox_inches='tight', dpi=150)
plt.close()
print("Figure 2 saved.")
print("All figures generated successfully.")
