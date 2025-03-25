#Requires AutoHotkey v2.0

; -----------------------------------------------------------------------------
; Path to your custom or downloaded VirtualDesktopAccessor.dll
; (Ensure this matches your bitness: 64-bit DLL for 64-bit AHK, etc.)
; -----------------------------------------------------------------------------
VDA_PATH := A_ScriptDir . "\target\debug\VirtualDesktopAccessor.dll"

; Load the DLL
hVirtualDesktopAccessor := DllCall("LoadLibrary", "Str", VDA_PATH, "Ptr")

; Get function pointers for the functions you DO have
GetDesktopCountProc           := DllCall("GetProcAddress", "Ptr", hVirtualDesktopAccessor, "AStr", "GetDesktopCount", "Ptr")
GoToDesktopNumberProc         := DllCall("GetProcAddress", "Ptr", hVirtualDesktopAccessor, "AStr", "GoToDesktopNumber", "Ptr")
GetCurrentDesktopNumberProc   := DllCall("GetProcAddress", "Ptr", hVirtualDesktopAccessor, "AStr", "GetCurrentDesktopNumber", "Ptr")
MoveWindowToDesktopNumberProc := DllCall("GetProcAddress", "Ptr", hVirtualDesktopAccessor, "AStr", "MoveWindowToDesktopNumber", "Ptr")

; We are omitting RegisterPostMessageHook and UnregisterPostMessageHook,
; because your DLL does not export them and calling them triggers errors.

; -----------------------------------------------------------------------------
; Helper functions
; -----------------------------------------------------------------------------
GetDesktopCount() {
    global GetDesktopCountProc
    return DllCall(GetDesktopCountProc, "Int")
}

GetCurrentDesktopNumber() {
    global GetCurrentDesktopNumberProc
    return DllCall(GetCurrentDesktopNumberProc, "Int")
}

GoToDesktopNumber(num) {
    global GoToDesktopNumberProc
    DllCall(GoToDesktopNumberProc, "Int", num, "Int")
}

MoveWindowToDesktopNumber(hwnd, num) {
    global MoveWindowToDesktopNumberProc
    DllCall(MoveWindowToDesktopNumberProc, "Ptr", hwnd, "Int", num, "Int")
}

; -----------------------------------------------------------------------------
; MoveOrGotoDesktopNumber: 
; If LButton is held, move the active window + switch; otherwise, just switch.
; -----------------------------------------------------------------------------
MoveOrGotoDesktopNumber(num) {
    if (GetKeyState("LButton")) {
        activeHwnd := WinGetID("A")
        MoveWindowToDesktopNumber(activeHwnd, num)
    }
    GoToDesktopNumber(num)
}

; -----------------------------------------------------------------------------
; Optional: Next/Prev Desktop
; -----------------------------------------------------------------------------
GoToPrevDesktop() {
    current := GetCurrentDesktopNumber()
    last    := GetDesktopCount() - 1
    if (current = 0)
        MoveOrGotoDesktopNumber(last)
    else
        MoveOrGotoDesktopNumber(current - 1)
}

GoToNextDesktop() {
    current := GetCurrentDesktopNumber()
    last    := GetDesktopCount() - 1
    if (current = last)
        MoveOrGotoDesktopNumber(0)
    else
        MoveOrGotoDesktopNumber(current + 1)
}

; -----------------------------------------------------------------------------
; Hotkeys: Win+Numpad1..9 -> Switch to desktop #0..8
; (0-based indexing from the DLL)
; -----------------------------------------------------------------------------
#Numpad1::MoveOrGotoDesktopNumber(0)
#Numpad2::MoveOrGotoDesktopNumber(1)
#Numpad3::MoveOrGotoDesktopNumber(2)
#Numpad4::MoveOrGotoDesktopNumber(3)
#Numpad5::MoveOrGotoDesktopNumber(4)
#Numpad6::MoveOrGotoDesktopNumber(5)
#Numpad7::MoveOrGotoDesktopNumber(6)
#Numpad8::MoveOrGotoDesktopNumber(7)
#Numpad9::MoveOrGotoDesktopNumber(8)

; -----------------------------------------------------------------------------
; Optional: Win+PgUp / Win+PgDn -> Prev/Next desktop
; -----------------------------------------------------------------------------
#PgUp::GoToPrevDesktop()
#PgDn::GoToNextDesktop()
