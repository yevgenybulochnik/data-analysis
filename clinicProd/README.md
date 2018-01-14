# Clinic Productivity Report
This report is a prototype/proof of concept. The idea is to generate an automated PDF report using python pandas for data analysis and weazyprint to generate a PDF. HTML templates populated by python are fed to weazyprint to generate a formated PDF. The report shows the total number of provider encounters broken out by date, encounter type and clinic over a two week pay period. Further, encounters can be displayed by their raw counts or by an adjusted weight. For example, a new patient encounter will count as 1, however, the encounter weight, is 3 so it will be depicted as 1(3).   
## Input Data Schema 
```
"Date","Dept/Loc","Type","Prov/Res"
"11/29/2017","ONB COAG [1234]","AC RETURN [5678]","BULOCHNIK, YEVGENY"
"12/08/2017","OMW ACC [4321]","AC PHONE [8765]","BULOCHNIK, YEVGENY"
"12/06/2017","OPHAC [1234]","AC RTRN PT [5678]","BULOCHNIK, YEVGENY"
```
