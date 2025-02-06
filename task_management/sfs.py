import argparse
import os
import subprocess
import sys
import uuid
import winreg
import textwrap

def main():
    parser = argparse.ArgumentParser(
        description="Schedule one or more commands to run at Windows startup."
    )
    parser.add_argument(
        "--parallel", action="store_true",
        help="Run all commands concurrently (by default they run sequentially)."
    )
    parser.add_argument(
        "--repeat", action="store_true",
        help="If set, the scheduled task will run at every startup; otherwise it runs only once."
    )
    parser.add_argument(
        "commands", nargs="+",
        help="The command(s) to schedule. (If a command has spaces, enclose it in quotes.)"
    )
    args = parser.parse_args()

    # Capture the current working directory (strip any trailing backslash to avoid raw string issues)
    working_dir = os.getcwd().rstrip("\\")

    # Generate a unique ID for this scheduled task.
    task_id = uuid.uuid4().hex

    # Create (if needed) a folder to store the scheduled task scripts.
    tasks_folder = os.path.join(os.getenv("APPDATA"), "rbs_sfs_tasks")
    os.makedirs(tasks_folder, exist_ok=True)

    # Full path to the task script that will run at startup.
    task_filename = os.path.join(tasks_folder, f"sfs_task_{task_id}.py")

    # Build the content of the scheduled task script.
    # This script will open new consoles and run the commands.
    task_script = textwrap.dedent(f"""
        import subprocess
        import os
        import sys

        def run_command(cmd):
            return subprocess.Popen(
                ["cmd.exe", "/c", cmd],
                cwd=r"{working_dir}",
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

        commands = {args.commands}
        parallel = {args.parallel}

        processes = []
        if parallel:
            for command in commands:
                p = run_command(command)
                processes.append(p)
            for p in processes:
                p.wait()
        else:
            for command in commands:
                p = run_command(command)
                p.wait()

        # If not repeating, remove this task script after execution.
        repeat = {args.repeat}
        if not repeat:
            try:
                os.remove(sys.argv[0])
            except Exception:
                pass
        """)

    # Write the scheduled task script to file.
    with open(task_filename, "w") as f:
        f.write(task_script)

    # Determine which registry key to use.
    # Use "RunOnce" for one-off tasks, or "Run" for repeated tasks.
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\RunOnce" if not args.repeat else r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
    except Exception:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

    # Command that will run the scheduled task.
    # (This assumes that the Python executable is in your PATH.)
    command_to_run = f'python "{task_filename}"'
    task_name = f"sfs_task_{task_id}"
    winreg.SetValueEx(reg_key, task_name, 0, winreg.REG_SZ, command_to_run)
    winreg.CloseKey(reg_key)

    print(f"Scheduled task '{task_name}' has been created to run at startup.")
    print("The following command(s) will be executed:")
    for cmd in args.commands:
        print(f"  {cmd}")

if __name__ == "__main__":
    main()
