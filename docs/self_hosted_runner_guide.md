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

You do not need to move every job to the self-hosted runner. Jobs can use different runners.

## 5. How to test the workflow

1. Make sure the runner is online.
2. Update the workflow file on your feature branch.
3. Commit and push the workflow changes.
4. Open or update a pull request targeting `main`.
5. Open the **Actions** tab and inspect the workflow run.
6. Confirm that Check runs on the self-hosted runner and passes for a valid branch name.

## 8. Troubleshooting

### Job remains queued

Check:
- The runner is online.
- The job's `runs-on` labels match the runner's labels.
- The runner is not already busy with another job.
- The repository or organization allows the runner to be used by this workflow.

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
- [ ] Runner access and machine permissions follow team security requirements.

## Official documentation

- [Adding a self-hosted runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)
- [Using a self-hosted runner in a workflow](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow)
- [About self-hosted runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners)

