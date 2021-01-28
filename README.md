To get started with the project 
1- Clone the repo to a folder 
2- create a virtual environment for the project 
3- run pip install -r requirements.txt to install all the required packages 
4- python manage.py makemigrations 
5- python manage.py migrate
6- python manage.py runserver

Postman documentation - https://documenter.getpostman.com/view/10412699/TW6xmn6K
postman collection -https://www.getpostman.com/collections/ed904ba1383bbd492b74

things to remember - 
in authorization header in postman token pattern is as follows : - "Token {token}"
ex = "Token a59a963c067a12dc72f53a18350bd2332d28ef2caa6ae41bd42737c9bd5e6709"

in search api ordering field can order posts on basis of its fields which have to be mentioned in the request itself 
so the attributes for it are :- content(content of  post), created(date of creation), updated(date of updation), author(registered users), image(images posted)
