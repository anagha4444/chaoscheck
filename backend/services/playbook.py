import re
import os

def load_playbook():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # backend/
    file_path = os.path.join(base_dir, "knowledge", "remediation_guide.md")

    with open(file_path, "r") as f:
        return f.read()

    sections = content.split("# Service:")
    playbooks = []

    for sec in sections[1:]:
        lines = sec.strip().split("\n")

        service = lines[0].strip()
        error = None
        fix = None

        for line in lines:
            if "Error:" in line:
                error = line.replace("## Error:", "").strip()
            if "Fix:" in line:
                fix_line = line.replace("- **Fix:**", "").strip()
                fix = [cmd.strip("`") for cmd in fix_line.split("or")]

        if error and fix:
            playbooks.append({
                "service": service,
                "error": error,
                "fix": fix
            })

    return playbooks