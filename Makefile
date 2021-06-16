clean:
	rm -rf ./data

run: clean
	mkdir ./data && python3 infinity_axe.py > ./data/infinity_axe_results.txt

update:
	git add . && git commit -m "update" && git push origin master