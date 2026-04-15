# src/config.py
# Central configuration — change paths here, everything else follows.

# Google Drive paths (mounted in Colab at /content/drive/MyDrive/)
PROJECT_PATH = "/content/drive/MyDrive/PhD/2PhD 1Paper/"
DATA_PATH    = PROJECT_PATH + "data/"
RESULTS_PATH = PROJECT_PATH + "results/"

# Experiment settings
N_REPS           = 1      # 1 for testing, 10+ for the paper
PAUSE_SECONDS    = 1    # delay between API calls
CHECKPOINT_EVERY = 50     # save progress every N trials
TEMPERATURE      = 0.7
MAX_TOKENS       = 1024
