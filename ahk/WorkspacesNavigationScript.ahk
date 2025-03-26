; Globals
DesktopCount = 2 ; Windows starts with 2 desktops at boot
CurrentDesktop = 1 ; Desktop count is 1-indexed (Microsoft numbers them this way)
PromptfooRunning = 0 ; Track if promptfoo is running
PromptfooCmdTitle = "C:\Windows\system32\cmd.exe"  ; Standard CMD window title
PromptfooWindowID = 0 ; Store window ID
;
; This function examines the registry to build an accurate list of the current virtual desktops and which one we're currently on.
; Current desktop UUID appears to be in HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo\1\VirtualDesktops
; List of desktops appears to be in HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops
;
mapDesktopsFromRegistry() {
 global CurrentDesktop, DesktopCount
 ; Get the current desktop UUID. Length should be 32 always, but there's no guarantee this couldn't change in a later Windows release so we check.
 IdLength := 32
 SessionId := getSessionId()
 if (SessionId) {
 RegRead, CurrentDesktopId, HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo\%SessionId%\VirtualDesktops, CurrentVirtualDesktop
 if (CurrentDesktopId) {
 IdLength := StrLen(CurrentDesktopId)
 }
 }
 ; Get a list of the UUIDs for all virtual desktops on the system<
 RegRead, DesktopList, HKEY_CURRENT_USER, SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops, VirtualDesktopIDs
 if (DesktopList) {
 DesktopListLength := StrLen(DesktopList)
 ; Figure out how many virtual desktops there are
 DesktopCount := DesktopListLength / IdLength
 }
 else {
 DesktopCount := 1
 }
 ; Parse the REG_DATA string that stores the array of UUID's for virtual desktops in the registry.
 i := 0
 while (CurrentDesktopId and i < DesktopCount) {
 StartPos := (i * IdLength) + 1
 DesktopIter := SubStr(DesktopList, StartPos, IdLength)
 OutputDebug, The iterator is pointing at %DesktopIter% and count is %i%.
 ; Break out if we find a match in the list. If we didn't find anything, keep the
 ; old guess and pray we're still correct :-D.
 if (DesktopIter = CurrentDesktopId) {
 CurrentDesktop := i + 1
 OutputDebug, Current desktop number is %CurrentDesktop% with an ID of %DesktopIter%.
 break
 }
 i++
 }
}
;
; This functions finds out ID of current session.
;
getSessionId()
{
 ProcessId := DllCall("GetCurrentProcessId", "UInt")
 if ErrorLevel {
 OutputDebug, Error getting current process id: %ErrorLevel%
 return
 }
 OutputDebug, Current Process Id: %ProcessId%
 DllCall("ProcessIdToSessionId", "UInt", ProcessId, "UInt*", SessionId)
 if ErrorLevel {
 OutputDebug, Error getting session id: %ErrorLevel%
 return
 }
 OutputDebug, Current Session Id: %SessionId%
 return SessionId
}
;
; This function switches to the desktop number provided.
;
switchDesktopByNumber(targetDesktop)
{
 global CurrentDesktop, DesktopCount
 ; Re-generate the list of desktops and where we fit in that. We do this because
 ; the user may have switched desktops via some other means than the script.
 mapDesktopsFromRegistry()
 ; Don't attempt to switch to an invalid desktop
 if (targetDesktop > DesktopCount || targetDesktop < 1) {
 OutputDebug, [invalid] target: %targetDesktop% current: %CurrentDesktop%
 return
 }
 ; Go right until we reach the desktop we want
 while(CurrentDesktop < targetDesktop) {
 Send ^#{Right}
 CurrentDesktop++
 OutputDebug, [right] target: %targetDesktop% current: %CurrentDesktop%
 }
 ; Go left until we reach the desktop we want
 while(CurrentDesktop > targetDesktop) {
 Send ^#{Left}
 CurrentDesktop--
 OutputDebug, [left] target: %targetDesktop% current: %CurrentDesktop%
 }
}
;
; This function creates a new virtual desktop and switches to it
;
createVirtualDesktop()
{
 global CurrentDesktop, DesktopCount
 Send, #^d
 DesktopCount++
 CurrentDesktop = %DesktopCount%
 OutputDebug, [create] desktops: %DesktopCount% current: %CurrentDesktop%
}
;
; This function deletes the current virtual desktop
;
deleteVirtualDesktop()
{
 global CurrentDesktop, DesktopCount
 Send, #^{F4}
 DesktopCount--
 CurrentDesktop--
 OutputDebug, [delete] desktops: %DesktopCount% current: %CurrentDesktop%
}
; Main
SetKeyDelay, 75
mapDesktopsFromRegistry()
OutputDebug, [loading] desktops: %DesktopCount% current: %CurrentDesktop%

; User config!
; This section binds the key combo to the switch/create/delete actions
#z::switchDesktopByNumber(1)  ; Win+Z for Desktop 1
#x::switchDesktopByNumber(2)  ; Win+X for Desktop 2
#c::switchDesktopByNumber(3)  ; Win+C for Desktop 3
#v::switchDesktopByNumber(4)  ; Win+V for Desktop 4
#a::switchDesktopByNumber(5)  ; Win+A for Desktop 5
#s::switchDesktopByNumber(6)  ; Win+S for Desktop 6

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
            PromptfooRunning = 0
            PromptfooWindowID = 0
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
            PromptfooRunning = 1
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
        PromptfooRunning = 0
        PromptfooWindowID = 0
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