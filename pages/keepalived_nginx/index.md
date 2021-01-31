# keepalived + nginx + tomcat メモ

- [keepalived + nginx + tomcat メモ](#keepalived---nginx---tomcat---)
  * [Prefix](#prefix)
  * [keepalived and nginx command](#keepalived-and-nginx-command)
    + [manjaro](#manjaro)
    + [fedora／centos](#fedora-centos)
    + [disable selinux, firewalld](#disable-selinux--firewalld)
    + [設定ファイル](#------)
      - [manjaro](#manjaro-1)
      - [centos/fedora](#centos-fedora)
      - [共通](#--)
  * [tomcat command](#tomcat-command)
    + [ubuntu (centosのインストール方法は類似ので、省略。apt -> dnf, nano -> vi, ufw -> firewall)](#ubuntu--centos------------------apt----dnf--nano----vi--ufw----firewall-)

<a href="https://xflduke.github.io/">Back to Index</a>

## Prefix

- 環境
  - manjaro (keepalived master, nginx)
  - fedora (keepalived backup, nginx)
  - centos 8 (keepalived backup, nginx)
    - install from boot
    - repos sources : http://mirror.centos.org/centos/8/BaseOS/x86_64/os/

[//]: <> (参照：https://linuxhint.com/install_centos8_netboot_iso/)

  - ubuntu (tomcat)
  - centos 8 (tomcat)
    - install from full media

## keepalived and nginx command

### manjaro

```bash
  # リブ管理ツールを用いて、nginxをインストール＆サービス自動開始
  sudo pacman -Syu
  sudo pacman -S nginx
  sudo systemctl start nginx
  sudo systemctl enable nginx
  # install keepalived
  sudo pacman -S keepalived
  sudo systemctl start keepalived
  sudo systemctl enable keepalived
```
### fedora／centos

need set selinux and firewall

[//]: <> (参照：https://mangolassi.it/topic/16651/install-nginx-as-a-reverse-proxy-on-fedora-27/23)
[//]: <> (selinux参照：https://www.nginx.com/blog/using-nginx-plus-with-selinux/)

```bash
  # リブ管理ツールを用いて、nginxをインストール
  dnf upgrade -y --refresh
  dnf install -y certbot-nginx nginx policycoreutils-python-utils
  # ファイアウォール http/https許可
  firewall-cmd --add-port=http/tcp --permanent
  firewall-cmd --add-port=https/tcp --permanent
  firewall-cmd --reload
  # selinux設定、nginxからウェブサーバへ接続可能のためhttp許可、setools方式
  sudo dnf install sesearch
  setsebool -P httpd_can_network_connect 1
  # semanage方式
  semanage permissive -a httpd_t
  semanage port -l | grep http_port_t
  semanage port -a -t http_port_t -p tcp 8080
  # nginx有効化
  systemctl start nginx
  systemctl enable nginx
  # install keeplived
  dnf install keepalived
  systemctl start keepalived
  systemctl enable keepalived
```

### disable selinux, firewalld
```bash
  # 再起動まで無効化、有効には１
  sudo setenforce 0
  # 永久的に無効化には　/etc/selinux/config　の　SELINUX　を　permissive　or disabled　に設定　（reboot必要）
  #     enforcing - SELinux security policy is enforced.
  #     permissive - SELinux prints warnings instead of enforcing.
  #     disabled - No SELinux policy is loaded.
  # チェックSELINUX設定状態
  sestatus
```

### 設定ファイル

#### manjaro

/etc/nginx/nginx.conf 
```properties
#user html;

worker_processes  2;

error_log  /var/log/nginx/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;
    types_hash_max_size 4096;

    #gzip  on;

    upstream io.duke {
    	server 192.168.3.58:8080 weight=1;
    	server 192.168.3.59:8080 weight=1;
    }
 
    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

#        location / {
#            root   /usr/share/nginx/html;
#            index  index.html index.htm;
#        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #
	
	location ~ .*\.(html|htm|gif|jpg|jpeg|bmp|png|ico|txt|js|css)$ 
    	{	
	 	root         /data/www;
		expires      1m;
	}

	location /
	{
		proxy_pass http://io.duke;
	}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
```

/etc/keepalived/keepalived.conf

```properties
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.3.56
   smtp_connect_timeout 30
   router_id LVS_DEVEL
   vrrp_skip_check_adv_addr
#   vrrp_strict
   vrrp_garp_interval 1
   vrrp_gna_interval 1
   script_user root
   enable_script_security
}

vrrp_script chk_http_port {
        script "/usr/local/nginx/nginx_check.sh"
        interval 2
        weight 2
}

vrrp_instance VI_1 {
    state MASTER
    interface ens33 
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.3.16/24 label vip
    }
    track_script {
        chk_http_port
    }
}
```

#### centos/fedora

/etc/nginx/nginx.conf

```properties
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    upstream io.duke {
        server 192.168.3.58:8080 weight=1;
        server 192.168.3.59:8080 weight=1;
    }

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }

        location ~ .*\.(html|htm|gif|jpg|jpeg|bmp|png|ico|txt|js|css)$ 
        {
                root         /data/www;
                expires      1m;
        }

        location /
        {
                proxy_pass http://io.duke;
        }
    }

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers PROFILE=SYSTEM;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}
```
/etc/keepalived/keepalived.conf

```bash
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.3.60
   smtp_connect_timeout 30
   router_id LVS_DEVEL
   vrrp_skip_check_adv_addr
#   vrrp_strict
   vrrp_garp_interval 1
   vrrp_gna_interval 1
   script_user root
   enable_script_security
}

vrrp_script chk_http_port {
        script "/usr/local/nginx/nginx_check.sh"
        interval 2
        weight 2
}

vrrp_instance VI_1 {
    state MASTER
    interface ens33
    virtual_router_id 51
    priority 95
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.3.16/24 label vip
    }
    track_script {
        chk_haproxy
    }
}
```


#### 共通

/usr/local/nginx/nginx_check.sh 
```bash
#!/bin/bash
counter=$(ps -C nginx --no-heading|wc -l)
if [ "${counter}" = "0" ]; then
    systemctl start nginx 
    sleep 2
    counter=$(ps -C nginx --no-heading|wc -l)
    if [ "${counter}" = "0" ]; then
        systemctl stop keepalived
    fi
fi
```

## tomcat command

### ubuntu (centosのインストール方法は類似ので、省略。apt -> dnf, nano -> vi, ufw -> firewall)
```bash
  sudo apt update
  sudo apt install default-jdk
  sudo useradd -r -m -U -d /opt/tomcat -s /bin/false tomcat
  wget http://www-eu.apache.org/dist/tomcat/tomcat-9/v9.0.41/bin/apache-tomcat-9.0.41.tar.gz -P /tmp
  sudo tar xf /tmp/apache-tomcat-9*.tar.gz -C /opt/tomcat
  sudo ln -s /opt/tomcat/apache-tomcat-9.0.27 /opt/tomcat/latest
  sudo chown -RH tomcat: /opt/tomcat/latest
  sudo sh -c 'chmod +x /opt/tomcat/latest/bin/*.sh'
  sudo nano /etc/systemd/system/tomcat.service # 
  sudo systemctl daemon-reload
  sudo systemctl start tomcat
  sudo systemctl enable tomcat
  sudo ufw allow 8080/tcp
  sudo nano /opt/tomcat/latest/conf/tomcat-users.xml # 
  sudo nano /opt/tomcat/latest/webapps/manager/META-INF/context.xml # 
```
/etc/systemd/system/tomcat.service 
```properties
[Unit]
Description=Tomcat 9 servlet container
After=network.target

[Service]
Type=forking

User=tomcat
Group=tomcat

Environment="JAVA_HOME=/usr/lib/jvm/default-java"
Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom -Djava.awt.headless=true"

Environment="CATALINA_BASE=/opt/tomcat/latest"
Environment="CATALINA_HOME=/opt/tomcat/latest"
Environment="CATALINA_PID=/opt/tomcat/latest/temp/tomcat.pid"
Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"

ExecStart=/opt/tomcat/latest/bin/startup.sh
ExecStop=/opt/tomcat/latest/bin/shutdown.sh

[Install]
WantedBy=multi-user.target
```

/opt/tomcat/latest/conf/tomcat-users.xml

```xml
<tomcat-users>
<!--
    Comments
-->
   <role rolename="admin-gui"/>
   <role rolename="manager-gui"/>
   <user username="admin" password="admin_password" roles="admin-gui,manager-gui"/>
</tomcat-users>
```

/opt/tomcat/latest/webapps/manager/META-INF/context.xml
/opt/tomcat/latest/webapps/host-manager/META-INF/context.xml
add remote address to access tomcat server
```xml
<Context antiResourceLocking="false" privileged="true" >
<!--
  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />
-->
</Context>
```

 <a href="#top">Back to top</a>

<a href="https://xflduke.github.io/">Back to Index</a>
