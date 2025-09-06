.DEFAULT_GOAL := help

run: ## Run the application with debug logging
	poetry run uvicorn main:app --reload --log-level debug

run-prod: ## Run in production mode
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

docs-generate: ## Generate HTML documentation for the entire project
	@echo "Generating documentation..."
	rm -rf docs_html
	pdoc bot_config database filters handlers keyboards models projects_images repository services setup templates --output-dir docs_html

docs-open: ## Open generated HTML documentation in browser
ifeq ($(OS),Windows_NT)
	@start docs_html\index.html
else
	@xdg-open docs_html/index.html || open docs_html/index.html
endif

test: ## run pytest
	pytest -q