# Git Fundamentals

A practical introduction to the core Git concepts you need before learning advanced Git and GitHub workflows.

---

## 1. What Git Is

**Git** is a distributed version control system (VCS).

It records changes to files over time so you can:

* Track what changed
* See when changes were made
* Go back to previous versions
* Work on different features safely
* Create branches
* Merge work together
* Collaborate with other developers

Git runs primarily on your computer and can work without GitHub or an internet connection.

### Example

Imagine you are building a Python project:

```text
my_project/
├── app.py
├── model.py
└── README.md
```

You modify `model.py`, then create a commit:

```bash
git add model.py
git commit -m "Improve model training"
```

Git records the state of the project at that point.

Later, you can inspect the history:

```bash
git log
```

---

# 2. Git vs GitHub

Git and GitHub are related, but they are **not the same thing**.

## Git

**Git is the version control system.**

It runs locally on your computer.

```text
Your Computer
      |
      v
     Git
      |
      +-- tracks files
      +-- creates commits
      +-- manages branches
      +-- stores history
```

## GitHub

**GitHub is an online platform for hosting Git repositories and collaborating around them.**

GitHub provides features such as:

* Remote repository hosting
* Pull requests
* Code review
* Issues
* GitHub Actions
* Releases
* Collaboration

You can use Git without GitHub.

You can also use Git with other platforms such as GitLab or Bitbucket.

### Simple distinction

```text
Git      = version control tool
GitHub   = online platform built around Git repositories
```

---

# 3. Version Control

**Version control** is the practice of recording changes to files so you can manage different versions of a project.

Without version control, you might create files like:

```text
project_final.py
project_final_v2.py
project_final_v3.py
project_final_really_final.py
```

With Git, you keep the project organized and Git records its history:

```text
Commit A
   |
   v
Commit B
   |
   v
Commit C
   |
   v
Commit D
```

Each commit represents a recorded state of the project.

### Why version control matters

Version control allows you to:

1. Track changes
2. Identify when a change happened
3. Understand what changed
4. Recover previous versions
5. Experiment safely using branches
6. Collaborate with other developers
7. Review changes before integrating them

---

# 4. Repository

A **repository**, commonly called a **repo**, is a project managed by Git.

A repository contains:

```text
Project files
+
Git metadata
+
Commit history
+
Branches
```

For example:

```text
my_project/
├── .git/
├── app.py
├── model.py
└── README.md
```

The hidden `.git` directory contains the Git information for the repository.

When you run:

```bash
git init
```

inside a project directory, Git creates the repository metadata.

### Important

The `.git` directory is extremely important.

Do not manually modify or delete it unless you intentionally want to remove the Git history.

---

# 5. Working Directory

The **working directory**, also called the **working tree**, is the actual set of files you are currently working on.

For example:

```text
my_project/
├── app.py
├── model.py
└── README.md
```

These files are part of your working directory.

If you edit:

```text
model.py
```

you have changed the working directory.

Git can detect this:

```bash
git status
```

You might see:

```text
modified: model.py
```

At this point, the change has **not been committed**.

---

# 6. Staging Area

The **staging area** is an intermediate area where you select which changes will be included in the next commit.

You add changes to the staging area using:

```bash
git add
```

For example:

```bash
git add model.py
```

The flow is:

```text
Working Directory
       |
       | git add
       v
Staging Area
```

You can stage several files:

```bash
git add app.py model.py README.md
```

Or stage all changes:

```bash
git add .
```

Then check the state:

```bash
git status
```

### Why does the staging area exist?

It allows you to choose exactly what goes into your next commit.

For example, suppose you changed:

```text
app.py
model.py
README.md
```

But you only want to commit `model.py`.

You can do:

```bash
git add model.py
git commit -m "Improve model training"
```

The changes in `app.py` and `README.md` remain in your working directory.

---

# 7. Local Repository

The **local repository** is the Git repository stored on your own computer.

It contains your local Git history, including:

* Commits
* Branches
* Tags
* Git metadata

Conceptually:

```text
Your Computer
└── my_project/
    ├── files
    └── .git/
         ├── commits
         ├── branches
         └── Git metadata
```

You can perform many Git operations without an internet connection:

