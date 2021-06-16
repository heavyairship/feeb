clean:
	rm -f *.png infinity_axe_results.txt

run: clean
	python3 infinity_axe.py > infinity_axe_results.txt

update:
	git add . && git commit -m "update" && git push origin master