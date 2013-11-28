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
    $SERVER = &trim($FORM{selectedServer});
    $DBNAME = &trim($FORM{selectedDB});
    $TBLNAME = &trim($FORM{selectedTable});

#    $QUERY= "select # = c.colid, Field_Name =c.name,  Type = t.name, Sybase_Type= c.type, Length= c.length,  Scale = c.scale,  Precision = c.prec, Nullable  = t.allownulls from $DBNAME.dbo.syscolumns c, $DBNAME.dbo.systypes t where  c.id = object_id('$DBNAME..$TBLNAME') and c.usertype *= t.usertype order by c.colid";
    $QUERY= "select # = c.colid,  Field_Name =c.name,  Type = t.name,  Sybase_Type= c.type, Length= c.length, Scale = c.scale, Precision = c.prec, Nullable  = case when c.status & 8 = 8 then \"1\" else \"0\" end from $DBNAME.dbo.syscolumns c, $DBNAME.dbo.systypes t where   c.id =object_id('$DBNAME..$TBLNAME') and  c.usertype *= t.usertype order by c.colid";

    print "Content-type: text/html\n\n" ;
    print "<head>";
    print "<SCRIPT language=\"JavaScript\" SRC=\"jsGG.js\"></SCRIPT>";
    print "<title>SI-UI Tool</title></head>";
    $USER     = `grep "username" config.txt |cut -d'=' -f2`;
    chomp($USER);
    $PASSWORD = `grep "password" config.txt |cut -d'=' -f2`;
    chomp($PASSWORD);
    print "<body><form method=\"GET\" action=\"http:\/\/localhost:8009\/sp_help.cgi\"><font color=\"#336699\"><b>sp_help</b></font><br>";
    print "<table>";
    print "<tr><td>Server <input type=\"text\" name=\"selectedServer\" value=\"$SERVER\"><td></tr>";
    print "<tr><td>Database  <input type=\"text\" name=\"selectedDB\" value=\"$DBNAME\"><td>";
    print "<td>Table <input type=\"text\" name=\"selectedTable\" value=\"$TBLNAME\"><td>";
    print "<td> <input type=\"submit\" name=\"submit\" value=\"GO\"><td></tr>";
    print "</table>";
    print "<br/><font color=\"#339966\"><b>Table Info </b> (Special thanks to Dillibabu for his nullable column \"discovery\")</font><br/><br/>";
    &runQuery($QUERY);
    print "<br/><font color=\"#339966\"><b>Index(es) Info </b></font> <br/><br/>";
    $QUERY="sp_helpindex $TBLNAME"; 
    &runIndexQuery($QUERY);
    print "</form></body></html>";


###############################################################################
# Subroutine: selectColumns
# purpose   : selects the columns from a table
###############################################################################
sub runQuery{
$QUERY1=shift;
%sybase_type=(109,"floatn",62,"float",111,"datetimn",61,"datetime",59,"real",108,"numericn",63,"numeric",106,"decimaln",55,"decimal",110,"moneyn",60, "money",122,"smallmoney",58,"smalldatetime",38,"intn",56,"int",52,"smallint",48,"tinyint",50,"bit",155,"univarchar",135,"unichar",39,"varchar", 47,"char", 37,"timestamp", 45,"binary",35,"text",34,"image",123,"date", 124,"time",160,"daten",29,"timen");

$dsn = "dbi:Sybase:server=$SERVER;database=$DBNAME";
$dbha = DBI->connect($dsn, $USER, $PASSWORD);


my $sth = $dbha->prepare( $QUERY1 );
unless ($sth) {
        print  "Could not prepare dbquery: " . $QUERY1 ;
  }

unless ( $sth->execute ) {
    @ar1 = split(/=/,$sth->errstr);
    @ar2= split(/ /,$ar1[1]);
    $err_code= $ar2[0];
    print "<table border=\"1\"><tr><td width=\"20%\"> Error code </td> <td width=\"80%\">$err_code</td></tr>";
    print "<tr><td width=\"20%\"> Query </td> <td width=\"80%\">$QUERY1</td></tr>";
    print "<tr><td width=\"20%\"> Error Message </td> <td width=\"80%\">$ar1[6]</td></tr></table>";
    $sth->finish;
  }

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
        if ($i == 3)
           {  print "<td>$sybase_type{$ary_ref->[$i]} </td>";}
        elsif ($i == 7)
           {  if ($ary_ref->[$i] == 1) {print "<td>Yes</td>";}
              else {print "<td>No</td>";}
          }
        else 
           {  print "<td>$ary_ref->[$i] </td>"; }
        
    }
      print "</tr>";
}
print "</table>";
$sth->finish();
$dbha->disconnect();
}

###############################################################################
# Subroutine: selectColumns
# purpose   : selects the columns from a table
###############################################################################
sub runIndexQuery{
$QUERY1=shift;
$dsn1 = "dbi:Sybase:server=$SERVER;database=$DBNAME";
$dbha1 = DBI->connect($dsn1, $USER, $PASSWORD);


my $sth1 = $dbha1->prepare( $QUERY1 );
unless ($sth1) {
        print  "Could not prepare dbquery: " . $QUERY1 ;
  }

unless ( $sth1->execute ) {

    @ar1 = split(/=/,$sth1->errstr);
    @ar2= split(/ /,$ar1[1]);
    $err_code= $ar2[0];
    print "<table border=\"1\"><tr><td width=\"20%\"> Error code </td> <td width=\"80%\">$err_code</td></tr>";
    print "<tr><td width=\"20%\"> Query </td> <td width=\"80%\">$QUERY1</td></tr>";
    print "<tr><td width=\"20%\"> Error Message </td> <td width=\"80%\">$ar1[6]</td></tr></table>";
    $sth1->finish;
  }

$nf = $sth1->{NUM_OF_FIELDS};
print "<table border=\"1\">";
    print "<tr>";
    for ($i=0;$i<3;$i++){
       print "<th>$sth1->{NAME}[$i] </th>";
    }
    print "</tr>";
while ( my $ary_ref = $sth1->fetchrow_arrayref() ) {
        print "<tr>";
    for ($i=0;$i<3;$i++){
       print "<td>$ary_ref->[$i] </td>";
    }
      print "</tr>";
}
print "</table>";


$sth1->finish();
$dbha1->disconnect();
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


