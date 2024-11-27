# Markdown 3030
 - Namespace: picoctf/18739f24
 - ID: sql-orm
 - Type: custom
 - Category: Web Exploitation
 - Points: 300
 - Templatable: yes
 - MaxUsers: 1

## Description 

My friend told me that an ORM will protect me against SQL injections, so 
I used django to deploy my app to appease the AI overlords. Since django
uses an ORM, I should be 100% safe!

## Hints 

- An SQL injection is possible.
  
## Details

The server is running {{link_as('/', 'here')}}. 
Also, {{url_for("views.py", "views.py")}} is available.

## Attributes
 - author: aalfares
