# Lab 5 – Issue Table: `digital_wallet.py`

Line numbers refer to the **original** file. Ordered by severity (High → Low).

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Weak hash (SHA1) for PIN | Bandit B324 | Security | **High** | 14 | `hashlib.sha1` is broken for security use, and an unsalted hash of a 4-digit PIN can be reversed by trying all 10,000 PINs. | Replaced with salted `hashlib.pbkdf2_hmac("sha256", …, 100_000)`. |
| 2 | Insecure temp file (`mktemp`) | Bandit B306 | Security | **Medium** | 60 | `tempfile.mktemp` only returns a name; another process can create that file before we do (race condition, CWE-377). | Used `tempfile.mkstemp()`, which creates the file atomically; close the fd and return the path. |
| 3 | Mutable default argument | Pylint W0102 | Bug | **Medium** | 17 | `log=[]` is created once and shared across every call to `addMoney`, so amounts leak between calls. | Default changed to `None`, new list created inside the function. |
| 4 | Hard-coded secrets | Bandit B105 | Security | Low (sev) / Medium (conf) | 6–7 | Gateway key `sk_demo_wallet_0000` and plain PIN `4321` are in the source, so anyone with repo access has them. | Gateway key read from env var `WALLET_GATEWAY_SECRET`; the plain PIN is replaced by its stored PBKDF2 hash `WALLET_PIN_HASH`. Both comparisons use `hmac.compare_digest` (constant time). |
| 5 | Insecure random for OTP | Bandit B311 | Security | Low (sev) / High (conf) | 64 | `random.randint` is a predictable PRNG, unsuitable for a one-time password. | Replaced with `secrets.randbelow(900000) + 100000` (same 6-digit range). |
| 6 | Use of `global` | Pylint W0603 | Design | Medium | 28 | `setDailyLimit` mutates a module global, which makes state hard to track and test. | Moved the limit into the `wallet` dict (`wallet["daily_limit"]`); no `global` needed. |
| 7 | Unused argument `merchantType` | Pylint W0613 | Bug / Logic | Medium | 50 | `cashbackFor` takes a merchant type but ignores it, so the parameter has no effect. | Added a `CASHBACK_RATES` table looked up by merchant type, falling back to the 2% default, so the argument is now used and output is unchanged. |
| 8 | Non-snake_case names | Pylint C0103 | Style | Low | 9, 13, 17, 27, 32, 45, 50, 54, 58, 78 | camelCase functions/args/variables (`hashPin`, `addMoney`, `newLimit`, `creditAmounts`…) and lower-case "constant" `daily_limit`. | Renamed to snake_case (`hash_pin`, `add_money`, …); limit constant now `DEFAULT_DAILY_LIMIT`. |
| 9 | Missing docstrings | Pylint C0114 / C0116 | Style | Low | 1, 13–63 | No module docstring and none on the 9 functions. | Added a module docstring and one-line docstrings for every function. |
| 10 | Inline comment spacing | Flake8 E261 | Style | Low | 76 | Only one space before `# should be False`. | Two spaces before inline comment. |
| 11 | Missing whitespace around operator | Flake8 E225 | Style | Low | 78 | `creditAmounts=[...]`. | `credit_amounts = [...]`. |
| 12 | Missing whitespace after comma | Flake8 E231 | Style | Low | 79 | `"Total credited:",sum(...)`. | Added a space after the comma. |
| 13 | Blank lines / top-level call | Flake8 E305 | Style | Low | 80 | `main()` called right after a function with no blank lines, and it runs on import. | Two blank lines plus an `if __name__ == "__main__":` guard. |
| 14 | Line too long (introduced by fix #11) | Flake8 E501 | Style | Low | 78 | Adding spaces pushed the list comprehension to 80 chars. | Wrapped the comprehension over two lines. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.69 / 10 (25 messages) | **10.00 / 10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 4 issues | **0 issues** (empty report) |

The program's output is unchanged after the fixes (apart from the random OTP): same declines, mini statement, cashback 8.4, gateway check False, final balance Rs. 1900.0, total credited 2500.
