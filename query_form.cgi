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
    $TABLENAME=&trim($FORM{selectedTable});
    $FIELDS = &trim($FORM{selectedField});
    $SERVER = &trim($FORM{selectedServer});
      if (($FIELDS eq "") and ($TABLENAME eq "")){ $query ="";}
      else {   $query = "select $FIELDS from $TABLENAME"; }
    print "Content-type: text/html\n\n" ;
    print "<head>";
    print "<SCRIPT language=\"JavaScript\" SRC=\"jsGG.js\"></SCRIPT>";
    print "<title>SI-UI Tool</title></head>";
    $USER     = `grep "username" config.txt |cut -d'=' -f2`;
    chomp($USER);
    $PASSWORD = `grep "password" config.txt |cut -d'=' -f2`;
    chomp($PASSWORD);
    
    print "<body><form method=\"POST\"><font color=\"#336699\"><b>Query</b></font><font color=\"#339966\"><br>Edit the way you want!!! </font><br>";
    print "<table><tr><td valign=\"top\">";
    print "</td></tr>";
    print "<textarea rows=\"6\" cols=\"60\" name=\"query\">$query</textarea>";
    print "<input type=\"hidden\" name=\"selectedDB\" value=\"$DBNAME\"/>";
    print "<input type=\"hidden\" name=\"qModified\"/>";
    print "<input type=\"hidden\" name=\"selectedServer\" value=\"$SERVER\"/><br>";
    print "<table><tr><td width=\"20%\"></td><td width=\"20%\"></td>";
    print "<td width=\"20%\"><font color=\"#336699\" size=\"-1\">Row Count</font></td><td width=\"20%\"></td><td width=\"20%\"></td></tr>";
    print "<tr width=\"100%\"><td width=\"20%\"></td><td width=\"20%\"></td><td width=\"20%\"><select name=\"RecNos\" size=\"1\">";
    print "<option value=\"1\">1</option>";
    print "<option value=\"5\">5</option>";
    print "<option value=\"10\" selected=\"selected\">10</option>";
    print "<option value=\"50\">50</option>";
    print "<option value=\"100\">100</option>";
    print "<option value=\"500\">500</option>";
    print "<option value=\"1000\">1000</option>";
    print "<option value=\"ALL\">ALL</option>";
    print "</select></td>";
    print "<td width=\"20%\"><input type=\"button\" name=\"b1\" value=\"Run\" onclick=\"runQuery(\'$DBNAME\',\'$TABLENAME\',\'$FIELDS\')\"></td>";
    print "<td width=\"20%\"><input type=\"button\" name=\"reset\" value=\"Clear\" onclick=\"clean()\"></td></tr></table></form></body></html>";
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

