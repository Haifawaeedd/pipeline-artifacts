"""
Generate both figures for the pipeline paper.
Figure 1: Action distribution across 4 protocols x 2 models (stacked bar).
Figure 2: Calibration gap (actual - declared) across A1, A2, B.
           Sign: actual_error_rate - declared_prob  (positive = overconfident).
           A0 omitted: declared error_prob not reliably captured under truncation.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── colour palette ────────────────────────────────────────────────────────────
C_COMMIT  = '#2166ac'   # blue
C_ABSTAIN = '#f4a582'   # orange
C_SEEK    = '#d6604d'   # red

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — Action distribution across protocols
# Verified from confusion matrices in notebook outputs.
# A0: GPT commit=82.2%, abstain=17.8%, seek=0.0%
#     Llama commit=91.4%, abstain=8.6%, seek=0.0%
# A1: GPT commit=65.1%, abstain=34.7%, seek=0.2%
#     Llama commit=78.2%, abstain=0.7%, seek=21.1%
# A2: GPT commit=94.0%, abstain=6.0%, seek=0.0%
#     Llama commit=88.3%, abstain=2.0%, seek=9.7%
# B:  GPT commit=88.3%, abstain=9.7%, seek=2.0%
#     Llama commit=70.7%, abstain=0.0%, seek=29.3%
# ─────────────────────────────────────────────────────────────────────────────

data = {
    'GPT\nA0':   (82.2, 17.8,  0.0),
    'GPT\nA1':   (65.1, 34.7,  0.2),
    'GPT\nA2':   (94.0,  6.0,  0.0),
    'GPT\nB':    (88.3,  9.7,  2.0),
    'Llama\nA0': (91.4,  8.6,  0.0),
    'Llama\nA1': (78.2,  0.7, 21.1),
    'Llama\nA2': (88.3,  2.0,  9.7),
    'Llama\nB':  (70.7,  0.0, 29.3),
}

labels  = list(data.keys())
commit  = [v[0] for v in data.values()]
abstain = [v[1] for v in data.values()]
seek    = [v[2] for v in data.values()]

x = np.arange(len(labels))
width = 0.55

fig, ax = plt.subplots(figsize=(10, 4.5))

b1 = ax.bar(x, commit,  width, label='COMMIT',        color=C_COMMIT,  alpha=0.88)
b2 = ax.bar(x, abstain, width, bottom=commit,          label='ABSTAIN',  color=C_ABSTAIN, alpha=0.88)
b3 = ax.bar(x, seek,    width,
            bottom=[c + a for c, a in zip(commit, abstain)],
            label='SEEK_EVIDENCE', color=C_SEEK, alpha=0.88)

for bar, pct in zip(b1, commit):
    if pct >= 5:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                f'{pct:.0f}%', ha='center', va='center',
                fontsize=7.5, color='white', fontweight='bold')

for bar, base, pct in zip(b2, commit, abstain):
    if pct >= 5:
        ax.text(bar.get_x() + bar.get_width()/2, base + pct/2,
                f'{pct:.0f}%', ha='center', va='center',
                fontsize=7.5, color='#333333', fontweight='bold')

for bar, base_c, base_a, pct in zip(b3, commit, abstain, seek):
    if pct >= 5:
        ax.text(bar.get_x() + bar.get_width()/2, base_c + base_a + pct/2,
                f'{pct:.0f}%', ha='center', va='center',
                fontsize=7.5, color='white', fontweight='bold')

ax.axvline(x=3.5, color='#888888', linewidth=0.8, linestyle='--')
ax.text(1.5, 105, 'GPT-4.1-mini',   ha='center', fontsize=9, color='#333333', style='italic')
ax.text(5.5, 105, 'Llama-3.3-70b',  ha='center', fontsize=9, color='#333333', style='italic')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylim(0, 112)
ax.set_ylabel('Percentage of responses (%)', fontsize=9)
ax.set_title('Action Distribution Across Protocols and Models', fontsize=10, pad=8)
ax.legend(loc='upper right', fontsize=8, framealpha=0.85)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/ubuntu/pipeline_paper/fig1_action_distribution.png', bbox_inches='tight', dpi=150)
plt.close()
print("Figure 1 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — Calibration gap: actual - declared  (positive = overconfident)
# A0 omitted: declared error_prob not reliably captured under max_tokens=80.
# ─────────────────────────────────────────────────────────────────────────────

cond_labels   = ['A1\n(tokens)', 'A2\n(full evid.)', 'B\n(no table)']
gpt_declared  = [0.235, 0.146, 0.146]
gpt_actual    = [0.488, 0.410, 0.400]
llama_declared = [0.301, 0.205, 0.205]
llama_actual   = [0.369, 0.433, 0.423]

x = np.arange(len(cond_labels))
width = 0.18

fig, ax = plt.subplots(figsize=(9, 4.5))

ax.bar(x - 1.5*width, gpt_declared,   width, label='GPT declared',   color='#2166ac', alpha=0.85)
ax.bar(x - 0.5*width, gpt_actual,     width, label='GPT actual',     color='#2166ac', alpha=0.40, hatch='//')
ax.bar(x + 0.5*width, llama_declared, width, label='Llama declared', color='#d6604d', alpha=0.85)
ax.bar(x + 1.5*width, llama_actual,   width, label='Llama actual',   color='#d6604d', alpha=0.40, hatch='//')

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
ax.set_xticklabels(cond_labels, fontsize=9)
ax.set_ylim(0, 0.65)
ax.set_ylabel('Error probability', fontsize=9)
ax.set_title('Calibration Gap: Actual Error Rate \u2212 Declared Probability\n(A0 omitted; declared values unreliable under truncation)',
             fontsize=10, pad=8)
ax.legend(loc='upper right', fontsize=8, framealpha=0.85)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/ubuntu/pipeline_paper/fig2_calibration_gap.png', bbox_inches='tight', dpi=150)
plt.close()
print("Figure 2 saved.")
print("Done.")
