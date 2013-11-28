#!/usr/bin/perl
local ($buffer, @pairs, $pair, $name, $value, %FORM);
    $ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
    if ($ENV{'REQUEST_METHOD'} eq "POST")
    {
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    }else {
	$buffer = $ENV{'QUERY_STRING'};
    }
    # Split information into name/value pairs
    @pairs = split(/&/, $buffer);
    foreach $pair (@pairs)
    {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%(..)/pack("C", hex($1))/eg;
	$FORM{$name} = $value;
    }
    $DBNAME = &trim($FORM{selectedDB});
    $SERVER = &trim($FORM{selectedServer});
    if ($SERVER eq ""){$SERVER   = "PSITDB1M25";}
    if ($DBNAME eq ""){$DBNAME = "AuthenDB";}

print "Content-type: text/html\n\n" ;
print "<head>";
print "<SCRIPT language=\"JavaScript\" SRC=\"jsGG.js\"></SCRIPT>";
print "<title>SI-UI Tool</title>";
print "<style type=\"text/css\">";
print "#siva input.b1{";
print "font-family: helvetica, verdana, arial;";
print "font-size: 10pt;";
print "color:#0000FF;";
print "border:#fff 0px solid;";
print "text-decoration: underline;";
print "cursor: hand;";
print "Background-Color:#FFFFFF;";
print "}</style>";
print "</head>";
$USER     = `grep "username" config.txt |cut -d'=' -f2`;
chomp($USER);
$PASSWORD = `grep "password" config.txt |cut -d'=' -f2`;
chomp($PASSWORD);

$url="'/sp_help.cgi?selectedServer='\+document.forms[0].selectedServer.value\+'\&selectedDB='\+document.forms[0].selectedDB.value\+'\&selectedTable='\+document.forms[0].selectedTable.value";
print "<body><form method=\"POST\"><table><tr><td><font color=\"#336699\"><b>Tables</b></font></td>";
print "<td><div id=\"siva\"><input class=\"b1\" type=\"button\" name=\"b2\" value=\"sp_help\" onClick=\"window.open($url,'mywindow','width=600,height=500,scrollbars=yes',resizable=1)\"></input></div></td></tr>";
print "<tr><td colspan=2><font color=\"#339966\">Select to see Columns</font></td></tr></table>";
print "<table><tr><td valign=\"top\">";
&selectTables();

print "</td></tr></table>";
print "<input type=\"hidden\" name=\"selectedServer\" value=\"$SERVER\">";
print "<input type=\"hidden\" name=\"selectedDB\" value=\"$DBNAME\">";
print "<input type=\"hidden\" name=\"selectedTable\">";
#print "<br/><div id=\"siva\"><input class=\"b1\" type=\"button\" name=\"b2\" value=\"sp_help\" onClick=\"window.open($url,'mywindow','width=600,height=500,scrollbars=yes',resizable=1)\"></input>";
print "</form>";
print "</body></html>";
###############################################################################
# Subroutine: selectTables
# purpose   : selects the tables present in a DB
###############################################################################
sub selectTables(){
$cmd="date +%Y%m%d%H%M%S";
 $DATE=`$cmd`;
 chomp($DATE);

$Ifname="/tmp/tgg1"."_".$DATE;
$Ofname="/tmp/tgg.dat"."_".$DATE;

open (FP,">$Ifname");
print FP "select name from sysobjects where type='U'\ngo";
close(FP);

$cmd.="isql -S $SERVER -U $USER -P $PASSWORD -D $DBNAME < $Ifname > $Ofname";
$res=`$cmd`;

open (FP, $Ofname);
@ar=<FP>;
$len=@ar;
close(FP);

$size=$len-4;
$size=($size>16)?16:$size;
if ($size == 1){ $size=3;}

print "<select name=\"tbls\" size=\"$size\" onchange=\"selTable(\'$DBNAME\')\">";

$l=$ar[0];
  $i=1;
 $s=($l =~ m/^----/)?"Yes":"No";
 while ($s eq "No"){
   $l=$ar[$i];
   chomp($l);
   $s=($l =~ m/^ ----/)?"Yes":"No";
   $i++;
 }
while($i<($len-2)){
   $l=$ar[$i];
   chomp($l);
   $i++;
   print "<option value=\"$l\">$l</option> <br>";
}
print "</select>";
$cmd="rm $Ifname;rm $Ofname";
$res=`$cmd`;
}
#################################################################################
# Routine: trim
# Description: trims the whitespaces
#################################################################################

sub trim($)
{
        my $string = shift;
        $string =~ s/^\s+//;
        $string =~ s/\s+$//;
        return $string;
}

