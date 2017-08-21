# EconomicModel
Minimal economic model of long-term storage

This code implements the Web site http://economicmodel.dshr.org as described here http://blog.dshr.org/2017/08/economic-model-of-long-term-storage.html

To install the Web site on a Raspberry Pi:
1. Install Raspbian minimal version, and update it.
2. Install python3 python3 python3-chardet python3-dateutil python3-matplotlib python3-minimal python3-nose python3-numpy python3-pil python3-pkg-resources python3-pyparsing python3-requests python3-six python3-tk python3-tz python3-urllib3
3. Install apache2. "sudo a2enmod cgid"
4. Install web pages in /var/www/html owned by www-data.
5. Install CGI scripts in /usr/lib/cgi-bin owned by www-data.
6. Create /var/www/html/images, chown to www-data.
7. Give www-data a crontab that cleans /var/www/html/images.
