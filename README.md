# ttdsCW3
A search engine for recipes.

**Deployment on the AWS2 server**<br/>
1. Python
1) Install python3:<br/>
   yum install python37<br/>
<br/>
2. Python virtual environment
1) Install virtualenv:<br/>
   pip3 install virtualenv<br/>
2) Add environment variables:<br/>
   PATH=$PATH:/usr/local/bin<br/>
3) Create virtual environment:<br/>
   virtualenv -p /usr/bin/python3 djangoenv<br/>
<br/>
3. Git
1) Install git:<br/>
   yum install git<br/>
2) Download the project:<br/>
   git clone https://github.com/crystal-xu/ttdsCW3.git\n<br/>
3) Switch to dev branch:<br/>
   git checkout dev<br/>
<br/>
4. Install dependent libraries<br/>
1) Enter the virtual environment<br/>
   source djangoenv/bin/active<br/>
2) Install libraries:<br/>
   pip install -r requirements.txt<br/>

5. uwsgi
1) Install uwsgi:<br/>
   pip install gcc python3-devel uwsgi<br/>
2) Start uwsgi:<br/>
   uwsgi --ini uwsgi.ini<br/>

6. nginx
1) Install nginx:<br/>
   sudo amazon-linux-extras install nginx1<br/>
2) Configure nginx:<br/>
   /etc/nginx/nginx.conf<br/>
3) Switch to root user<br/>
4) Add configurations<br/>
    location / {<br/>
        include uwsgi_params;<br/>
        uwsgi_pass 127.0.0.1:8000;<br/>
    }<br/>
<br/>
    location /static {<br/>
        alias /root/ttdsCW3/static;<br/>
    }<br/>
5) Start nginx<br/>


