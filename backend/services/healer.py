from services.matcher import find_fix
from services.executor import execute_command
from services.verifier import verify_recovery
import datetime

def trigger_healer(error_log):
    print("\n🚨 INCIDENT DETECTED:", error_log)

    fix = find_fix(error_log)

    if not fix:
        print("❌ No fix found")
        return

    print("🧠 Decision:", fix)

    success = execute_command(fix["command"])

    if success:
        verified = verify_recovery(fix["service"])

        if verified:
            print("✅ SYSTEM RECOVERED\n")
        else:
            print("⚠ Fix applied but verification failed\n")

    log_incident(error_log, fix, success)

def log_incident(error, fix, success):
    with open("healer_logs.txt", "a") as f:
        f.write(f"""
Time: {datetime.datetime.now()}
Error: {error}
Fix: {fix}
Success: {success}
------------------------
""")