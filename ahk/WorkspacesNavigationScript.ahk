; WorkspacesNavigationScript.ahk
; Script to switch between Windows 10 virtual desktops using Windows+Numpad keys 1-9
; Requires VirtualDesktopAccessor.dll in the same directory

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#SingleInstance Force  ; Ensure only one instance is running
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; Display initial debugging message
MsgBox, 64, Virtual Desktop Switcher, Script is starting. Will now attempt to load VirtualDesktopAccessor.dll, 3

; Initialize VirtualDesktopAccessor.dll
DetectHiddenWindows, On
hwnd := WinExist("ahk_pid " . DllCall("GetCurrentProcessId", "Uint"))
hwnd += 0x1000 << 32

; Load the DLL - adjust the path if needed
dllPath := A_ScriptDir . "\VirtualDesktopAccessor.dll"
hVirtualDesktopAccessor := DllCall("LoadLibrary", "Str", dllPath, "Ptr")
if (hVirtualDesktopAccessor == 0) {
    MsgBox, 16, Error, Failed to load VirtualDesktopAccessor.dll.`nEnsure it's in the same directory as this script.`n`nAttempted to load from: %dllPath%
    ExitApp
}

; Get function pointers from the DLL and check for any errors
GoToDesktopNumberProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "GoToDesktopNumber", "Ptr")
if (GoToDesktopNumberProc == 0) {
    MsgBox, 16, Error, Failed to get GoToDesktopNumber function. The DLL might not be compatible with your Windows version.
    ExitApp
}

GetCurrentDesktopNumberProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "GetCurrentDesktopNumber", "Ptr")
GetDesktopCountProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "GetDesktopCount", "Ptr")
IsWindowOnCurrentVirtualDesktopProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "IsWindowOnCurrentVirtualDesktop", "Ptr")
MoveWindowToDesktopNumberProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "MoveWindowToDesktopNumber", "Ptr")
IsPinnedWindowProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "IsPinnedWindow", "Ptr")
RestartVirtualDesktopAccessorProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "RestartVirtualDesktopAccessor", "Ptr")

; Restart the virtual desktop accessor when Explorer.exe crashes, or restarts (e.g. when coming from fullscreen game)
explorerRestartMsg := DllCall("user32\RegisterWindowMessage", "Str", "TaskbarCreated")
OnMessage(explorerRestartMsg, "OnExplorerRestart")
OnExplorerRestart(wParam, lParam, msg, hwnd) {
    global RestartVirtualDesktopAccessorProc
    DllCall(RestartVirtualDesktopAccessorProc, UInt, 0)
    return
}

; Active window by desktop tracking
activeWindowByDesktop := {}

; Function to switch to the specified desktop number
GoToDesktopNumber(num) {
    global GoToDesktopNumberProc, GetDesktopCountProc
    
    ; Check if desktop exists
    desktopCount := DllCall(GetDesktopCountProc, UInt)
    if (num >= desktopCount) {
        MsgBox, Desktop %num% does not exist. Only %desktopCount% virtual desktops are available.
        return
    }
    
    ; Change desktop
    result := DllCall(GoToDesktopNumberProc, UInt, num)
    
    ; Output for troubleshooting
    OutputDebug, Attempted to switch to desktop %num% with result: %result%
    
    return
}

MoveCurrentWindowToDesktop(num) {
    global MoveWindowToDesktopNumberProc, GoToDesktopNumberProc, GetDesktopCountProc
    
    ; Check if desktop exists
    desktopCount := DllCall(GetDesktopCountProc, UInt)
    if (num >= desktopCount) {
        MsgBox, Desktop %num% does not exist. Only %desktopCount% virtual desktops are available.
        return
    }
    
    WinGet, activeHwnd, ID, A
    DllCall(MoveWindowToDesktopNumberProc, UInt, activeHwnd, UInt, num)
    DllCall(GoToDesktopNumberProc, UInt, num)
}

; Hotkeys for ALT+Windows+Numpad 1-9 to switch to desktops 0-8 (Windows counts from 0)
!#Numpad1::GoToDesktopNumber(0)  ; Switch to desktop 1 (index 0)
!#Numpad2::GoToDesktopNumber(1)  ; Switch to desktop 2 (index 1)
!#Numpad3::GoToDesktopNumber(2)  ; Switch to desktop 3 (index 2)
!#Numpad4::GoToDesktopNumber(3)  ; Switch to desktop 4 (index 3)
!#Numpad5::GoToDesktopNumber(4)  ; Switch to desktop 5 (index 4)
!#Numpad6::GoToDesktopNumber(5)  ; Switch to desktop 6 (index 5)
!#Numpad7::GoToDesktopNumber(6)  ; Switch to desktop 7 (index 6)
!#Numpad8::GoToDesktopNumber(7)  ; Switch to desktop 8 (index 7)
!#Numpad9::GoToDesktopNumber(8)  ; Switch to desktop 9 (index 8)

; Windows+Alt+Shift+Numpad to move current window to desktop and follow it
!+#Numpad1::MoveCurrentWindowToDesktop(0)  ; Move to desktop 1 (index 0)
!+#Numpad2::MoveCurrentWindowToDesktop(1)  ; Move to desktop 2 (index 1)
!+#Numpad3::MoveCurrentWindowToDesktop(2)  ; Move to desktop 3 (index 2)
!+#Numpad4::MoveCurrentWindowToDesktop(3)  ; Move to desktop 4 (index 3)
!+#Numpad5::MoveCurrentWindowToDesktop(4)  ; Move to desktop 5 (index 4)
!+#Numpad6::MoveCurrentWindowToDesktop(5)  ; Move to desktop 6 (index 5)
!+#Numpad7::MoveCurrentWindowToDesktop(6)  ; Move to desktop 7 (index 6)
!+#Numpad8::MoveCurrentWindowToDesktop(7)  ; Move to desktop 8 (index 7)
!+#Numpad9::MoveCurrentWindowToDesktop(8)  ; Move to desktop 9 (index 8)

; Remove the Win+Number hotkeys to avoid conflicts with Windows default shortcuts

; Display current desktop number (useful for debugging)
!#Numpad0::
    global GetCurrentDesktopNumberProc, GetDesktopCountProc
    current := DllCall(GetCurrentDesktopNumberProc, UInt)
    count := DllCall(GetDesktopCountProc, UInt)
    MsgBox, Current desktop: %current% of %count% desktops (0-based index)`nPress Alt+Win+Numpad1-9 to switch desktops
return

; Test if desktop switching works
!#Space::
    global GetCurrentDesktopNumberProc
    current := DllCall(GetCurrentDesktopNumberProc, UInt)
    if (current < 0) {
        MsgBox, ERROR: Failed to get current desktop number.
    } else {
        MsgBox, SUCCESS: Current desktop is %current% (0-based index)
    }
return

; Display desktop count
!#c::
    global GetDesktopCountProc
    count := DllCall(GetDesktopCountProc, UInt)
    if (count <= 0) {
        MsgBox, ERROR: Failed to get desktop count or no virtual desktops exist.
    } else {
        MsgBox, SUCCESS: Total virtual desktops: %count%
    }
return

; Initialize desktop count display
desktopCount := DllCall(GetDesktopCountProc, UInt)
currentDesktop := DllCall(GetCurrentDesktopNumberProc, UInt)
MsgBox, 64, Virtual Desktop Switcher, Script loaded successfully!`n`nCurrent desktop: %currentDesktop%`nTotal desktops: %desktopCount%`n`nHotkeys:`n- Alt+Win+Numpad1-9: Switch desktops`n- Alt+Win+Shift+Numpad1-9: Move window to desktop`n- Alt+Win+Numpad0: Show current desktop`n- Alt+Win+Space: Test if switching works`n- Alt+Win+C: Show desktop count
return
