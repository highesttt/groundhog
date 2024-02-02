##
## EPITECH PROJECT, 2023
## Groundhog [WSL: Manjaro]
## File description:
## Makefile
##

all:
	@cp src/groundhog.py groundhog
	@chmod 777 groundhog

re: fclean all

fclean:
	@rm -f groundhog

tests_run:
	@pytest tests/.

coverage:
	@coverage run -m pytest -v tests/ && coverage report --show-missing

coverage_html:
	@coverage run -m pytest -v tests/ && coverage html

.PHONY: all re fclean tests_run coverage coverage_html