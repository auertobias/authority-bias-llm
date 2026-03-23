# =============================================================
# 01_run_experiment_v2.py
# Updated for: economics-only arguments, new authority labels,
#              new prompt template (no system prompt)
# =============================================================
# All output files are prefixed with "v2_" to clearly separate
# from earlier data collection rounds.
# =============================================================


# ── CELL 1: Clone Repo & Mount Drive ─────────────────────────

import os

os.chdir('/content')

# Clone repo (fresh each time)
# !rm -rf /content/authority-bias-llm
# !git clone https://github.com/auertobias/authority-bias-llm.git /content/authority-bias-llm

os.chdir('/content/authority-bias-llm')

from google.colab import drive
drive.mount('/content/drive')

# !pip install -q google-genai openai anthropic


# ── CELL 2: Configure ────────────────────────────────────────

import os, sys
sys.path.insert(0, '.')

from src.config import DATA_PATH, RESULTS_PATH, N_REPS, PAUSE_SECONDS, CHECKPOINT_EVERY

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)
print(f"Data saves to: {DATA_PATH}")

# Version tag — prefixed to ALL output files
VERSION = "v2"


# ── CELL 3: API Keys ─────────────────────────────────────────

from google.colab import userdata

OPENAI_API_KEY    = userdata.get('OPEN_API_KEY')
DEEPSEEK_API_KEY  = userdata.get('DEEPSEEK_API_KEY')
GEMINI_API_KEY    = userdata.get('GEMINI_API_KEY')
# ANTHROPIC_API_KEY = userdata.get('ANTHROPIC_API_KEY')
# TOGETHER_API_KEY  = userdata.get('TOGETHER_API_KEY')  # for Llama


# ── CELL 4: Load New Data ────────────────────────────────────
# NOTE: These are the NEW files. The old arguments.csv and
# authority.csv are still on Drive but are NOT loaded here.

import pandas as pd

arguments   = pd.read_csv(DATA_PATH + "arguments_economics.csv")
authorities = pd.read_csv(DATA_PATH + "authority_labels.csv")

print(f"Arguments:   {len(arguments)} rows, {arguments['claim_id'].nunique()} claims")
print(f"Authorities: {len(authorities)} labels")
print(f"  Matched:      {len(authorities[authorities['layer']=='matched'])}")
print(f"  Reference:    {len(authorities[authorities['layer']=='reference'])}")
print(f"  Naturalistic: {len(authorities[authorities['layer']=='naturalistic'])}")


# ── CELL 5: Build Trials ─────────────────────────────────────
# Key difference from v1: expertise is pre-coded in
# authority_labels.csv — no need to compute it by comparing
# branches. Every argument is economics, so expertise depends
# only on the authority label, not the argument.

trials = []
trial_id = 0

for _, arg in arguments.iterrows():
    for _, auth in authorities.iterrows():
        trial_id += 1
        trials.append({
            'trial_id':        trial_id,
            'argument_id':     arg['id'],
            'claim_id':        arg['claim_id'],
            'claim':           arg['claim'],
            'argument':        arg['argument'],
            'stance':          arg['stance'],
            'arg_type':        arg['type'],
            'topic':           arg['topic'],
            'authority_id':    auth['authority_id'],
            'authority_label': auth['label'].strip(),
            'status':          auth['status'],
            'expertise':       auth['expertise'],
            'layer':           auth['layer'],
            'pair_id':         auth['pair_id'] if pd.notna(auth['pair_id']) else '',
        })

trials_df = pd.DataFrame(trials)
trials_df = trials_df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\nTotal trials: {len(trials_df)}")
print(f"  = {len(arguments)} arguments × {len(authorities)} labels")

print(f"\n── Matched pairs (primary analysis) ──")
matched = trials_df[trials_df['layer'] == 'matched']
print(matched.groupby(['status', 'expertise', 'arg_type']).size().unstack(fill_value=0))

print(f"\n── Reference conditions ──")
ref = trials_df[trials_df['layer'] == 'reference']
print(ref.groupby(['authority_label', 'arg_type']).size().unstack(fill_value=0))

print(f"\n── Naturalistic titles ──")
nat = trials_df[trials_df['layer'] == 'naturalistic']
print(nat.groupby(['authority_label', 'status']).size())


# ── CELL 6: Prepare Hidden Condition ─────────────────────────
# Hidden condition runs on matched pairs + reference only
# (the theoretically important comparisons).
# Naturalistic titles are supplementary and only need open.

trials_hidden = trials_df[
    trials_df['layer'].isin(['matched', 'reference'])
].copy().reset_index(drop=True)

print(f"Open trials:   {len(trials_df)}  (all labels)")
print(f"Hidden trials: {len(trials_hidden)}  (matched + reference only)")


# ── CELL 7: Choose Models ────────────────────────────────────

import importlib
import src.models
importlib.reload(src.models)

from src.models import make_gemini_fn, make_gpt_fn, make_deepseek_fn
# from src.models import make_claude_fn, make_llama_fn
from src.prompts import build_prompt, build_prompt_hidden
from src.parsing import extract_rating

# Uncomment the models you want to run:
MODELS = {
    'gpt':      make_gpt_fn(OPENAI_API_KEY),
    # 'deepseek': make_deepseek_fn(DEEPSEEK_API_KEY),
    # 'gemini':   make_gemini_fn(GEMINI_API_KEY),
    # 'claude':   make_claude_fn(ANTHROPIC_API_KEY),
    # 'llama':    make_llama_fn(TOGETHER_API_KEY),
}


