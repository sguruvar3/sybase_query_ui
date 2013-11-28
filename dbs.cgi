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
    $SERVER = &trim($FORM{selectedServer});

print "Content-type: text/html\n\n" ;
print "<head>";
print "<SCRIPT language=\"JavaScript\" SRC=\"jsGG.js\"></SCRIPT>";
print "<title>SI-UI Tool</title></head>";
$USER     = `grep "username" config.txt |cut -d'=' -f2`;
chomp($USER);
$PASSWORD = `grep "password" config.txt |cut -d'=' -f2`;
chomp($PASSWORD);

print "<body><form method=\"POST\"><font color=\"#336699\"><b>Databases</b></font><font color=\"#339966\"><br>Select to see Tables</font>";
print "<table><tr><td valign=\"top\">";
&selectDatabases();

print "</td></tr>";
print "<input type=\"hidden\" name=\"selectedDB\">";
print "<input type=\"text\" name=\"selectedServer\" value=\"$SERVER\">";
print "</form></body></html>";
###############################################################################
# Subroutine: selectDatabases
# purpose   : selects the databases present in a server
###############################################################################
sub selectDatabases(){

$cmd="date +%Y%m%d%H%M%S";
 $DATE=`$cmd`;
 chomp($DATE);

$Ifname="/tmp/gg1"."_".$DATE;
$Ofname="/tmp/gg.dat"."_".$DATE;

open (FP,">$Ifname");
print FP "select name from sysdatabases\ngo";
close(FP);

$cmd.="isql -S $SERVER -U $USER -P $PASSWORD < $Ifname > $Ofname";
$res=`$cmd`;

open (FP, $Ofname);
@ar=<FP>;
$len=@ar;
close(FP);

$size=$len-4;
$size=($size>16)?16:$size;

print "<select name=\"dbs\" size=\"$size\" onChange=\"selDB()\">";
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
$cmd="rm $Ofname; rm $Ifname";
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


