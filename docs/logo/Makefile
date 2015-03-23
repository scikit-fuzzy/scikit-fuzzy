all: clean generate-logo generate-icon
	rm -f ./temp.png

clean:
	rm -f ./logo*.png
	rm -f ./icon*.png
	rm -f ./temp.png

generate-logo:
	python skfuzzy_logo.py
	rm -f ./temp.png

generate-icon:
	python skfuzzy_icon.py
	rm -f ./temp.png
