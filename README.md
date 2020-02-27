# ttdsCW3
A search engine for recipes.

**Deployment on the AWS2 server**
1.Install python3:<br/>
yum install python37<br/>
<br/>
2.Install virtualenv:<br/>
pip3 install virtualenv<br/>
Add environment variables:<br/>
PATH=$PATH:/usr/local/bin<br/>
Create virtual environment:<br/>
virtualenv -p /usr/bin/python3 djangoenv<br/>
<br/>
3.Install git:<br/>
yum install git<br/>
Download the project:<br/>
git clone https://github.com/crystal-xu/ttdsCW3.git\n<br/>
Switch to dev branch:<br/>
git checkout dev<br/>
<br/>
4.Install dependent libraries:<br/>
Enter the virtual environment<br/>
source djangoenv/bin/active<br/>
Install libraries:<br/>
pip install -r requirements.txt<br/>

5.Install uwsgi:<br/>
pip install gcc python3-devel uwsgi<br/>
Start uwsgi:<br/>
uwsgi --ini uwsgi.ini<br/>

6.Install nginx:<br/>
sudo amazon-linux-extras install nginx1<br/>
Configure nginx:<br/>
/etc/nginx/nginx.conf<br/>
Switch to root user<br/>
Add configurations<br/>
    location / {<br/>
        include uwsgi_params;<br/>
        uwsgi_pass 127.0.0.1:8000;<br/>
    }<br/>
<br/>
    location /static {<br/>
        alias /root/ttdsCW3/static;<br/>
    }<br/>
Start nginx<br/>


