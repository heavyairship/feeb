.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

clean:
	rm -rf ./data 

clean_bot:
	rm -rf ./data/bot

clean_sal:
	rm -rf ./data/sal

clean_bix:
	rm -rf ./data/bix

bot: clean_bot
	mkdir -p ./data/bot && PYTHONPATH=$(PYTHONPATH):./lib python3 players/ragebot3000.py > ./data/bot/ragebot3000_results.txt

sal: clean_sal
	mkdir -p ./data/sal && PYTHONPATH=$(PYTHONPATH):./lib python3 players/salamandrew.py > ./data/sal/salamandrew_results.txt

bix: clean_bix
	mkdir -p ./data/bix && PYTHONPATH=$(PYTHONPATH):./lib python3 players/bixby.py > ./data/bix/bixby_results.txt

all: bot sal bix

update:
	git add . && git commit -m "update" && git push origin master