```bash
git status
git diff
git log
git branch
git commit
```

For example:

```bash
git log
```

shows the commit history stored in your local repository.

---

# 8. Remote Repository

A **remote repository** is another copy of your Git repository that is stored somewhere else.

A common example is a repository hosted on GitHub.

```text
Your Computer                    GitHub
-------------                    ------
Local Repository  <---------->  Remote Repository
```

The conventional name for a remote is:

```text
origin
```

You can see your configured remotes with:

```bash
git remote -v
```

For example:

```text
origin  git@github.com:username/my_project.git
origin  git@github.com:username/my_project.git
```

You can send local commits to the remote repository with:

```bash
git push
```

You can retrieve changes from the remote with:

```bash
git fetch
```

You can commonly retrieve and integrate remote changes with:

```bash
git pull
```

### Important

A remote repository does **not** have to be on GitHub.

It can be hosted on:

* GitHub
* GitLab
* Bitbucket
* A company server
* Another Git hosting service

---

# 9. Commit

A **commit** is a recorded snapshot of changes in your Git repository.

A typical workflow is:

```bash
git add model.py
git commit -m "Improve model training"
```

The commit records information such as:

* The project state
* The changes being recorded
* Author
* Timestamp
* Commit message
* Unique commit hash
* Relationship to previous commits

A commit can be represented as:

```text
Commit
  |
  +-- hash
  +-- author
  +-- timestamp
  +-- commit message
  +-- project snapshot
```

You can inspect commits with:

```bash
git log
```

### Local commit vs remote commit

When you run:

```bash
git commit
```

the commit is created in your **local repository**.

It is not automatically sent to GitHub.

To send it to the remote repository:

```bash
git push
```

So:

```text
git commit
     |
     v
Local Repository

git push
     |
     v
Remote Repository
```

---

# 10. HEAD

`HEAD` is a special Git reference that tells Git **where your current checkout is positioned**.

In normal branch-based work, `HEAD` points to your current branch, and that branch points to the current commit.

For example:

```text
HEAD
 |
 v
main
 |
 v
C3
 |
 v
C2
 |
 v
C1
```

This means:

```text
HEAD → main → C3
```

You are currently on the `main` branch, at commit `C3`.

If you switch to another branch:

```bash
git switch feature-login
```

the structure may become:

```text
HEAD
 |
 v
feature-login
 |
 v
C5
```

Now `HEAD` points to `feature-login`.

### Why HEAD matters

Many Git commands use `HEAD` as a reference to your current position.

For example:

```bash
git show HEAD
```

shows the commit currently referenced by `HEAD`.

You can refer to the previous commit using:

```bash
HEAD~1
```

Two commits before:

```bash
HEAD~2
```

For example:

```bash
git show HEAD~1
```

means:

> Show the commit immediately before the current commit.

---

# 11. Branch

A **branch** is a movable reference to a commit that allows you to work on a separate line of development.

Suppose you have:

```text
A --- B --- C
             ^
            main
```

You create a new branch:

```bash
git switch -c feature-login
```

Now you might have:

```text
A --- B --- C
             ^
            main
              \
               D --- E
                    ^
             feature-login
```

You can work on `feature-login` without changing the `main` branch.

### Why use branches?

Branches are useful for:

* New features
* Bug fixes
* Experiments
* Refactoring
* Releases
* Isolated development

### Common branch commands

Create and switch to a new branch:

```bash
git switch -c feature-login
```

Switch to an existing branch:

```bash
git switch main
```

List branches:

```bash
git branch
```

Delete a merged local branch:

```bash
git branch -d feature-login
```

---

# 12. How Everything Connects

This is the most important Git mental model.

```text
                    GIT
                     |
        +------------+------------+
        |                         |
        v                         v
Working Directory          Local Repository
        |                         |
        | git add                 |
        v                         |
 Staging Area                    |
        |                         |
        | git commit              |
        +-----------------------> |
                                  |
                               Commits
                                  |
                               Branches
                                  |
                                 HEAD
                                  |
                                  | git push
                                  v
                           Remote Repository
                              (GitHub)
```

A normal Git workflow is:

```text
1. Edit files
       |
       v
2. Working Directory
       |
       | git add
       v
3. Staging Area
       |
       | git commit
       v
4. Local Repository
       |
       | git push
       v
5. Remote Repository
```

