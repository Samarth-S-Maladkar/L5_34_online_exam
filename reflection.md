# Reflection

## 1. Which issues were the easiest and hardest to fix?
Easiest: Flake8 style issues (blank lines, spacing, line length, final
newline) and Pylint naming and docstrings, since they are mechanical.
Hardest: the Bandit findings, because they needed design decisions. I
replaced `os.system` with `subprocess.run` and an argument list, and
removed MD5 hashing instead of just swapping the algorithm. The mutable
default `penalties={}` was also subtle, since it caused shared state
between calls without any visible error.

## 2. Did the tools report any false positives?
Mostly no. B311 (`random.choice`) is low risk for picking a bonus
question, but I switched to `secrets.choice` anyway. After switching to
`subprocess.run`, Bandit raised B404/B603/B607 as low-severity warnings.
The call uses no shell and a fixed argument list, so I suppressed them
with `# nosec` and documented why. Those are judgement calls, not real
vulnerabilities.

## 3. How would you integrate static analysis into your workflow?
Run Flake8 and Pylint in the editor and in a pre-commit hook, and run all
three tools in CI (for example GitHub Actions) so a pull request fails if
Bandit finds high-severity issues or the Pylint score drops below a
threshold.

## 4. What improvements did you see?
Pylint went from 5.65/10 to 10.00/10, Bandit from 4 issues (2 High) to 0,
and Flake8 from 4 issues to 0. The program output stayed identical. The
code is more readable (snake_case, docstrings), safer (no shell injection,
no hardcoded password, no weak hash) and more robust (no shared mutable
default, `topper()` no longer crashes on empty results).