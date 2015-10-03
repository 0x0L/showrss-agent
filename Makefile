install:
	@mkdir -p ~/bin
	@/bin/echo -n "➜ Enter your showRSS user id (eg. 17065): "
	@read user_id && \
				sed "s|USER_ID|$$user_id|" showrss_helper.py > ~/bin/showrss_helper.py

	@chmod u+x ~/bin/showrss_helper.py
	@sed "s|HOME_DIR|$(HOME)|" org.0x0L.showrss.plist \
			 > ~/Library/LaunchAgents/org.0x0L.showrss.plist

	@echo "➜ Starting agent"
	@echo "You can edit the CONFIGURATION variable in" \
		    "$(HOME)/bin/showrss_helper.py to customize your HD and Proper/Repack" \
				"settings."

	@/bin/launchctl load ~/Library/LaunchAgents/org.0x0L.showrss.plist

uninstall:
	@echo "➜ Stopping agent"
	@/bin/launchctl unload org.0x0L.showrss.plist

	@echo "➜ Removing files"
	@rm ~/Library/LaunchAgents/org.0x0L.showrss.plist
	@rm ~/bin/showrss_helper.py*
# @rm ~/.showrss
