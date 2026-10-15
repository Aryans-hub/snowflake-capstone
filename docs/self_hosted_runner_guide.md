# GitHub Actions Self-Hosted Runner Guide

This guide explains how to register and use a Windows self-hosted runner for a GitHub repository, configure a workflow job to use it, test it, and troubleshoot common issues.

## 1. What is a self-hosted runner?

A **self-hosted runner** is a machine that you manage which runs GitHub Actions jobs. Unlike a GitHub-hosted runner such as `ubuntu-latest`, it uses your own machine and its installed tools.

In this project, the runner is registered on a Windows machine and is used by the `convention-check` job to validate pull-request source branch names.

## 2. Register a Windows self-hosted runner

You only need to register the machine once, unless you remove or reconfigure the runner.

1. Open the repository on GitHub.
2. Go to **Settings → Actions → Runners**.
3. Select **New self-hosted runner**.
4. Choose **Windows** and the appropriate architecture, usually **x64**.
5. Follow the commands displayed by GitHub for your repository.

GitHub provides a temporary registration token and repository-specific commands. Use those instructions rather than copying a token or command from an old setup guide.

Keep the runner directory on the machine. Do **not** commit the `actions-runner` directory to the project repository. If that directory is inside the repository, add it to `.gitignore`, for example:

```gitignore
actions-runner/
```

## 3. Start and check the runner

Open PowerShell in the runner installation directory.

To start the runner interactively, run:

```powershell
.\run.cmd
```

Keep the terminal open while the runner is needed. On GitHub, visit **Settings → Actions → Runners** and verify that the runner is **Online** and **Idle** when it is waiting for work.

- **Idle**: connected and waiting for a job.
- **Active**: currently executing a job.
- **Offline**: not connected or not running.


## 4. Configure a workflow job to use the runner

A job selects its runner through `runs-on`.

For this Windows runner, the job uses labels like:

```yaml
  runs-on: [self-hosted, Windows, X64]
```

The labels must match those shown for the registered runner in GitHub's runner settings. GitHub assigns the job only to an online runner that matches all requested labels.

You do not need to move every job to the self-hosted runner. Jobs can use different runners. In this project, only `convention-check` was switched; the other jobs can retain their existing `runs-on` values.

## 5. Current branch-name check

The `convention-check` job currently checks the pull request's source branch name. The PowerShell step is:

```yaml
- name: Check branch name
  shell: powershell
  env:
    BRANCH_NAME: ${{ github.head_ref }}
  run: |
    if ($env:BRANCH_NAME -notmatch '^feature/[a-z0-9]+(-[a-z0-9]+)*$') {
      Write-Error "Invalid branch name: $env:BRANCH_NAME"
      exit 1
    }

    Write-Host "Branch name is valid."
```

The pattern requires the branch name to:
- Start with `feature/`.
- Use lowercase letters and digits.
- Separate words with single hyphens.
- Contain no uppercase letters, underscores, or consecutive hyphens.

Examples:

| Branch name | Result |
|---|---|
| `feature/linting-pass` | Pass |
| `feature/add-banking-dag` | Pass |
| `feature/fix2-connection` | Pass |
| `Feature/add-banking-dag` | Fail |
| `feature/add_banking_dag` | Fail |
| `bugfix/fix-connection` | Fail |

The `github.head_ref` context contains the source branch name for a pull request. This workflow is intended for a `pull_request` event.

## 6. Why use `shell: powershell` on this runner?

The runner is Windows-based. The branch check uses Windows PowerShell syntax, so it explicitly declares:

```yaml
shell: powershell
```

This uses Windows PowerShell, which is available on standard Windows installations.

We initially tried Bash, but the runner selected `C:\Windows\System32\bash.exe`, and the temporary script path was not handled correctly. We then tried `pwsh`, but PowerShell 7 was not available (`pwsh: command not found`). Using `shell: powershell` resolved the issue.

If a workflow step uses Bash syntax, do not assume it will work in a Windows PowerShell step. Either adapt it to PowerShell or deliberately configure and test an appropriate Bash environment.

## 7. How to test the workflow

1. Make sure the runner is online.
2. Update the workflow file on your feature branch.
3. Commit and push the workflow changes.
4. Open or update a pull request targeting `main`.
5. Open the **Actions** tab and inspect the workflow run.
6. Confirm that **Branch Convention Check** runs on the self-hosted runner and passes for a valid branch name.

To test the invalid case, use a temporary test branch with a name that violates the rule, such as `test/invalid-name`, and open a pull request targeting `main`. The branch check should fail. Delete the temporary branch after testing.

Avoid renaming a shared branch or changing branch protection just to test the check. Ensure the test branch contains no real credentials or other sensitive data.

## 8. Troubleshooting

### Job remains queued

Check:
- The runner is online.
- The job's `runs-on` labels match the runner's labels.
- The runner is not already busy with another job.
- The repository or organization allows the runner to be used by this workflow.

### `pwsh: command not found`

PowerShell 7 is not installed or isn't available on `PATH`. For the current Windows runner, use `shell: powershell` if Windows PowerShell is installed.

### Bash script cannot find a temporary script path

The runner may be using a Bash executable that doesn't interpret the Windows path correctly. Confirm which Bash executable is selected and either configure a compatible Git for Windows Bash environment or convert the script to PowerShell. For the current branch-name check, PowerShell is the working solution.

### Branch check fails

Confirm that:
- The pull request targets `main`.
- The source branch starts with `feature/`.
- The remaining name uses lowercase letters or digits separated by single hyphens.
- The workflow uses `${{ github.head_ref }}` for the source branch name.

## 9. Security and maintenance

A self-hosted runner executes workflow code on a machine you manage. Treat it as a security-sensitive system.

- Prefer running workflows only for repositories and contributors you trust.
- Be cautious with workflows triggered by pull requests from forks or other untrusted contributors.
- Do not expose credentials, personal files, or production access to untrusted jobs.
- Keep the runner software and operating system updated.
- Keep the runner installation directory out of Git.
- Limit who can administer the runner and machine.
- Stop the runner when it is not needed, or configure it as a service according to your organization's policies.

A self-hosted runner is not a clean, disposable environment by default. Jobs may leave files or other changes on the machine, so use appropriate cleanup and access controls.

## 10. Quick checklist

- [ ] Runner is registered in **Settings → Actions → Runners**.
- [ ] Runner is online.
- [ ] `runs-on` labels match the runner's labels.
- [ ] `actions-runner/` is not committed to the repository.
- [ ] Windows-specific steps declare the correct shell.
- [ ] The workflow has been tested with a valid branch name.
- [ ] The workflow has been tested with an invalid branch name.
- [ ] Runner access and machine permissions follow team security requirements.

## Official documentation

- [Adding a self-hosted runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)
- [Using a self-hosted runner in a workflow](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow)
- [About self-hosted runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners)

