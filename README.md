# ttdsCW3
A search engine for recipes.

##################Deployment on the AWS2 server#############
1.Install python3:
yum install python37

2.Install virtualenv:
pip3 install virtualenv
Add environment variables:
PATH=$PATH:/usr/local/bin
Create virtual environment:
virtualenv -p /usr/bin/python3 djangoenv

3.Install git:
yum install git
Download the project:
git clone https://github.com/crystal-xu/ttdsCW3.git\n
Switch to dev branch:
git checkout dev

4.Install dependent libraries:
Enter the virtual environment
source djangoenv/bin/active
Install libraries:
pip install -r requirements.txt

5.Install uwsgi:
pip install gcc python3-devel uwsgi
Start uwsgi:
uwsgi --ini uwsgi.ini

6.Install nginx:
sudo amazon-linux-extras install nginx1
Configure nginx:
/etc/nginx/nginx.conf
Switch to root user
Add configurations
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
    }

    location /static {
        alias /root/ttdsCW3/static;
    }
Start nginx


