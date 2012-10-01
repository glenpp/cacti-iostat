iostat () {
	/usr/bin/iostat -Ndkx 300 2 \
		| /usr/bin/tail -n+4 \
		| /bin/grep -A 1000 Device \
		| /usr/bin/tail -n+2 \
		| /usr/bin/head -n-1 \
		| /bin/sed 's/  */ /g' \
		> /var/local/snmp/iostat.tmp$$
	mv /var/local/snmp/iostat.tmp$$ /var/local/snmp/iostat
}


# background the iostat run
iostat &
