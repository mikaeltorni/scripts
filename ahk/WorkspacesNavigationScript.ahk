; VirtualDesktopSwitcher.ahk
; This script uses VirtualDesktopAccessor.dll to switch directly to virtual desktops 1-9 using Win + Numpad keys.
; Download VirtualDesktopAccessor.dll from:
;   https://github.com/Ciantic/VirtualDesktopAccessor
; and place it in the same directory as this script.

; Check for VirtualDesktopAccessor.dll
if !FileExist("VirtualDesktopAccessor.dll")
{
    MsgBox, 16, Error, VirtualDesktopAccessor.dll not found.`nDownload it from https://github.com/Ciantic/VirtualDesktopAccessor and place it in the script directory.
    ExitApp
}

; Function to switch to a specific virtual desktop.
; desktopNumber is 1-based (1 means first desktop)
GoToDesktop(desktopNumber)
{
    ; Get the total number of virtual desktops
    desktopCount := DllCall("VirtualDesktopAccessor.dll\GetDesktopCount", "UInt")
    if (desktopNumber > desktopCount)
    {
        return false
    }
    ; Switch to the desktop (note: the DLL uses 0-based indexing)
    DllCall("VirtualDesktopAccessor.dll\GoToDesktopNumber", "UInt", desktopNumber - 1)
    return true
}

; Hotkeys for switching virtual desktops 1-9 using Win + Numpad keys
#Numpad1:: if (!GoToDesktop(1)) MsgBox, Virtual Desktop 1 does not exist.
#Numpad2:: if (!GoToDesktop(2)) MsgBox, Virtual Desktop 2 does not exist.
#Numpad3:: if (!GoToDesktop(3)) MsgBox, Virtual Desktop 3 does not exist.
#Numpad4:: if (!GoToDesktop(4)) MsgBox, Virtual Desktop 4 does not exist.
#Numpad5:: if (!GoToDesktop(5)) MsgBox, Virtual Desktop 5 does not exist.
#Numpad6:: if (!GoToDesktop(6)) MsgBox, Virtual Desktop 6 does not exist.
#Numpad7:: if (!GoToDesktop(7)) MsgBox, Virtual Desktop 7 does not exist.
#Numpad8:: if (!GoToDesktop(8)) MsgBox, Virtual Desktop 8 does not exist.
#Numpad9:: if (!GoToDesktop(9)) MsgBox, Virtual Desktop 9 does not exist.
