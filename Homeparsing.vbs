Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c Homeparsing.bat"
oShell.Run strArgs, 0, false