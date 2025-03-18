import os
import subprocess

# 檔案名稱列表
command_files = [
    "add_income_to_community.py",
    # "load_2016_Census_of_Canada_-_Household_Income_20240806.py",
    # "load_2023_community_crimes_csv.py",
    # "load_community_csv.py",
    # "load_community_services.py"
]

base_dir = os.path.dirname(os.path.abspath(__file__))
commands_path = os.path.join(base_dir, 'commands')

for command_file in command_files:
    command_path = os.path.join(commands_path, command_file)
    try:
        subprocess.run(["python", command_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {command_file}: {e}")