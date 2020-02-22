# EconomicModel
Minimal economic model of long-term storage

This code implements the Web site http://economicmodel.dshr.org as described here http://blog.dshr.org/2017/08/economic-model-of-long-term-storage.html

1. Install Raspbian minimal version.
2. Log in
3. Install needed packages:

sudo apt-get install python3 python3 python3-chardet python3-dateutil python3-matplotlib python3-minimal python3-nose python3-numpy python3-pil python3-pkg-resources python3-pyparsing python3-requests python3-six python3-tk python3-tz python3-urllib3 git apache2

4. Enable CGI scripts:

sudo a2enmod cgid

5. Clone the model from github:

git clone https://github.com/dshrosenthal/EconomicModel

6. Install Web pages:

sudo cp EconomicModel/html/*.html /var/www/html
sudo chown www-data:www-data /var/www/html/*.html

7. Install CGI scripts:

sudo cp EconomicModel/cgi-bin/*.py /usr/lib/cgi-bin
sudo chown www-data:www-data /usr/lib/cgi-bin/*.py

8. Make directory for graphs:

sudo mkdir /var/www/html/images
sudo chown www-data:www-data /var/www/html/images

9. Give www-data a cron script to clean the image directory:

cat >/tmp/foo <<Funky-EOF
13 * * * * find /var/www/html/images -amin +120 -exec rm {} \;
Funky-EOF
sudo crontab -u www-data /tmp/foo

10. Reboot.
