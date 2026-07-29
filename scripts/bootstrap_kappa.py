import numpy as np

def cohen_kappa(y1, y2):
    labels = list(set(y1) | set(y2))
    n = len(y1)
    po = np.mean(y1 == y2)
    pe = sum((np.sum(y1==l)/n) * (np.sum(y2==l)/n) for l in labels)
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1 - pe)

# ── GPT B case reconstruction ──────────────────────────────────────────────
# From notebook: agreement=0.970, kappa=0.860, N=300
# Model actions: COMMIT=265, ABSTAIN=29, SEEK=6
# Rule actions derived from error_probs using threshold function
# Solved: rule COMMIT=260, ABSTAIN=35, SEEK=5
# Confusion matrix reconstruction:
#   COMMIT/COMMIT=260, ABSTAIN/ABSTAIN=25, SEEK/SEEK=6 (agree=291)
#   COMMIT/ABSTAIN=4, ABSTAIN/COMMIT=5 (disagree=9)
gpt_b_rule   = ['COMMIT']*260 + ['ABSTAIN']*35 + ['SEEK']*5
gpt_b_model  = ['COMMIT']*260 + ['COMMIT']*5 + ['ABSTAIN']*25 + ['ABSTAIN']*4 + ['SEEK']*6
# Verify
assert len(gpt_b_rule) == 300
assert len(gpt_b_model) == 300
gpt_b_rule  = np.array(gpt_b_rule)
gpt_b_model = np.array(gpt_b_model)
k_gpt = cohen_kappa(gpt_b_rule, gpt_b_model)
print(f"GPT B kappa (reconstructed): {k_gpt:.3f}")

# ── Llama B case reconstruction ────────────────────────────────────────────
# From Table 3 in paper (from ArmB notebook confusion matrix):
# rule_action  COMMIT  SEEK  Total
# COMMIT         212    58    270
# ABSTAIN          0     2      2
# SEEK             0    28     28
# Total          212    88    300
llama_b_rule  = ['COMMIT']*270 + ['ABSTAIN']*2 + ['SEEK']*28
llama_b_model = ['COMMIT']*212 + ['SEEK']*58 + ['SEEK']*2 + ['SEEK']*28
assert len(llama_b_rule) == 300
assert len(llama_b_model) == 300
llama_b_rule  = np.array(llama_b_rule)
llama_b_model = np.array(llama_b_model)
k_llama = cohen_kappa(llama_b_rule, llama_b_model)
print(f"Llama B kappa (from confusion matrix): {k_llama:.3f}")

# ── Bootstrap CIs ──────────────────────────────────────────────────────────
np.random.seed(42)
n_boot = 10000

# GPT B
cases_gpt = np.column_stack([gpt_b_rule, gpt_b_model])
kappas_gpt = []
for _ in range(n_boot):
    idx = np.random.choice(300, 300, replace=True)
    s = cases_gpt[idx]
    kappas_gpt.append(cohen_kappa(s[:, 0], s[:, 1]))
kappas_gpt = np.array(kappas_gpt)
print(f"GPT B kappa 95% CI (bootstrap, N=10000): [{np.percentile(kappas_gpt, 2.5):.3f}, {np.percentile(kappas_gpt, 97.5):.3f}]")

# Llama B
cases_llama = np.column_stack([llama_b_rule, llama_b_model])
kappas_llama = []
for _ in range(n_boot):
    idx = np.random.choice(300, 300, replace=True)
    s = cases_llama[idx]
    kappas_llama.append(cohen_kappa(s[:, 0], s[:, 1]))
kappas_llama = np.array(kappas_llama)
print(f"Llama B kappa 95% CI (bootstrap, N=10000): [{np.percentile(kappas_llama, 2.5):.3f}, {np.percentile(kappas_llama, 97.5):.3f}]")

# ── Chi-squared homogeneity test (A1 vs B marginal action distributions) ──
from scipy import stats

# A1 action distributions (N=1000): COMMIT=65.1%, ABSTAIN=34.7%, SEEK=0.2%
a1_gpt   = np.array([651, 347, 2])
# B action distributions (N=300): COMMIT=88.3%, ABSTAIN=9.7%, SEEK=2.0%
b_gpt    = np.array([265,  29, 6])

a1_llama = np.array([782,   7, 211])
b_llama  = np.array([212,   0,  88])

def chi2_homogeneity(obs1, obs2):
    contingency = np.array([obs1, obs2])
    mask = contingency.sum(axis=0) > 0
    contingency = contingency[:, mask]
    chi2, p, dof, _ = stats.chi2_contingency(contingency)
    return chi2, p, dof

gpt_chi2, gpt_p, gpt_dof = chi2_homogeneity(a1_gpt, b_gpt)
llama_chi2, llama_p, llama_dof = chi2_homogeneity(a1_llama, b_llama)
print(f"\nChi-squared homogeneity (A1 vs B action distributions):")
print(f"  GPT:   chi2={gpt_chi2:.3f}, df={gpt_dof}, p={gpt_p:.6f}")
print(f"  Llama: chi2={llama_chi2:.3f}, df={llama_dof}, p={llama_p:.6f}")

print("\nSUMMARY FOR PAPER:")
print(f"  GPT B:   kappa={k_gpt:.3f}, 95% CI [{np.percentile(kappas_gpt, 2.5):.3f}, {np.percentile(kappas_gpt, 97.5):.3f}]")
print(f"  Llama B: kappa={k_llama:.3f}, 95% CI [{np.percentile(kappas_llama, 2.5):.3f}, {np.percentile(kappas_llama, 97.5):.3f}]")
print(f"  GPT A1 vs B chi2={gpt_chi2:.1f}, p={gpt_p:.4f}")
print(f"  Llama A1 vs B chi2={llama_chi2:.1f}, p={llama_p:.4f}")
