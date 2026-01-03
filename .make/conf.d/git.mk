# Git prune
.PHONY: git-prune
git-prune:
	@echo "Pruning unreachable objects …"
	@git prune

# Git Reset Soft to HEAD~1
.PHONY: git-reset-soft
git-reset-soft:
	@echo "Resetting HEAD to the previous commit …"
	@git reset --soft HEAD~1

# Git force push
.PHONY: git-force-push
git-force-push:
	@echo "Forcing push to the remote repository …"
	@git push --force

# Git housekeeping tasks
.PHONY: git-clean-untracked
git-clean-untracked:
	@echo "Cleaning untracked files and directories …"
	@git clean -fd

# Git garbage collection
.PHONY: git-garbage-collection
git-garbage-collection:
	@echo "Optimizing the repository with garbage collection …"
	@git gc --prune=now --aggressive

# Git housekeeping (all tasks)
.PHONY: git-housekeeping
git-housekeeping: git-clean-untracked git-prune git-garbage-collection
	@echo "Git housekeeping done …"

.PHONY: help
help::
	@echo "  $(TEXT_UNDERLINE)Git:$(TEXT_UNDERLINE_END)"
	@echo "    git-prune                   Pruning unreachable objects"
	@echo "    git-reset-soft              Resetting HEAD to the previous commit (soft)"
	@echo "    git-force-push              Forcing push to the remote repository"
	@echo "    git-clean-untracked         Cleaning untracked files and directories"
	@echo "    git-garbage-collection      Optimizing the repository with garbage collection"
	@echo "    git-housekeeping            Run all git housekeeping commands"
	@echo ""
