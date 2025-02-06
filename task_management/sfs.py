import argparse
import os
import subprocess
import sys
import uuid
import winreg
import textwrap

def list_tasks():
    """
    Scans both the Run and RunOnce registry keys for tasks created by sfs (names starting with 'sfs_task_')
    and returns a list of dictionaries containing task details.
    """
    tasks = []
    registry_keys = [
        (r"Software\Microsoft\Windows\CurrentVersion\Run", "Run"),
        (r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "RunOnce")
    ]
    for reg_path, key_label in registry_keys:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        except Exception:
            continue
        index = 0
        while True:
            try:
                name, data, _ = winreg.EnumValue(reg_key, index)
                if name.startswith("sfs_task_"):
                    tasks.append({
                        "name": name,
                        "command": data,
                        "reg_path": reg_path,
                        "key_label": key_label
                    })
                index += 1
            except OSError:
                break
        winreg.CloseKey(reg_key)
    return tasks

def remove_task_by_index(task_index):
    """
    Removes the scheduled task (both registry entry and its scheduled file, if applicable)
    corresponding to the given index.
    """
    tasks = list_tasks()
    if task_index < 0 or task_index >= len(tasks):
        print(f"Invalid task index: {task_index}")
        return
    task = tasks[task_index]

    # Remove the registry entry
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, task["reg_path"], 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(reg_key, task["name"])
        winreg.CloseKey(reg_key)
        print(f"Removed task [{task_index}]: {task['name']} from {task['key_label']}")
    except Exception as e:
        print(f"Error removing registry entry: {e}")

    # Try to remove the scheduled file.
    # The command is expected to be of the form: "full_path_to_python" "full_path_to_task_file"
    cmd = task["command"]
    try:
        parts = cmd.split('"')
        # Expecting a command like: "C:\Path\to\python.exe" "C:\...\sfs_task_XXXX.py"
        if len(parts) >= 4:
            task_file = parts[3]
            if os.path.exists(task_file):
                os.remove(task_file)
                print(f"Removed scheduled file: {task_file}")
        else:
            print("Could not parse the file path from the command string.")
    except Exception as e:
        print(f"Error removing scheduled file: {e}")

def schedule_tasks(args):
    """
    Schedules a new startup task based on the provided arguments.
    """
    # Capture the current working directory (remove trailing backslash)
    working_dir = os.getcwd().rstrip("\\")
    # Generate a unique ID for the scheduled task.
    task_id = uuid.uuid4().hex
    # Create a folder in %APPDATA% to store scheduled task scripts.
    tasks_folder = os.path.join(os.getenv("APPDATA"), "rbs_sfs_tasks")
    os.makedirs(tasks_folder, exist_ok=True)
    # Full path for the scheduled task file.
    task_filename = os.path.join(tasks_folder, f"sfs_task_{task_id}.py")

    # Create the content of the scheduled task file.
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

        # For one-off tasks, remove the script file after execution.
        repeat = {args.repeat}
        if not repeat:
            try:
                os.remove(sys.argv[0])
            except Exception:
                pass
        """)
    with open(task_filename, "w") as f:
        f.write(task_script)

    # Choose registry key based on --repeat flag.
    reg_path = (r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
                if not args.repeat else
                r"Software\Microsoft\Windows\CurrentVersion\Run")
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
    except Exception:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

    # Use the absolute path to the Python interpreter.
    command_to_run = f'"{sys.executable}" "{task_filename}"'
    task_name = f"sfs_task_{task_id}"
    winreg.SetValueEx(reg_key, task_name, 0, winreg.REG_SZ, command_to_run)
    winreg.CloseKey(reg_key)

    print(f"Scheduled task '{task_name}' has been created to run at startup.")
    print("The following command(s) will be executed:")
    for cmd in args.commands:
        print(f"  {cmd}")

def main():
    parser = argparse.ArgumentParser(
        description="Schedule commands to run at Windows startup or manage scheduled tasks."
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands: schedule (default), tasks, remove")

    # Subparser for listing tasks.
    parser_tasks = subparsers.add_parser("tasks", help="List scheduled tasks")

    # Subparser for removing a task.
    parser_remove = subparsers.add_parser("remove", help="Remove a scheduled task by its index (see 'sfs tasks')")
    parser_remove.add_argument("task_index", type=int, help="Index of the task to remove")

    # Subparser for scheduling tasks.
    parser_schedule = subparsers.add_parser("schedule", help="Schedule a new startup task")
    parser_schedule.add_argument("--parallel", action="store_true", help="Run all commands concurrently")
    parser_schedule.add_argument("--repeat", action="store_true", help="Schedule the task to run at every startup (default is one-off)")
    parser_schedule.add_argument("commands", nargs="+", help="The command(s) to schedule (enclose commands with spaces in quotes)")

    # If no subcommand is provided, assume scheduling mode.
    if len(sys.argv) > 1 and sys.argv[1] not in ["tasks", "remove"]:
        # Insert "schedule" as the subcommand if it's not "tasks" or "remove"
        if sys.argv[1] != "schedule":
            sys.argv.insert(1, "schedule")
    args = parser.parse_args()

    if args.subcommand == "tasks":
        tasks = list_tasks()
        if not tasks:
            print("No scheduled tasks found.")
        else:
            print("Scheduled tasks:")
            for idx, task in enumerate(tasks):
                print(f"[{idx}] {task['name']} ({task['key_label']}) -> {task['command']}")
    elif args.subcommand == "remove":
        remove_task_by_index(args.task_index)
    elif args.subcommand == "schedule":
        schedule_tasks(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
