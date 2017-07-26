f=/root/sbx_nxos/learning_labs/poap/poap_app/templates/ztp_script.py ; cat $f | sed '/^#md5sum/d' > $f.md5 ; sed -i \
"s/^#md5sum=.*/#md5sum=\"$(md5sum $f.md5 | sed 's/ .*//')\"/" $f
