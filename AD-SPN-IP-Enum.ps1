$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = ($domainObj.PdcRoleOwner).Name
$SearchString = "LDAP://"
$SearchString += $PDC + "/"
$DistinguishedName = "DC=$($domainObj.Name.Replace('.', ',DC='))"
$SearchString += $DistinguishedName
$Searcher = New-Object System.DirectoryServices.DirectorySearcher([ADSI]$SearchString)
$objDomain = New-Object System.DirectoryServices.DirectoryEntry($SearchString, "INSERT-DOMAIN-User", "PASSWORD")
$Searcher.SearchRoot = $objDomain
$Searcher.filter="(serviceprincipalname=*)"
$Result = $Searcher.FindAll()
Foreach($obj in $Result)
{
 $outputObject= "" | Select samaccountname, ipaddress, serviceprincipalname
 
 Foreach($prop in $obj.Properties)
 {
  $outputObject.samaccountname=$prop.samaccountname
  $SPN_initial=$prop.serviceprincipalname
  $SPN = $SPN_initial.split("/")[1].split(":")[0]
  $outputObject.serviceprincipalname=$SPN
  if ($SPN -Like "*.com")
  {
  	$outputObject.ipaddress= nslookup $SPN | Select-String Address | Select-Object -Unique 
  }
  $outputObject
 }
}
