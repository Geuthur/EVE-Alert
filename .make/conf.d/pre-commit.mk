# Install pre-commit hook
.PHONY: pre-commit-install
pre-commit-install: check-python-venv
	@echo "Installing pre-commit hook …"
	@pre-commit install

# Uninstall pre-commit hook
.PHONY: pre-commit-uninstall
pre-commit-uninstall: check-python-venv
	@echo "Uninstalling pre-commit hook …"
	@pre-commit uninstall

# Update pre-commit configuration
.PHONY: pre-commit-update
pre-commit-update: check-python-venv
	@echo "Updating pre-commit configuration …"
	@pre-commit autoupdate --freeze

# Run pre-commit checks
.PHONY: pre-commit-checks
pre-commit-checks: pre-commit-install check-python-venv
	@echo "Running pre-commit checks …"
	@pre-commit run --all-files

# Help message for the Pre-Commit commands
.PHONY: help
help::
	@echo "  $(TEXT_UNDERLINE)Pre-Commit:$(TEXT_UNDERLINE_END)"
	@echo "    pre-commit-install          Install pre-commit hook"
	@echo "    pre-commit-uninstall        Uninstall pre-commit hook"
	@echo "    pre-commit-update           Update pre-commit configuration"
	@echo "    pre-commit-checks           Run pre-commit checks"
	@echo ""
