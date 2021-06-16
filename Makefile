clean:
	rm -rf ./data 

clean_bot:
	rm -rf ./data/bot

clean_sal:
	rm -rf ./data/sal

bot: clean_bot
	mkdir -p ./data/bot && python3 ragebot3000.py > ./data/bot/ragebot3000_results.txt

sal: clean_sal
	mkdir -p ./data/sal && python3 salamandrew.py > ./data/sal/salamandrew_results.txt

all: bot sal

update:
	git add . && git commit -m "update" && git push origin master