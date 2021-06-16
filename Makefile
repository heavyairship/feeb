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