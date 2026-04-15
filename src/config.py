# src/config.py
# Central configuration — change paths here, everything else follows.

# Google Drive paths (mounted in Colab at /content/drive/MyDrive/)
PROJECT_PATH = "/content/drive/MyDrive/PhD/2PhD 1Paper/"
DATA_PATH    = PROJECT_PATH + "data/"
RESULTS_PATH = PROJECT_PATH + "results/"

# Experiment settings
N_REPS           = 1      # 1 for testing, 10+ for the paper
PAUSE_SECONDS = {
    'gpt':      0.3,   # OpenAI tier limits are generous; latency is your throttle
    'deepseek': 0.3,   # slow API, no need to add delay
    'gemini':   0.3,   # 2.5-flash free tier has tight RPM; paid is fine at 0
    'claude':   1.0,   # Haiku 4.5 needs this to avoid Sonnet fallback
    'llama':    0.3,   # Together is latency-bound
}
CHECKPOINT_EVERY = 50     # save progress every N trials
TEMPERATURE      = 0.7
MAX_TOKENS       = 1024
