PYTHON ?= python3
.PHONY: help setup build fydp-1 watch check thumbnail package
help:
	@$(PYTHON) scripts/project.py --help
setup:
	$(PYTHON) scripts/project.py doctor
build:
	$(PYTHON) scripts/project.py build
fydp-1:
	$(PYTHON) scripts/project.py build --stage fydp-1
watch:
	$(PYTHON) scripts/project.py watch
check:
	$(PYTHON) scripts/project.py check
thumbnail:
	$(PYTHON) scripts/project.py thumbnail
package:
	$(PYTHON) scripts/project.py package
