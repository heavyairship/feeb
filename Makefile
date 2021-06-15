run:
	python infinity_axe.py &> infinity_axe_results.txt

make update:
	git add . && git commit -m "update" && git push origin master