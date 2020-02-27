# ttdsCW3
A search engine for recipes.

Deploy the project on the AWS2 server:\n
1.Install python3:\n
yum install python37\n
\n
2.Install virtualenv:\n
pip3 install virtualenv\n
Add environment variables:\n
PATH=$PATH:/usr/local/bin\n
Create virtual environment:\n
virtualenv -p /usr/bin/python3 djangoenv\n
\n
3.Install git:\n
yum install git\n
Download the project:\n
git clone https://github.com/crystal-xu/ttdsCW3.git\n
Switch to dev branch:\n
git checkout dev\n
\n
4.Install dependent libraries:\n
Enter the virtual environment\n
source djangoenv/bin/active\n
Install libraries:\n
pip install -r requirements.txt\n
\n
5.Install uwsgi:\n
pip install gcc python3-devel uwsgi\n
Start uwsgi:\n
uwsgi --ini uwsgi.ini\n
\n
6.Install nginx:\n
sudo amazon-linux-extras install nginx1\n
Configure nginx:\n
/etc/nginx/nginx.conf\n
Switch to root user\n
Add configurations\n
    location / {\n
        include uwsgi_params;\n
        uwsgi_pass 127.0.0.1:8000;\n
    }\n

    location /static {\n
        alias /root/ttdsCW3/static;\n
    }\n
Start nginx\n


