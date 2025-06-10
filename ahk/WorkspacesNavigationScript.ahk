; Globals
DesktopCount = 2 ; Windows starts with 2 desktops at boot
CurrentDesktop = 1 ; Desktop count is 1-indexed (Microsoft numbers them this way)
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
;
; This function sends the active window to the desktop number provided and follows it.
; NOTE: This requires VD.ahk library from https://github.com/FuPeiJiang/VD.ahk
; Download VD.ahk and place it in the same folder as this script or in your AutoHotkey library folder
;
sendWindowToDesktopByNumber(targetDesktop)
{
    ; Check if VD.ahk is included
    if (!IsObject(VD)) {
        MsgBox, VD.ahk library is required!`nPlease download it from https://github.com/FuPeiJiang/VD.ahk and place it in the same folder as this script.
        return
    }
    
    ; Move active window ("A") to target desktop and follow it
    VD.MoveWindowToDesktopNum("A", targetDesktop).follow()
    
    OutputDebug, [send window] Window moved to desktop %targetDesktop%
}
; Main
SetKeyDelay, 10
mapDesktopsFromRegistry()
OutputDebug, [loading] desktops: %DesktopCount% current: %CurrentDesktop%

; User config!
; This section binds the key combo to the switch/create/delete actions
#sc056::switchDesktopByNumber(1)  ; Win+< (sc056) for Desktop 1 (Nordic layout)
#z::switchDesktopByNumber(2)      ; Win+Z for Desktop 2
#c::switchDesktopByNumber(3)      ; Win+C for Desktop 3
#a::switchDesktopByNumber(4)      ; Win+A for Desktop 4
#s::switchDesktopByNumber(5)      ; Win+S for Desktop 5
#f::switchDesktopByNumber(6)      ; Win+F for Desktop 6

; Send active window to desktop
; NOTE: Requires VD.ahk library from https://github.com/FuPeiJiang/VD.ahk
; These hotkeys will only work after you download and include the library
#Include %A_ScriptDir%\VD.ahk  ; Add this line to include VD.ahk if it's in the same folder

^#z::sendWindowToDesktopByNumber(1)  ; Ctrl+Win+Z for sending window to Desktop 1
^#x::sendWindowToDesktopByNumber(2)  ; Ctrl+Win+X for sending window to Desktop 2
^#c::sendWindowToDesktopByNumber(3)  ; Ctrl+Win+C for sending window to Desktop 3
^#v::sendWindowToDesktopByNumber(4)  ; Ctrl+Win+V for sending window to Desktop 4
^#a::sendWindowToDesktopByNumber(5)  ; Ctrl+Win+A for sending window to Desktop 5
^#s::sendWindowToDesktopByNumber(6)  ; Ctrl+Win+S for sending window to Desktop 6