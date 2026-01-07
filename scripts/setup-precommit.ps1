# Install and configure pre-commit hooks for SpiralSafe
# Requires python/pip
python -m pip install --user pre-commit detect-secrets
# Install git hooks
python -m pre_commit install
# Generate baseline (inspect before committing)
detect-secrets scan --update .secrets.baseline
Write-Host "Pre-commit installed. Review and commit .secrets.baseline before pushing." -ForegroundColor Green