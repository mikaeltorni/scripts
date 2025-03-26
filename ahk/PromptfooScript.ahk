; PromptfooScript.ahk
; Script to start and stop promptfoo with F12/Ctrl+Win+F12 hotkeys

; Globals
PromptfooRunning := 0 ; Track if promptfoo is running
PromptfooWindowID := 0 ; Store window ID

; Main
#SingleInstance Force
SetKeyDelay, 75

; Run promptfoo command in CMD window
#F12::
    global PromptfooRunning, PromptfooWindowID
    
    ; Check if we have a stored window ID and if that window still exists
    if (PromptfooRunning = 1 && PromptfooWindowID != 0) {
        ; Check if window still exists
        WinGet, isExist, PID, ahk_id %PromptfooWindowID%
        if (isExist) {
            ; Window exists, activate it
            WinActivate, ahk_id %PromptfooWindowID%
            ToolTip, Promptfoo is already running. Use Ctrl+Win+F12 to close it first.
            SetTimer, RemoveToolTip, 3000
            return
        } else {
            ; Window doesn't exist anymore, reset status
            PromptfooRunning := 0
            PromptfooWindowID := 0
        }
    }
    
    ; At this point either we have confirmed it's not running or reset status
    if (PromptfooRunning = 0) {
        ; Start new CMD window and run the command (normal size)
        Run, cmd.exe /k npx promptfoo@latest view -y,, , cmdPID
        
        ; Wait for the window to open with longer timeout
        WinWait, ahk_pid %cmdPID%,, 10
        if ErrorLevel {
            ToolTip, Failed to start CMD window
            SetTimer, RemoveToolTip, 3000
            return
        }
        
        ; Store the Window ID
        WinGet, PromptfooWindowID, ID, ahk_pid %cmdPID%
        if (PromptfooWindowID) {
            PromptfooRunning := 1
            ToolTip, Promptfoo started successfully. Press Ctrl+Win+F12 to close.
            SetTimer, RemoveToolTip, 3000
        } else {
            ToolTip, Failed to get window ID
            SetTimer, RemoveToolTip, 3000
        }
    }
    return

; Close promptfoo instance with Ctrl+Win+F12
^#F12::
    global PromptfooRunning, PromptfooWindowID
    
    if (PromptfooRunning = 1 && PromptfooWindowID != 0) {
        ; Try to check if window exists
        WinGet, isExist, PID, ahk_id %PromptfooWindowID%
        if (isExist) {
            ; Window exists, terminate it
            WinActivate, ahk_id %PromptfooWindowID%
            
            ; Try to close gracefully with keyboard shortcuts
            SendInput, ^c
            Sleep, 500
            SendInput, exit{Enter}
            Sleep, 1000
            
            ; Check if still open
            WinGet, isStillExist, PID, ahk_id %PromptfooWindowID%
            if (isStillExist) {
                ; Try WM_CLOSE message
                WinClose, ahk_id %PromptfooWindowID%
                Sleep, 1000
                
                ; Last resort
                WinGet, isStillStillExist, PID, ahk_id %PromptfooWindowID%
                if (isStillStillExist) {
                    WinKill, ahk_id %PromptfooWindowID%
                    Sleep, 500
                }
            }
            
            ToolTip, Promptfoo has been closed.
            SetTimer, RemoveToolTip, 3000
        } else {
            ToolTip, Promptfoo window no longer exists.
            SetTimer, RemoveToolTip, 3000
        }
        
        ; Reset status regardless
        PromptfooRunning := 0
        PromptfooWindowID := 0
    } else {
        ToolTip, No promptfoo instance is running.
        SetTimer, RemoveToolTip, 3000
    }
    return

; Function to remove tooltip
RemoveToolTip:
    SetTimer, RemoveToolTip, Off
    ToolTip
    return 