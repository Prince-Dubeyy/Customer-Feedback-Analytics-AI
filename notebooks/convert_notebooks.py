import os
import subprocess
import glob
import sys

# Ensure we're in the notebooks directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

scripts = sorted(glob.glob("*.py"))
scripts = [s for s in scripts if s != "convert_notebooks.py"]

print("Executing pipeline and converting to notebooks...")

for script in scripts:
    print(f"\n--- Running {script} ---")
    # Execute the script to generate outputs and models
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Error running {script}")
        exit(1)
    
    print(f"\n--- Converting {script} to Jupyter Notebook ---")
    # Convert to notebook using jupytext
    subprocess.run([sys.executable, "-m", "jupytext", "--to", "notebook", script])
    
print("\nPipeline execution and conversion complete!")

