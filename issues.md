# Static Analysis Issues: online_exam.py

Baseline: Pylint 5.65/10, Bandit 4 issues (2 High, 2 Low), Flake8 4 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Starting a process with a shell (B605) | Security, High | 56 | `os.system("ssh " + labPc + ...)` builds a shell command from a variable, so command injection is possible | Replace with `subprocess.run(["ssh", lab_pc, "lock-screen"], check=True)` (no shell, argument list) |
| Weak MD5 hash (B324) | Security, High | 16 | `hashlib.md5` is a weak hash, and hashing is unnecessary just to compare answers | Remove hashing and compare normalized (stripped, lowercased) strings |
| Hardcoded password (B105) | Security, Low | 11 | `PROCTOR_PASSWORD = "proctor-demo"` stores a secret in source | Read it from an environment variable with `os.environ.get` |
| Weak PRNG (B311) | Security, Low | 20 | `random.choice` is not cryptographically secure | Use `secrets.choice` |
| Dangerous default value (W0102) | Bug, Pylint | 23 | `penalties={}` is created once and shared across calls, so state leaks between students | Default to `None` and create a new dict inside the function |
| Use enumerate (C0200) | Refactor, Pylint | 25 | `for i in range(len(QUESTIONS))` is unidiomatic | `for i, question in enumerate(QUESTIONS)` |
| Unnecessary elif after return (R1705) | Refactor, Pylint | 37 | `elif`/`else` after `return` is redundant | Use plain `if` statements and a final `return` |
| Invalid names (C0103) | Convention, Pylint | 15, 19, 23, 35, 45, 54 (functions); 23, 54 (args) | `hashAnswer`, `pickBonusQuestion`, `gradeStudent`, `getGrade`, `classAverage`, `lockScreen`, `studentName`, `labPc` are not snake_case | Rename to snake_case and update all call sites |
| Missing docstrings (C0114, C0116) | Convention, Pylint | 1, 15, 19, 23, 35, 45, 51, 54, 59 | Module and every function lack docstrings | Add short docstrings |
| Expected 2 blank lines (E302) | Style, Flake8 | 54 | Only 1 blank line before `lockScreen` | Add a second blank line |
| Missing whitespace around operator (E225) | Style, Flake8 | 67 | `average=classAverage()` | `average = class_average()` |
| Inline comment spacing (E261) | Style, Flake8 | 69 | Needs two spaces before `#` | Put two spaces before the comment |
| Line too long (E501) | Style, Flake8 | 70 | 93 characters, limit is 79 | Wrap the `print` call across two lines |

## Fix order (3 commits)

1. Bandit: lines 56, 16, 11, 20.
2. Pylint: names, docstrings, W0102, C0200, R1705.
3. Flake8: E302, E225, E261, E501.
