import subprocess
import random
import string

# Generate random string of given length
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Generate random 5-character database name, 6-character username, and 16-character password
db_name = generate_random_string(5)
db_username = generate_random_string(6)
db_password = generate_random_string(16)

# Ask for user input
domain_name = input("Enter the domain name (e.g., example.com): ")
email_address = input("Enter your email address: ")

# List of commands
commands = [
    "apt update",
    "apt upgrade -y",
    "apt install nginx -y",
    "systemctl enable nginx",
    "systemctl start nginx",
    "iptables -I INPUT -p tcp --dport 80 -j ACCEPT",
    "ufw allow http",
    "chown www-data:www-data /usr/share/nginx/html -R",
    "apt install mariadb-server mariadb-client -y",
    "systemctl start mariadb",
    "systemctl enable mariadb",
    f"mysql -e \"CREATE DATABASE {db_name}; GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_username}'@'localhost' IDENTIFIED BY '{db_password}'; FLUSH PRIVILEGES;\"",
    "mysql_secure_installation",
    "apt install php7.4 php7.4-fpm php7.4-mysql php-common php7.4-cli php7.4-common php7.4-json php7.4-opcache php7.4-readline php7.4-mbstring php7.4-xml php7.4-gd php7.4-curl -y",
    "systemctl start php7.4-fpm",
    "systemctl enable php7.4-fpm",
    "rm /etc/nginx/sites-enabled/default",
    "rm /etc/nginx/sites-available/default",
    "systemctl reload nginx",
    "systemctl restart nginx",
    "mkdir -p /etc/systemd/system/nginx.service.d/",
    "systemctl daemon-reload",
    "mkdir /down",
    f"cd /down", 
    "wget https://wordpress.org/latest.zip",
    "apt install unzip -y",
    "mkdir -p /usr/share/nginx",
    "unzip latest.zip -d /usr/share/nginx/",
    f"mv /usr/share/nginx/wordpress /usr/share/nginx/{domain_name}",
    "rm -rf /down"
    "systemctl reload nginx",
    "apt install php-imagick php7.4-fpm php7.4-mbstring php7.4-bcmath php7.4-xml php7.4-mysql php7.4-common php7.4-gd php7.4-json php7.4-cli php7.4-curl php7.4-zip -y",
    "apt install python3-certbot-nginx -y",

]

# Run the commands
for command in commands:
    subprocess.run(command, shell=True, check=True)

# Server block configuration
server_block = f"""
# Server block configuration for {domain_name}
server {{
    listen 80;
    listen [::]:80;
    server_name www.{domain_name} {domain_name};
    root /usr/share/nginx/{domain_name}/;
    index index.php index.html index.htm index.nginx-debian.html;

    location / {{
        try_files $uri $uri/ /index.php;
    }}

    location ~ ^/wp-json/ {{
        rewrite ^/wp-json/(.*?)$ /?rest_route=/$1 last;
    }}

    location ~* /wp-sitemap.*\.xml {{
        try_files $uri $uri/ /index.php$is_args$args;
    }}

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;

    client_max_body_size 20M;

    location = /50x.html {{
        root /usr/share/nginx/html;
    }}

    location ~ \.php$ {{
        fastcgi_pass unix:/run/php/php7.4-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        include snippets/fastcgi-php.conf;
        fastcgi_buffers 1024 4k;
        fastcgi_buffer_size 128k;

        # Add headers to serve security related headers
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header X-Permitted-Cross-Domain-Policies none;
        add_header X-Frame-Options "SAMEORIGIN";
    }}

    #enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_comp_level 5;
    gzip_types application/json text/css application/x-javascript application/javascript image/svg+xml;
    gzip_proxied any;

    # A long browser cache lifetime can speed up repeat visits to your page
    location ~* \.(jpg|jpeg|gif|png|webp|svg|woff|woff2|ttf|css|js|ico|xml)$ {{
        access_log        off;
        log_not_found     off;
        expires           360d;
    }}

    # disable access to hidden files
    location ~ /\.ht {{
        access_log off;
        log_not_found off;
        deny all;
    }}
}}
"""

# Write the server block configuration to the file
with open(f"/etc/nginx/conf.d/{domain_name}.conf", "w") as config_file:
    config_file.write(server_block)

# Run certbot command
# certbot_command = f"certbot --nginx --agree-tos --redirect --hsts --staple-ocsp --email {email_address} -d {domain_name},www.{domain_name}"
# subprocess.run(certbot_command, shell=True, check=True)

# Print database credentials
print("Database Name:", db_name)
print("Username:", db_username)
print("Password:", db_password)

print("Setup, configuration, and certbot completed. Restart Nginx and enjoy.   CySec LLC")

