# EconomicModel
Minimal economic model of long-term storage

This code implements the Web site http://economicmodel.dshr.org as described here http://blog.dshr.org/2017/08/economic-model-of-long-term-storage.html

To install the Web site on a Raspberry Pi:
1. Install Raspbian minimal version, and update it.
2. Get ssh daemon to start on power-up.
3. Enter sudo raspi-config in a terminal window
4. Select Interfacing Options
5. Navigate to and select SSH
6. Choose Yes
7. Select Ok
8. Choose Finish
9. Install python3 and modules: python3-requests, python3-matplotlib, XXX check apt listing
10. Install apache2. "sudo a2enmod cgid"
11. Install web pages in /var/www/html owned by www-data.
12. Install CGI scripts in /usr/lib/cgi-bin owned by www-data.
13. Create /var/www/html/images, chown to www-data.
14. Give www-data a crontab that cleans /var/www/html/images.
