import argparse
import subprocess
import os

def run_command(command):
    """
    Run a command in a new console window.
    The command is executed with the current working directory.
    """
    return subprocess.Popen(
        ["cmd.exe", "/c", command],
        cwd=os.getcwd(),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def main():
    parser = argparse.ArgumentParser(
        description="Run one or more commands in new command prompt windows, then shut down the computer."
    )
    parser.add_argument(
        "--parallel", action="store_true",
        help="Run all commands concurrently (by default they run sequentially)."
    )
    parser.add_argument(
        "commands", nargs="+",
        help="The command(s) to execute. (If a command has spaces, enclose it in quotes.)"
    )
    args = parser.parse_args()

    processes = []

    if args.parallel:
        # Start all commands concurrently.
        for cmd in args.commands:
            p = run_command(cmd)
            processes.append(p)
        # Wait for all commands to finish.
        for p in processes:
            p.wait()
    else:
        # Run commands one after the other.
        for cmd in args.commands:
            p = run_command(cmd)
            p.wait()

    # Once all commands have finished, shut down the computer.
    subprocess.call(["shutdown", "/s", "/t", "0"])

if __name__ == "__main__":
    main()
