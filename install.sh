/bin/echo -n "➜ Enter your custom feed address: "

read FEED_URL

FEED_URL=$(echo "$FEED_URL" | sed 's/&/\\&/g')

mkdir -p ~/bin

sed "s|FEED_URL_CONFIG|$FEED_URL|" showrss_helper.py \
		> ~/bin/showrss_helper.py

chmod u+x ~/bin/showrss_helper.py


echo "➜ Starting agent"

sed "s|HOME_DIR|$HOME|" org.0x0L.showrss.plist \
		> ~/Library/LaunchAgents/org.0x0L.showrss.plist

/bin/launchctl load ~/Library/LaunchAgents/org.0x0L.showrss.plist