---

# 13. Example: Real Machine Learning Project

Suppose you have a project:

```text
bankAI/
├── src/
├── data/
├── tests/
├── README.md
└── requirements.txt
```

You modify:

```text
src/agent.py
```

## Step 1 — Check the state

```bash
git status
```

Git tells you that `src/agent.py` has changed.

---

## Step 2 — Review the change

```bash
git diff
```

This shows what you changed.

---

## Step 3 — Stage the change

```bash
git add src/agent.py
```

The change moves from:

```text
Working Directory
        ↓
Staging Area
```

---

## Step 4 — Check staging

```bash
git status
```

Now the file should appear under changes ready to be committed.

---

## Step 5 — Create a commit

```bash
git commit -m "Add financial agent tool"
```

The change is now recorded in your **local repository**.

---

## Step 6 — Push to GitHub

```bash
git push
```

Now the commit is sent to the **remote repository**.

---

# 14. The Three Main Areas

For Git fundamentals, memorize this model:

```text
┌─────────────────────────┐
│   WORKING DIRECTORY     │
│                         │
│   Files you edit        │
└────────────┬────────────┘
             │
          git add
             │
             v
┌─────────────────────────┐
│     STAGING AREA        │
│                         │
│ Changes selected for    │
│ the next commit         │
└────────────┬────────────┘
             │
         git commit
             │
             v
┌─────────────────────────┐
│    LOCAL REPOSITORY     │
│                         │
│ Local commit history    │
└────────────┬────────────┘
             │
          git push
             │
             v
┌─────────────────────────┐
│   REMOTE REPOSITORY     │
│                         │
│ GitHub / GitLab / etc.  │
└─────────────────────────┘
```

### Commands associated with each area

| Concept           | Important commands                      |
| ----------------- | --------------------------------------- |
| Working Directory | `git status`, `git diff`                |
| Staging Area      | `git add`, `git diff --staged`          |
| Local Repository  | `git commit`, `git log`, `git branch`   |
| Remote Repository | `git push`, `git fetch`, `git pull`     |
| Branch            | `git branch`, `git switch`, `git merge` |
| HEAD              | `git show HEAD`, `git diff HEAD`        |

---

# 15. Git Fundamentals Vocabulary

| Term                  | Meaning                                                           |
| --------------------- | ----------------------------------------------------------------- |
| **Git**               | Distributed version control system                                |
| **GitHub**            | Online platform for hosting and collaborating on Git repositories |
| **Version control**   | System for tracking and managing changes over time                |
| **Repository**        | Project managed by Git, including its history                     |
| **Working directory** | Files you are currently editing                                   |
| **Staging area**      | Changes selected for the next commit                              |
| **Local repository**  | Git repository stored on your computer                            |
| **Remote repository** | Repository stored somewhere else, often on GitHub                 |
| **Commit**            | Recorded snapshot of project changes                              |
| **HEAD**              | Reference to your current position in Git history                 |
| **Branch**            | Movable reference used for an independent line of development     |

---

# 16. What You Should Be Able to Explain

Before moving to advanced Git, you should be able to explain these concepts in your own words:

### Git

> What problem does Git solve?

### Git vs GitHub

> What is the difference between Git and GitHub?

### Repository

> What is a Git repository?

### Working Directory

> Where are the files that I am currently editing?

### Staging Area

> Why does Git have a staging area?

### `git add`

> What happens when I run `git add file.py`?

### Commit

> What happens when I run `git commit`?

### Local Repository

> Where is my commit stored after `git commit`?

### Remote Repository

> Where is the repository stored on GitHub?

### `git push`

> What happens when I run `git push`?

### HEAD

> What does `HEAD` represent?

### Branch

> Why would I create a branch?

git switch -c mlops

# work on your notebook
git add .
git commit -m "Add MLOps notes"

# later
git switch main
git merge mlops


If you understand this flow, you have the foundation for the next Git topics:

* `git status`
* `git diff`
* `git log`
* `git restore`
* `git reset`
* `git revert`
* Branching
* Merging
* Merge conflicts
* Remote workflows
* Pull requests
* GitHub Actions
* GitHub collaboration
