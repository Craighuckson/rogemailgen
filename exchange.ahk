Inputbox,tn,Enter ticket number
Runwait,python -m ahkexchangetest.py %tn%
FileRead, file, msg.txt
if (file != "")
	msgbox % file
else
	msgbox % "Failed"
