echo "➜ Stopping agent"
/bin/launchctl unload org.0x0L.showrss.plist

echo "➜ Removing files"
rm ~/Library/LaunchAgents/org.0x0L.showrss.plist
rm ~/bin/showrss_helper.py*
# rm ~/.showrss
