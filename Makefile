clean:
	rm -rf ./data 

clean_inf:
	rm -rf ./data/inf

clean_sal:
	rm -rf ./data/sal

inf: clean_inf
	mkdir -p ./data/inf && python3 infinity_axe.py > ./data/inf/infinity_axe_results.txt

sal: clean_sal
	mkdir -p ./data/sal && python3 salamandrew.py > ./data/sal/salamandrew_results.txt

all: inf sal

update:
	git add . && git commit -m "update" && git push origin master