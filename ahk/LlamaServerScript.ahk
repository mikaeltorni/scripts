; LlamaServerScript.ahk
; Script to start and stop the Llama server with F11/Ctrl+Win+F11 hotkeys

; Globals
LlamaRunning := 0 ; Track if Llama server is running
LlamaWindowID := 0 ; Store window ID
LlamaLocationFile := "llamaLocation.txt" ; File containing the Llama directory path
ModelLocationFile := "modelLocation.txt" ; File containing the model directory path

; Main
#SingleInstance Force
SetKeyDelay, 75

; Run Llama server in CMD window
#F11::
    global LlamaRunning, LlamaWindowID, LlamaLocationFile
    
    ; Check if we have a stored window ID and if that window still exists
    if (LlamaRunning = 1 && LlamaWindowID != 0) {
        ; Check if window still exists
        WinGet, isExist, PID, ahk_id %LlamaWindowID%
        if (isExist) {
            ; Window exists, activate it
            WinActivate, ahk_id %LlamaWindowID%
            ToolTip, Llama server is already running. Use Ctrl+Win+F11 to close it first.
            SetTimer, RemoveToolTip, 3000
            return
        } else {
            ; Window doesn't exist anymore, reset status
            LlamaRunning := 0
            LlamaWindowID := 0
        }
    }
    
    ; Check if the location file exists
    if (!FileExist(LlamaLocationFile)) {
        ; Create the file with default path
        FileAppend, C:\Projects\ai\llama.cpp, %LlamaLocationFile%
        ToolTip, Created llamaLocation.txt with default path. Edit if needed.
        SetTimer, RemoveToolTip, 5000
    }
    
    ; Read the Llama location from file
    FileRead, LlamaPath, %LlamaLocationFile%
    if (ErrorLevel) {
        ToolTip, Error reading Llama location from file.
        SetTimer, RemoveToolTip, 3000
        return
    }
    
    ; Trim any whitespace
    LlamaPath := Trim(LlamaPath)
    
    ; At this point either we have confirmed it's not running or reset status
    if (LlamaRunning = 0) {
        ; Construct the command to run - using simpler string concatenation
        CmdLine := "cmd.exe /k set CUDA_VISIBLE_DEVICES=-0 && " . LlamaPath . "\build\bin\Release\llama-server --model " . LlamaPath . "\..\models\" . ModelLocationFile . " --n-gpu-layers 420"
        
        ; Start new CMD window and run the command (normal size)
        Run, %CmdLine%,, , cmdPID
        
        ; Wait for the window to open with longer timeout
        WinWait, ahk_pid %cmdPID%,, 10
        if ErrorLevel {
            ToolTip, Failed to start CMD window for Llama
            SetTimer, RemoveToolTip, 3000
            return
        }
        
        ; Store the Window ID
        WinGet, LlamaWindowID, ID, ahk_pid %cmdPID%
        if (LlamaWindowID) {
            LlamaRunning := 1
            ToolTip, Llama server started successfully. Press Ctrl+Win+F11 to close.
            SetTimer, RemoveToolTip, 3000
        } else {
            ToolTip, Failed to get window ID for Llama server
            SetTimer, RemoveToolTip, 3000
        }
    }
    return

; Close Llama server instance with Ctrl+Win+F11
^#F11::
    global LlamaRunning, LlamaWindowID
    
    if (LlamaRunning = 1 && LlamaWindowID != 0) {
        ; Try to check if window exists
        WinGet, isExist, PID, ahk_id %LlamaWindowID%
        if (isExist) {
            ; Window exists, terminate it
            WinActivate, ahk_id %LlamaWindowID%
            
            ; Try to close gracefully with keyboard shortcuts
            SendInput, ^c
            Sleep, 500
            SendInput, exit{Enter}
            Sleep, 1000
            
            ; Check if still open
            WinGet, isStillExist, PID, ahk_id %LlamaWindowID%
            if (isStillExist) {
                ; Try WM_CLOSE message
                WinClose, ahk_id %LlamaWindowID%
                Sleep, 1000
                
                ; Last resort
                WinGet, isStillStillExist, PID, ahk_id %LlamaWindowID%
                if (isStillStillExist) {
                    WinKill, ahk_id %LlamaWindowID%
                    Sleep, 500
                }
            }
            
            ToolTip, Llama server has been closed.
            SetTimer, RemoveToolTip, 3000
        } else {
            ToolTip, Llama server window no longer exists.
            SetTimer, RemoveToolTip, 3000
        }
        
        ; Reset status regardless
        LlamaRunning := 0
        LlamaWindowID := 0
    } else {
        ToolTip, No Llama server instance is running.
        SetTimer, RemoveToolTip, 3000
    }
    return

; Function to remove tooltip
RemoveToolTip:
    SetTimer, RemoveToolTip, Off
    ToolTip
    return 