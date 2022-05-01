# ======================= Virtual Environment Management =======================

create_env:
	@echo "🐍 Creating Virtual Environment for python3.10..."
	python3.10 -m venv .venv

activate_env:
	@echo "🐍 Activating Virtual Environment (python3.10)..."
	activate ./.venv/bin/activate"

# =========================== Dependency Management ============================

update_deps:
	@echo "🔃 Updating dependencies..."
	@poetry update

deps_install_no_dev: update_deps
	@echo "⬇️ Installing only production dependencies..."
	@poetry install --no-dev

deps_install: update_deps
	@echo "⬇️ Installing all dependencies..."
	@poetry install

deps_export: update_deps
	@echo "📥 Exporting dependencies to requirements.txt"
	@poetry export --without-hashes --output requirements.txt

# ================================ Code Quality ================================

check_flake8:
	@echo "🎨 Checking with Flake8..."
	@poetry run flake8 ./mona --count --show-source --statistics
	@echo "✅ Flake8 check finished!"

check_isort:
	@echo "🎨 Checking with isort..."
	@poetry run isort **/*.py --check-only
	@echo "✅ isort check finished!"

test:
	@echo "🧪 Running tests with pytest..."
	@poetry run pytest
	@echo "✅ Pytest check finished!"

check: check_flake8 check_isort test
	@echo "✅ All checks are finished!"

setup_pre_commit:
	@echo "⚠️ Setting up pre-commit"
	@poetry run install

# ========================== Documentation Management ==========================

docs:
	@echo "📃 Updating documentation with handsdown..."
	@poetry run handsdown --external `git config --get remote.origin.url`

# ===================== Development Environment Management =====================

setup: create_env activate_env install_all setup_pre_commit
	@echo "✨ Setup finished!"