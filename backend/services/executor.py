import subprocess

def execute_command(command):
    print(f"⚡ Executing: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print("✅ Output:", result.stdout)
        return True
    except Exception as e:
        print("❌ Execution failed:", str(e))
        return False