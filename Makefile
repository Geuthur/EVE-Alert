# Specify the shell to be used for executing the commands in this Makefile.
# In this case, it is set to /bin/bash.
SHELL := /bin/bash

# Variables
appname = eve-alert
appname_verbose = EVE-Alert
package = evealert
git_repository = https://github.com/Geuthur/$(appname)
git_repository_issues = $(git_repository)/issues

# Default goal
.DEFAULT_GOAL := help

# Check if Python virtual environment is active
.PHONY: check-python-venv
check-python-venv:
	@if [ -z "$(VIRTUAL_ENV)" ]; then \
		echo "$(TEXT_COLOR_RED)$(TEXT_BOLD)Python virtual environment is NOT active!$(TEXT_RESET)" ; \
		exit 1; \
	fi

# Confirm action
.PHONY: confirm-action
confirm-action:
	@read -p "Are you sure you want to run '$(MAKECMDGOALS)'? [Y/n] " response; \
	response=$${response:-Y}; \
	if [ "$$response" != "Y" ] && [ "$$response" != "y" ]; then \
		echo "Aborted"; \
		exit 1; \
	fi

# General confirmation
.PHONY: confirm
confirm:
	@read -p "Are you sure? [Y/n] " response; \
	response=$${response:-Y}; \
	if [ "$$response" != "Y" ] && [ "$$response" != "y" ]; then \
		echo "Aborted"; \
		exit 1; \
	fi

# Prepare a new release
# Update the version in the package
.PHONY: prepare-release
prepare-release:
	@echo ""
	@echo "Preparing a release …"
	@read -p "New Version Number: " new_version; \
	if grep -qE "^## \[$$new_version\]" CHANGELOG.md; then \
		sed -i "/__version__ = /c\__version__ = \"$$new_version\"" $(package)/__init__.py; \
		echo "Updated version in $(TEXT_BOLD)$(package)/__init__.py$(TEXT_BOLD_END)"; \
		echo "$$new_version" | grep -q -E 'alpha|beta'; \
		if [ $$? -eq 0 ]; then \
			echo "$(TEXT_COLOR_RED)$(TEXT_BOLD)Pre-release$(TEXT_RESET) version detected!"; \
		else \
			echo "$(TEXT_BOLD)Release$(TEXT_BOLD_END) version detected."; \
		fi; \
	else \
		echo "$(TEXT_COLOR_RED)$$new_version not found in CHANGELOG.md!$(TEXT_COLOR_RED_END)\n$(TEXT_COLOR_YELLOW)Please ensure to update it with your changes.$(TEXT_COLOR_YELLOW_END)"; \
		exit 1; \
	fi

# Help
.PHONY: help
help::
	@echo ""
	@echo "$(TEXT_BOLD)$(appname_verbose)$(TEXT_BOLD_END) Makefile"
	@echo ""
	@echo "$(TEXT_BOLD)Usage:$(TEXT_BOLD_END)"
	@echo "  make [command]"
	@echo ""
	@echo "$(TEXT_BOLD)Commands:$(TEXT_BOLD_END)"
	@echo "  $(TEXT_UNDERLINE)General:$(TEXT_UNDERLINE_END)"
	@echo "    help                        Show this help message"
	@echo "    prepare-release             Prepare a release and update the version."
	@echo ""

# Include the configurations
include .make/conf.d/*.mk
