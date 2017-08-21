# EconomicModel
Minimal economic model of long-term storage

This code implements the Web site http://economicmodel.dshr.org as described here http://blog.dshr.org/2017/08/economic-model-of-long-term-storage.html

To install the Web site on a Raspberry Pi:
1. Install Raspbian minimal version, and update it.
2. Install python3 and modules: python3-requests, python3-matplotlib, XXX check apt listing
3. Install apache2. "sudo a2enmod cgid"
4. Install web pages in /var/www/html owned by www-data.
5. Install CGI scripts in /usr/lib/cgi-bin owned by www-data.
6. Create /var/www/html/images, chown to www-data.
7. Give www-data a crontab that cleans /var/www/html/images.
