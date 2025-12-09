"""
Recommendation Model Retraining Pipeline
=========================================
Automates the complete retraining process:
1. Extract fresh data from MongoDB
2. Train the recommendation model
3. Save recommendations to database

Usage: python main.py [--skip-extract] [--skip-train] [--skip-save]
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime

SCRIPTS = [
    ("mongodb_extract.py", "Extracting data from MongoDB"),
    ("feature_extraction_v5.py", "Extracting features from products"),
    ("train_model_v5.py", "Training recommendation model"),
    ("save_recommendations_to_db.py", "Saving recommendations to database"),
]

GENERATED_FILES = [
    "all_products.csv",
    "candidate_pairs.csv", 
    "product_features_v5.csv",
    "training_history_autoencoder_v5.png",
]


def print_header(text):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)


def print_step(step_num, total, text):
    print(f"\n[{step_num}/{total}] {text}")
    print("-" * 50)


def clean_generated_files():
    print_header("CLEANING GENERATED FILES")
    for filename in GENERATED_FILES:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  Removed: {filename}")
        else:
            print(f"  Skipped (not found): {filename}")
    print("Cleanup complete.")


def run_script(script_name, description):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"ERROR: Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(__file__),
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {script_name} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to run {script_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Recommendation Model Retraining Pipeline")
    parser.add_argument("--skip-extract", action="store_true", help="Skip MongoDB extraction")
    parser.add_argument("--skip-train", action="store_true", help="Skip model training")
    parser.add_argument("--skip-save", action="store_true", help="Skip saving to database")
    parser.add_argument("--clean", action="store_true", help="Clean generated files before starting")
    args = parser.parse_args()

    print_header("RECOMMENDATION MODEL RETRAINING PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    skip_flags = [args.skip_extract, args.skip_train, args.skip_save]
    scripts_to_run = [(s, d) for (s, d), skip in zip(SCRIPTS, skip_flags) if not skip]
    
    if not scripts_to_run:
        print("No scripts to run. All steps were skipped.")
        return 0

    if args.clean:
        clean_generated_files()

    total_steps = len(scripts_to_run)
    failed_scripts = []

    for i, (script, description) in enumerate(scripts_to_run, 1):
        print_step(i, total_steps, description)
        
        success = run_script(script, description)
        
        if success:
            print(f"Completed: {script}")
        else:
            print(f"Failed: {script}")
            failed_scripts.append(script)
            print("\nAborting pipeline due to failure.")
            break

    print_header("PIPELINE SUMMARY")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_scripts:
        print(f"Status: FAILED")
        print(f"Failed scripts: {', '.join(failed_scripts)}")
        return 1
    else:
        print(f"Status: SUCCESS")
        print(f"All {total_steps} steps completed successfully.")
        return 0


if __name__ == "__main__":
    exit(main())
