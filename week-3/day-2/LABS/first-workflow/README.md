# GitHub Actions Fundamentals Lab

This lab matches the workflow examples used in the slide deck.

## What You Will Learn

- GitHub Actions workflow basics
- Events and triggers
- Jobs and steps
- GitHub hosted runners
- Workflow execution

## Folder Structure

.github/
└── workflows/
    └── first-workflow.yml

## Lab Steps

1. Create a new GitHub repository
2. Upload this project
3. Push to the `main` branch
4. Open the `Actions` tab in GitHub
5. Verify the workflow runs successfully

## Expected Result

The workflow should print:

Hello GitHub Actions

## Workflow Explanation

### name
Defines the workflow name.

### on
Defines the trigger event.

### jobs
Contains the jobs to execute.

### runs-on
Defines the GitHub-hosted runner.

### steps
Defines the list of tasks.

### run
Executes a shell command.
