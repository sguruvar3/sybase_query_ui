sybase_query_ui
===============
Sybase isql based - brower UI

i.e., Browser based database and table querying tool for Sybase written in Perl-CGI.

This works across database servers, tables, views, constraints and columns in a “point-and-click” fashion.

Features
========

- Hop between database servers is a single mouse click

- Display is more readable compared to “isql”, which is a command line tool to access databases

- Forming a query just involves couple of mouse clicks and no keyboard touch is required

- Auto login within the network

- Adding a new database server entry is just one line config file change

- Reusable in any other RDBMS systems with less/no configuration changes

- Any developer can benefit from this tool and this can help in reduce the development time.

- This tool transforms the system level database operations to application level user clicks.

- By using this tool, database operations will no longer be command line operations. 

How To INSTALL
==============
    - Copy the files into your Apache (either by check-out or by downloading the zip verion) 

    - This one intends to run on localhost:8009, if your host/port varies, just replace the same 

    - In left.cgi, just configure your available servers 

    - In config.txt, just provide your username and password 

    - Thats it... You are ready to go.... 

Not Working??
=============
Possible reasons could be:

    - Check your httpd.conf file to see the directories entries and permission to run CGI 

    - Check your Perl path 

    - Check all the linux commands works fine / defined in your PATH (grep, cut etc) 

    - Just check from command line isql -s <server> -u <user> -p <passwd> and if connects fine, this should also work. 
