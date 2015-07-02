install:
	@echo
	@mkdir -p ~/bin
	@echo "⁇ Enter your showRSS user id (eg. 17065):"; \
			  read user_id; \
				sed "s|USER_ID|$$user_id|" show-rss-helper.py > ~/bin/show-rss-helper.py

	@sed "s|HOME_DIR|$(HOME)|" org.x0l.show-rss.plist \
			 > ~/Library/LaunchAgents/org.x0l.show-rss.plist

	@echo
	@echo "➜ Starting agent"
	@/bin/launchctl load ~/Library/LaunchAgents/org.x0l.show-rss.plist

	@echo
	@echo "You can edit the CONFIGURATION variable in" \
		    "$(HOME)/bin/show-rss-helper to customize your HD and Proper/Repack" \
				"settings."

uninstall:
	@echo
	@echo "➜ Stopping agent"
	@/bin/launchctl unload org.x0l.show-rss.plist

	@echo "➜ Removing files"
	@rm ~/Library/LaunchAgents/org.x0l.show-rss.plist
	@rm ~/bin/show-rss-helper.py
# @rm ~/.show-rss
