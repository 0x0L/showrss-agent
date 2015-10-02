install:
	@echo
	@mkdir -p ~/bin
	@echo "⁇ Enter your showRSS user id (eg. 17065):"; \
			  read user_id; \
				sed "s|USER_ID|$$user_id|" showrss_helper.py > ~/bin/showrss_helper.py

	@sed "s|HOME_DIR|$(HOME)|" org.0x0L.showrss.plist \
			 > ~/Library/LaunchAgents/org.0x0L.showrss.plist

	@echo
	@echo "➜ Starting agent"
	@/bin/launchctl load ~/Library/LaunchAgents/org.0x0L.showrss.plist

	@echo
	@echo "You can edit the CONFIGURATION variable in" \
		    "$(HOME)/bin/showrss_helper to customize your HD and Proper/Repack" \
				"settings."

uninstall:
	@echo
	@echo "➜ Stopping agent"
	@/bin/launchctl unload org.0x0L.showrss.plist

	@echo "➜ Removing files"
	@rm ~/Library/LaunchAgents/org.0x0L.showrss.plist
	@rm ~/bin/showrss_helper.py
# @rm ~/.showrss
