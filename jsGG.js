query="";
function setServer(dbserver){
parent.left_frame.location="http://localhost:8009/dbs.cgi?selectedServer="+dbserver;
}

function selDB()
{
box=document.forms[0].dbs;
selVal=box.options[box.selectedIndex].value;
document.forms[0].selectedDB.value=selVal;
parent.mid_frame.location="http://localhost:8009/tables.cgi?selectedDB="+selVal+"&selectedServer="+document.forms[0].selectedServer.value;
}

function selTable(selDB)
{
box=document.forms[0].tbls;
selVal=box.options[box.selectedIndex].value;
document.forms[0].selectedTable.value=selVal;
parent.right_frame.location="http://localhost:8009/columns.cgi?selectedDB="+selDB+"&selectedTable="+selVal+"&selectedServer="+document.forms[0].selectedServer.value;
}

function selFields(selDB,selTable)
{
 box=document.forms[0].cls;
 query="";

 selVal=box.options[box.selectedIndex].value;
 query = query + trim(selVal) + ", ";
 document.forms[0].selectedField.value+=query;
 query_str=delDuplicatesAndFormQuery(document.forms[0].selectedField.value);
 parent.query_frame.location="http://localhost:8009/query_form.cgi?selectedDB="+selDB+"&selectedTable="+selTable+"&selectedField="+query_str+"&selectedServer="+document.forms[0].selectedServer.value;
}

function runQuery(selDB,selTable,selFields){
 query=document.forms[0].query.value;
  var q =""; /*Need to change the code for queries other than Select */
/* if (document.forms[0].RecNos.value != "ALL") {
         q ="select top "+document.forms[0].RecNos.value+" "+selFields+" FROM "+selTable;
 }
 else{
         q ="select "+selFileds+" FROM "+selTable;
 }  
 
 document.forms[0].qModified.value=modifyQuery(q);*/
 var mq=modifyQuery(query); 
  mq=encodeQuery(mq); 
 parent.runner_frame.location="http://localhost:8009/query_run.cgi?selectedDB="+selDB+"&query="+mq+"&selectedServer="+document.forms[0].selectedServer.value+"&RecNos="+document.forms[0].RecNos.value;
}
function clean(){
document.forms[0].query.value="";
top.frames[4].document.forms[0].selectedField.value="";
}

function trim(stri) {
	return stri.replace(/^\s+|\s+$/g,"");
}

function delDuplicatesAndFormQuery(val){
     var myvals = new Array();
     myvals = val.split(",");
     myvals.sort();
     query_str="";
     var newAr = new Array();
     i=0;
     while (i<myvals.length){
           val = myvals[i];
           while (val == myvals[(i+1)]) {
                   i+=1;
           }
           newAr.push(myvals[i]);
           i+=1;
     } 
     
     for (i=1; i<newAr.length-1; i++){
         query_str+=newAr[i]+", ";
     }
         query_str+=newAr[i];
     return query_str;
}

function modifyQuery(query){
     return query.replace(/=/g,"EQUALLTO");
}
function encodeQuery(query){
     return query.replace(/%/g,"PERCENTAGE");
}

