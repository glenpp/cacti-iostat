# iostat on Cacti via SNMP

## iostat to SNMP

Like I described in similar Cacti sources, I run a cron job to pick up data and dump it in files where snmpd can pick it up as a low privilege user. I'm doing the same here, except that I'm using it to run iostat in the background to collect data over the polling period.

Take the data collection script **iostat\_cron.py**, make this executable and stick it somewhere convenient. I will assume **/etc/snmp/** for this article with the output files in **/var/local/snmp/**. Then add a CRON job (every 5 minutes or to match your Cacti polling time) to run a script to launch this:

```sh
# background the iostat run
/etc/snmp/iostat_cron.py /var/local/snmp/iostat.json &
```

That will launch iostat in a wrapper which will run for 5 minutes (300 seconds) outputting to a temporary file and rename the temporary file to the name given as the first argument. You can easily alter the script if you poll more/less frequently. Also you can modify the iostat arguments to output per-partition statistics if you require.

Check that the output file is being created and has data in it - it will take 5 minutes from the next cron run before the file is created.

Make the extension script **iostat\_stats.py** executable and put it somewhere suitable **like /etc/snmp/** which is what we will assume for this article. Next, to get the data into snmpd add the lines from **snmpd.conf.cacti-iostat** to the **/etc/snmp/snmpd.conf** file.

That simply picks up the column specified from data file when SNMP is queried. Restart **snmpd** and you should be able to test that with snmpwalk.

## SNMP to Cacti

I have the query xml **iostat.xml** in /**usr/local/share/cacti/resource/snmp_queries/** however if you put it elsewhere then you will need to modify the data query path in the template to match.

Import the Cacti template **cacti_host_template_iostat.xml** into Cacti and add it to the host you have configured above. Add the graphs and all going well after a couple polls data should start appearing on the graphs.
