# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues (E261, E225, E231, E305) and the Pylint naming and docstring warnings. They were mechanical: add a space, add two blank lines, rename `addMoney` to `add_money`. The mutable default argument (`log=[]` → `log=None`) was also quick once I understood that the list is created only once, when the function is defined.

The hardest were the security findings, because each one needed a design decision rather than a one-line edit:
- **Weak SHA1 PIN hash (B324):** switching to SHA-256 alone is not enough, because a 4-digit PIN has only 10,000 possibilities and could be brute-forced instantly. I used salted PBKDF2 with 100,000 iterations and stored only the hash, not the PIN.
- **Hard-coded gateway secret (B105):** moving it to an environment variable meant also deciding what happens when the variable is not set (the check now fails closed and returns `False`).
- **Unused `merchantType` argument:** I had to decide whether to delete the parameter or make it work. I kept it and added a per-merchant-type rate table with a 2% default, so the output did not change.

Fixing one tool's warning could also cause another's: adding spaces for E225 pushed a line to 80 characters and triggered a new E501, so the tools had to be rerun after each change.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Partly. The Bandit B105 warning was correct, but its scope was uneven. It flagged `GATEWAY_SECRET` because the name contains "secret", but it did **not** flag `WALLET_PIN = "4321"`, which is just as sensitive, because "PIN" is not in Bandit's keyword list. So it was a true positive on one line and a false negative on the next. It found the issue by matching names, not by understanding the code.

B306 (`mktemp`) was flagged in `receiptPath()`, which the demo never calls. The pattern is still unsafe, but in this program it cannot be reached, so its practical risk here is lower than its "Medium" severity suggests. Pylint's W0603 `global` warning is also a style/design judgment rather than a bug: the code worked correctly.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- **Locally:** run Flake8 and Pylint in the editor (VS Code extensions) for instant feedback, plus a **pre-commit hook** (`pre-commit` framework with flake8, pylint and bandit) so bad code is caught before it is committed.
- **In CI:** a GitHub Actions workflow on every push/pull request that runs all three tools and **fails the build** if Bandit finds any Medium/High issue, Flake8 reports anything, or the Pylint score drops below a threshold (for example `--fail-under=9.5`).
- **Configuration:** a shared `.pylintrc` / `setup.cfg` / `.bandit` in the repo so the whole team uses the same rules, and `# nosec` / `# pylint: disable=` only with a comment explaining why.
- **Secrets:** add a secret scanner (gitleaks or GitHub secret scanning), because Bandit only catches secrets whose variable names look suspicious.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Security:** the PIN is no longer stored in plain text and uses a slow, salted hash; PIN and gateway checks are constant-time (`hmac.compare_digest`); the OTP comes from a cryptographically secure generator; the temp file is created atomically; the gateway key is no longer in the source code.
- **Robustness:** the shared-list bug in `add_money` is gone. The daily limit is no longer a mutable global. The `if __name__ == "__main__":` guard means importing the module (for example from a test) no longer runs the demo and changes the wallet.
- **Readability:** consistent snake_case names, docstrings on every function, and PEP 8 formatting make the code easier to read and present.
- **Measured:** Pylint went from **5.69 to 10.00/10**, Bandit from **4 issues to 0**, Flake8 from **4 issues to 0**, and the program's output stayed the same.

One thing the tools did **not** flag: the balance is a `float`, which can cause rounding errors with money. A real wallet should use `decimal.Decimal` or integer paise. Static analysis catches many problems, but not all of them, so code review and testing are still needed.
