# RBS & SFS Scripts

This project provides two Python scripts that let you automate command execution tasks in Windows:

- **rbs.py (Run Before Shutdown):** Executes one or more commands in new command prompt windows and shuts down Windows after all commands finish.
- **sfs.py (Schedule For Startup):** Schedules one or more commands to run at Windows startup, either once or repeatedly.

---

## Overview

### rbs (Run Before Shutdown)
- **Purpose:**  
  Execute one or multiple commands in new console windows and then shut down the computer.
- **Features:**
  - Accepts one or multiple commands.
  - By default, commands run sequentially (each waits for the previous one to finish).
  - Use the `--parallel` flag to run commands concurrently.
  - Commands are executed in the current working directory.
  - Initiates a Windows shutdown once all commands have completed.

### sfs (Schedule For Startup)
- **Purpose:**  
  Schedule commands to run at the next Windows startup.
- **Features:**
  - Accepts one or multiple commands.
  - Commands run in new console windows in the current working directory.
  - By default, tasks are scheduled to run only once.
  - Use the `--parallel` flag to execute commands concurrently.
  - Use the `--repeat` flag to schedule the task to run at every startup.
  - The scheduled task is created via a registry entry under HKEY_CURRENT_USER using either the `RunOnce` (one-off) or `Run` (repeating) key.

---

## Files in This Project

- **rbs.py:**  
  Executes provided commands (sequentially or in parallel) and shuts down the system after they finish.
  
- **sfs.py:**  
  Creates a scheduled startup task by writing a temporary Python script (stored in the user's AppData folder) and registering it in the Windows Registry. The task will execute the specified commands at the next startup (or every startup if `--repeat` is used).

---

## Requirements

- **Operating System:** Windows
- **Python:** Installed and available in your system’s PATH.
- **Permissions:**  
  - Typically, modifying the registry under HKEY_CURRENT_USER does not require administrator privileges.
  - Ensure you have sufficient rights to trigger a shutdown if using `rbs.py`.

---

## Installation & Setup

1. **Download or Clone the Repository:**  
   Place `rbs.py` and `sfs.py` in a folder, e.g., `C:\Scripts\`.

2. **(Optional) Create Batch File Wrappers:**

   To easily call these scripts from any command prompt, create batch files:

   - **rbs.bat**
     ```
     @echo off
     python "C:\Scripts\rbs.py" %*
     ```

   - **sfs.bat**
     ```
     @echo off
     python "C:\Scripts\sfs.py" %*
     ```

   *Make sure to adjust the path if your scripts are stored elsewhere.*

3. **Add the Folder to Your PATH:**

   - Open the **Start Menu**, search for “Environment Variables,” and select “Edit the system environment variables.”
   - In the System Properties window, click **“Environment Variables…”**.
   - Under **User variables** (or **System variables**), select the **`Path`** variable and click **Edit**.
   - Click **New** and add the full path to your scripts folder (e.g., `C:\Scripts\`).
   - Click **OK** to save all changes.

   This allows you to run `rbs` or `sfs` from any command prompt.

---

## Usage Examples

### Running Commands Before Shutdown (rbs)

- **Sequential Execution (default):**
```
rbs "echo Hello, world!" "dir /s"
```

- **Parallel Execution:**
```
rbs --parallel "python -m unittest" "ping -n 5 127.0.0.1"
```

After all specified commands complete, the computer will shut down normally.

### Scheduling Commands for Startup (sfs)

- **One-off Startup Task:**
```
sfs "echo Running startup task" "dir"
```

- **Repeating Startup Task (runs every startup):**
```
sfs --repeat "echo This runs every startup"
```

The scheduled commands will execute in new command prompt windows the next time Windows starts (or at every startup with `--repeat`).

---

## How It Works

### rbs.py
- **Argument Parsing:**
- Uses `argparse` to read commands and flags (`--parallel`).
- **Command Execution:**
- Each command is launched in a new console window with the current working directory.
- **Sequential:** Commands are executed one after the other.
- **Parallel:** All commands are launched concurrently and then waited upon.
- **Shutdown Trigger:**
- Once all processes complete, the script calls `shutdown /s /t 0` to shut down Windows.

### sfs.py
- **Argument Parsing:**
- Uses `argparse` to process the commands and flags (`--parallel`, `--repeat`).
- **Scheduled Task Script Creation:**
- Generates a unique Python script that contains the logic to run the commands at startup.
- Saves this script to a folder (e.g., `%APPDATA%\rbs_sfs_tasks`).
- **Registry Entry:**
- For one-off tasks, a registry entry is added under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce`.
- For repeating tasks, the entry is added under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.
- **Execution at Startup:**
- On startup, Windows will execute the scheduled script which runs the commands. If the task is one-off (without `--repeat`), the script deletes itself after execution.

---

## Customization & Notes

- **Working Directory:**
- Both scripts run commands from the directory where you invoke the command, ensuring file paths are relative to your current location.
- **Python PATH:**
- Ensure Python is accessible via your system's PATH for both the batch wrappers and registry commands to work.
- **Modifications:**
- You can customize the behavior (e.g., change working directory defaults or add more flags) by modifying the Python source files directly.

---

## License
This project is provided as-is without any warranty. Use it at your own risk.

Enjoy automating your Windows tasks with RBS and SFS!
