#!/usr/bin/perl

use DBI;
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
    $QUERY=&trim($FORM{query});
    $SERVER = &trim($FORM{selectedServer});
    $RECNO = &trim($FORM{RecNos});
    $det_QUERY=&determineSelect($QUERY);
    if ($det_QUERY eq "select" and ($RECNO ne "ALL")){
      @ar = split (/ /, $QUERY);
      $len= @ar;
      $rem="";
      for ($i=1;$i<$len;$i++){$rem=$rem.$ar[$i]." ";}
      $QUERY = "select top $RECNO ".$rem;
    }  
    else{}
    $QUERY=~ s/EQUALLTO/=/g;
    $QUERY=~ s/PERCENTAGE/\%/g;
      


    print "Content-type: text/html\n\n" ;
    print "<head>";
    print "<SCRIPT language=\"JavaScript\" SRC=\"jsGG.js\"></SCRIPT>";
    print "<title>SI-UI Tool</title></head>";
    $USER     = `grep "username" config.txt |cut -d'=' -f2`;
    chomp($USER);
    $PASSWORD = `grep "password" config.txt |cut -d'=' -f2`;
    chomp($PASSWORD);
    print "<body><form method=\"POST\"><font color=\"#336699\"><b>RESULT</b></font><font color=\"#339966\"><br>";
    print "<table><tr><td valign=\"top\">";
    &runQuery();
    print "</td></tr>";
    print "<br></form></body></html>";


###############################################################################
# Subroutine: selectColumns
# purpose   : selects the columns from a table
###############################################################################
sub runQuery(){

$dsn = "dbi:Sybase:server=$SERVER;database=$DBNAME";
$dbha = DBI->connect($dsn, $USER, $PASSWORD);


my $sth = $dbha->prepare( $QUERY );
unless ($sth) {
        print  "Could not prepare dbquery: " . $QUERY ;
  }

unless ( $sth->execute ) {
 
    @ar1 = split(/=/,$sth->errstr);
    @ar2= split(/ /,$ar1[1]);
    $err_code= $ar2[0];
    print "<table border=\"1\"><tr><td width=\"20%\"> Error code </td> <td width=\"80%\">$err_code</td></tr>";
    print "<tr><td width=\"20%\"> Query </td> <td width=\"80%\">$QUERY</td></tr>";
    print "<tr><td width=\"20%\"> Error Message </td> <td width=\"80%\">$ar1[6]</td></tr></table>";
    $sth->finish;
  }
if ($det_QUERY eq "select"){
	$nf = $sth->{NUM_OF_FIELDS};
	print "<table border=\"1\">";
	    print "<tr>";
	    for ($i=0;$i<$nf;$i++){
	       print "<th>$sth->{NAME}[$i] </th>";
	    }
	    print "</tr>";
	while ( my $ary_ref = $sth->fetchrow_arrayref() ) {
	        print "<tr>";
	    for ($i=0;$i<$nf;$i++){
	       print "<td>$ary_ref->[$i] </td>";
	    }
	      print "</tr>";
	}
	print "</table>";
}
else{
     print "Query executed successfully.";
}



$dbha->disconnect();
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


#################################################################################
# Routine: determineSelect
# Description: determine whether select/insert etc....
#################################################################################

sub determineSelect($)
{
 $q=shift;
 $q=lc($q);
 @ar = split(/ /,$q);
 if ($ar[0] eq "select"){
     return "select";
 }
 else{
      return "non-select";
 }
}
