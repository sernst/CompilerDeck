; installer.nsi
; (C)2013
; Scott Ernst

!include "MUI2.nsh"
!include "x64.nsh"

;--------------------------------
;General

	; The name of the installer
	Name "CompilerDeck"
	OutFile "CompilerDeck_Installer.exe"

	; The default installation directory
	InstallDir "$PROGRAMFILES64\CompilerDeck"

	; Registry key to check for directory (so if you install again, it will
	; overwrite the old one automatically)
	InstallDirRegKey HKLM "Software\compilerDeck_CompilerDeckApplication" "Install_Dir"

	; Request application privileges for Windows Vista+
	RequestExecutionLevel admin

;--------------------------------
;Interface Settings

	!define MUI_ABORTWARNING

	;!define MUI_COMPONENTSPAGE_SMALLDESC ;No value
	!define MUI_INSTFILESPAGE_COLORS "FFFFFF 000000" ;Two colors

;--------------------------------
; Pages

	!insertmacro MUI_PAGE_COMPONENTS
	!insertmacro MUI_PAGE_DIRECTORY
	!insertmacro MUI_PAGE_INSTFILES

	!insertmacro MUI_UNPAGE_CONFIRM
	!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

	!insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections
Section "CompilerDeck (required)"

  SectionIn RO

  ; Install resource files
  SetOutPath "$LOCALAPPDATA\compilerDeck\CompilerDeckApplication\resources"
  File /r "resources\*"

  ; Install application files and dependencies
  SetOutPath "$INSTDIR\CompilerDeck"
  File /r "dist\*"

  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\compilerDeck_CompilerDeckApplication "Install_Dir" "$INSTDIR"

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\compilerDeck_CompilerDeckApplication" "DisplayName" "CompilerDeck"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\compilerDeck_CompilerDeckApplication" "UninstallString" '"$INSTDIR\CompilerDeck\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\compilerDeck_CompilerDeckApplication" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\compilerDeck_CompilerDeckApplication" "NoRepair" 1
  WriteUninstaller "CompilerDeck\uninstall.exe"

SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcut"

  CreateDirectory "$SMPROGRAMS\CompilerDeck"
  CreateShortCut "$SMPROGRAMS\CompilerDeck\CompilerDeck.lnk" "$INSTDIR\CompilerDeck\CompilerDeck.exe" "" "$INSTDIR\CompilerDeck\CompilerDeck.exe" 0
  CreateShortCut "$SMPROGRAMS\CompilerDeck\Uninstall.lnk" "$INSTDIR\CompilerDeck\uninstall.exe" "" "$INSTDIR\CompilerDeck\uninstall.exe" 0

SectionEnd

; Optional section (can be disabled by the user)
Section "Desktop Shortcut"

	CreateShortcut "$DESKTOP\CompilerDeck.lnk" "$INSTDIR\CompilerDeck\CompilerDeck.exe" "" "$INSTDIR\CompilerDeck\CompilerDeck.exe" 0

SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"

  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CompilerDeck"
  DeleteRegKey HKLM SOFTWARE\compilerDeck_CompilerDeckApplication

  ; Remove files and uninstaller
  Delete "$INSTDIR\*.*"
  Delete "$LOCALAPPDATA\compilerDeck\CompilerDeckApplication\resources\*.*"

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\CompilerDeck\*.*"

  ; Remove desktop shortcut if it exists
  Delete "$DESKTOP\CompilerDeck.lnk"

  ; Remove directories used
  RMDir /r "$INSTDIR"

  RMDir /r "$LOCALAPPDATA\compilerDeck\CompilerDeckApplication\resources"

  RMDir "$SMPROGRAMS\CompilerDeck"

SectionEnd
