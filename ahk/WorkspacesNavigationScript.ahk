#Requires AutoHotkey v2.0

; ---------------------------------------------------------------------------
; AHK v2 Script
; Requires AutoHotkey v2.x and VirtualDesktopAccessor.dll in the same folder.
; ---------------------------------------------------------------------------

; Check if the DLL exists
if !FileExist(A_ScriptDir "\VirtualDesktopAccessor.dll")
{
    MsgBox("VirtualDesktopAccessor.dll not found.`n" 
          . "Download it from: https://github.com/Ciantic/VirtualDesktopAccessor" 
          . " and place it in the script directory.",
          "Error", 48)
    ExitApp()
}

; Function: GoToDesktop
; Usage:    GoToDesktop(desktopNumber)
; Desc:     Switches to the given 1-based desktopNumber using VirtualDesktopAccessor
GoToDesktop(desktopNumber) {
    desktopCount := DllCall("VirtualDesktopAccessor.dll\GetDesktopCount", "UInt")
    if (desktopNumber > desktopCount) {
        return false
    }
    ; Switch to the requested desktop
    ; Note: the DLL uses 0-based index, so subtract 1
    DllCall("VirtualDesktopAccessor.dll\GoToDesktopNumber", "UInt", desktopNumber - 1)
    return true
}

; --- Hotkeys for Win + Numpad1..9 ---
#HotIf true
#Numpad1:: {
    if (!GoToDesktop(1)) {
        MsgBox("Virtual Desktop 1 does not exist.", "Info", 48)
    }
}

#Numpad2:: {
    if (!GoToDesktop(2)) {
        MsgBox("Virtual Desktop 2 does not exist.", "Info", 48)
    }
}

#Numpad3:: {
    if (!GoToDesktop(3)) {
        MsgBox("Virtual Desktop 3 does not exist.", "Info", 48)
    }
}

#Numpad4:: {
    if (!GoToDesktop(4)) {
        MsgBox("Virtual Desktop 4 does not exist.", "Info", 48)
    }
}

#Numpad5:: {
    if (!GoToDesktop(5)) {
        MsgBox("Virtual Desktop 5 does not exist.", "Info", 48)
    }
}

#Numpad6:: {
    if (!GoToDesktop(6)) {
        MsgBox("Virtual Desktop 6 does not exist.", "Info", 48)
    }
}

#Numpad7:: {
    if (!GoToDesktop(7)) {
        MsgBox("Virtual Desktop 7 does not exist.", "Info", 48)
    }
}

#Numpad8:: {
    if (!GoToDesktop(8)) {
        MsgBox("Virtual Desktop 8 does not exist.", "Info", 48)
    }
}

#Numpad9:: {
    if (!GoToDesktop(9)) {
        MsgBox("Virtual Desktop 9 does not exist.", "Info", 48)
    }
}