# ── CELL 8: Run Experiment ───────────────────────────────────

import time
from datetime import datetime

date_str = datetime.now().strftime("%Y%m%d")

for model_name, model_fn in MODELS.items():

    # ── CONDITION 1: OPEN ─────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  {VERSION} | {model_name.upper()} — OPEN condition")
    print(f"{'='*60}")

    results_open = []

    for rep in range(N_REPS):
        run_order = trials_df.sample(frac=1, random_state=rep*1000).reset_index(drop=True)
        print(f"\n--- Rep {rep+1}/{N_REPS} ({len(run_order)} trials) ---")

        for idx, row in run_order.iterrows():
            prompt = build_prompt(row)
            raw = model_fn(prompt)
            rating = extract_rating(raw)

            results_open.append({
                'trial_id':        row['trial_id'],
                'rep':             rep + 1,
                'model':           model_name,
                'version':         VERSION,
                'condition':       'open',
                'argument_id':     row['argument_id'],
                'claim_id':        row['claim_id'],
                'claim':           row['claim'],
                'argument':        row['argument'],
                'stance':          row['stance'],
                'arg_type':        row['arg_type'],
                'topic':           row['topic'],
                'authority_id':    row['authority_id'],
                'authority_label': row['authority_label'],
                'status':          row['status'],
                'expertise':       row['expertise'],
                'layer':           row['layer'],
                'pair_id':         row['pair_id'],
                'rating':          rating,
                'raw_response':    raw,
            })

            n_done = idx + 1
            if n_done % 50 == 0:
                print(f"  {n_done}/{len(run_order)} done | last rating: {rating}")

            if n_done % CHECKPOINT_EVERY == 0:
                pd.DataFrame(results_open).to_csv(
                    DATA_PATH + f"{VERSION}_checkpoint_{model_name}_open.csv",
                    index=False
                )

            time.sleep(PAUSE_SECONDS)

    # Save open condition
    filepath_open = DATA_PATH + f"{VERSION}_data_{model_name}_open_{date_str}.csv"
    pd.DataFrame(results_open).to_csv(filepath_open, index=False)
    valid = sum(1 for r in results_open if r['rating'] is not None)
    print(f"\n✓ Saved: {filepath_open}")
    print(f"  {len(results_open)} rows, {valid} valid ratings ({100*valid/len(results_open):.0f}%)")

    # ── CONDITION 2: HIDDEN ───────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  {VERSION} | {model_name.upper()} — HIDDEN condition")
    print(f"{'='*60}")

    results_hidden = []

    for rep in range(N_REPS):
        run_order = trials_hidden.sample(frac=1, random_state=rep*2000).reset_index(drop=True)
        print(f"\n--- Rep {rep+1}/{N_REPS} ({len(run_order)} trials) ---")

        for idx, row in run_order.iterrows():
            prompt = build_prompt_hidden(row)
            raw = model_fn(prompt)
            rating = extract_rating(raw)

            results_hidden.append({
                'trial_id':        row['trial_id'],
                'rep':             rep + 1,
                'model':           model_name,
                'version':         VERSION,
                'condition':       'hidden',
                'argument_id':     row['argument_id'],
                'claim_id':        row['claim_id'],
                'claim':           row['claim'],
                'argument':        '',
                'stance':          row['stance'],
                'arg_type':        row['arg_type'],
                'topic':           row['topic'],
                'authority_id':    row['authority_id'],
                'authority_label': row['authority_label'],
                'status':          row['status'],
                'expertise':       row['expertise'],
                'layer':           row['layer'],
                'pair_id':         row['pair_id'],
                'rating':          rating,
                'raw_response':    raw,
            })

            n_done = idx + 1
            if n_done % 50 == 0:
                print(f"  {n_done}/{len(run_order)} done | last rating: {rating}")

            if n_done % CHECKPOINT_EVERY == 0:
                pd.DataFrame(results_hidden).to_csv(
                    DATA_PATH + f"{VERSION}_checkpoint_{model_name}_hidden.csv",
                    index=False
                )

            time.sleep(PAUSE_SECONDS)

    # Save hidden condition
    filepath_hidden = DATA_PATH + f"{VERSION}_data_{model_name}_hidden_{date_str}.csv"
    pd.DataFrame(results_hidden).to_csv(filepath_hidden, index=False)
    valid = sum(1 for r in results_hidden if r['rating'] is not None)
    print(f"\n✓ Saved: {filepath_hidden}")
    print(f"  {len(results_hidden)} rows, {valid} valid ratings ({100*valid/len(results_hidden):.0f}%)")

    print(f"\n{'='*60}")
    print(f"  DONE: {VERSION} | {model_name.upper()} — both conditions complete")
    print(f"{'='*60}")


# ── CELL 9: Verify ───────────────────────────────────────────

import glob

print("\n── v2 data files ──")
v2_files = sorted(glob.glob(DATA_PATH + f"{VERSION}_data_*.csv"))
for f in v2_files:
    df_check = pd.read_csv(f)
    valid = df_check['rating'].notna().sum()
    print(f"  {os.path.basename(f):50s} → {len(df_check)} rows, {valid} valid")

print("\n── Old v1 data files (untouched) ──")
v1_files = sorted(glob.glob(DATA_PATH + "data_*.csv"))
for f in v1_files:
    df_check = pd.read_csv(f)
    print(f"  {os.path.basename(f):50s} → {len(df_check)} rows")
