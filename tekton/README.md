# Tekton CD Pipeline

## Note
This pipeline was designed for OpenShift with Tekton installed.
The lab environment does not have Tekton CRDs installed and lacks
the necessary cluster-admin permissions to install them.

## What Would Have Been Implemented

1. **git-clone task**: Clone repository from GitHub
2. **flake8 task**: Lint Python code
3. **nose task**: Run unit tests
4. **deploy task**: Apply Kubernetes manifests and restart deployment

## Working CI/CD Alternative

GitHub Actions is configured and working for this project:
- Runs on every push and pull request
- Executes linting (flake8)
- Runs unit tests (nosetests)
- Validates code quality

See: `.github/workflows/ci-build.yaml`
