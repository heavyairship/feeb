.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

clean_bot:
	rm -rf ./data/bot

clean_sal:
	rm -rf ./data/sal

clean_bix:
	rm -rf ./data/bix

clean: clean_bot clean_sal clean_bix
	rm -rf ./data 

bot: clean_bot
	mkdir -p ./data/bot && PYTHONPATH=$(PYTHONPATH):./lib:./players python3 players/ragebot3000.py > ./data/bot/ragebot3000_results.txt

sal: clean_sal
	mkdir -p ./data/sal && PYTHONPATH=$(PYTHONPATH):./lib python3 players/salamandrew.py > ./data/sal/salamandrew_results.txt

bix: clean_bix
	mkdir -p ./data/bix && PYTHONPATH=$(PYTHONPATH):./lib python3 players/bixby.py > ./data/bix/bixby_results.txt

all: bot sal bix

fight: clean
	PYTHONPATH=$(PYTHONPATH):./lib:./players python3 fun/fight.py

update:
	git add . && git commit -m "update" && git push origin master