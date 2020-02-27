# ttdsCW3
A search engine for recipes.

<h2>Deployment on the AWS2 server</h2>
<h4>1. Python</h4>
   <ul>
   <li>Install python3:</li>
   <code>yum install python37</code>
   </ul>
<h4>2. Python virtual environment</h4>
   <ul>
   <li>Install virtualenv:</li>
   <code>pip3 install virtualenv</code>
   <li>Add environment variables:</li>
   <code>PATH=$PATH:/usr/local/bin</code>
   <li>Create virtual environment:</li>
   <code>virtualenv -p /usr/bin/python3 djangoenv</code>
   </ul>
<h4>3. Git</h4>
   <ul>
   <li>Install git:</li>
   <code>yum install git</code>
   <li>Download the project:</li>
   <code>git clone https://github.com/crystal-xu/ttdsCW3.git</code>
   <li>Switch to dev branch:</li>
   <code>git checkout dev</code>
   </ul>
<h4>4. Install dependent libraries</h4>
   <ul>
   <li>Enter the virtual environment:</li>
   <code>source djangoenv/bin/active</code>
   <li>Install libraries:</li>
   <code>pip install -r requirements.txt</code>
   </ul>
<h4>5. uwsgi</h4>
   <ul>
   <li>Install uwsgi:</li>
   <code>pip install gcc python3-devel uwsgi</code>
   <li>Start uwsgi:</li>
   <code>uwsgi --ini uwsgi.ini</code>
   </ul>
<h4>6. nginx</h4>
   <ul>
   <li>Install nginx:</li>
   <code>sudo amazon-linux-extras install nginx1</code>
   <li>Configure nginx:</li>
   <code>/etc/nginx/nginx.conf</code>
   <li>Switch to root user</li>
   <li>Add configurations</li>
    <code>location / {</code><br>
        &nbsp<code>include uwsgi_params;</code><br>
        <code>uwsgi_pass 127.0.0.1:8000;</code><br>
    <code>}</code>
<br/>
    <code>location /static {</code><br>
        <code>alias /root/ttdsCW3/static;</code><br>
    <code>}</code>
   <li>Start nginx</li>
   </ul>


