# Tekton CD Pipeline

This directory contains Tekton pipeline definitions for Continuous Deployment.

## Files

- **tasks.yaml**: Defines reusable Tekton tasks (echo, checkout, nose tests, cleanup)
- **pipeline.yaml**: Defines the CD pipeline that chains tasks together
- **pipelinerun.yaml**: Template for running the pipeline

## Pipeline Flow

1. **init**: Prints a start message
2. **clone**: Checks out code from GitHub repository
3. **test**: Runs nose tests with PostgreSQL database
4. **cleanup**: Removes temporary files

## Usage (if Tekton were installed)
```bash
# Apply tasks and pipeline
oc apply -f tasks.yaml
oc apply -f pipeline.yaml

# Run the pipeline
oc create -f pipelinerun.yaml

# Watch execution
oc get pipelinerun -w
```

## Note

This project was developed in an environment without Tekton installation permissions.
The manifests are provided to demonstrate understanding of Tekton CD concepts.
