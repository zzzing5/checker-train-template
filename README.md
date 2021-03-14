# checker-train-template
Template repository for university class on writing A/D CTF checkers

## Checker API
Checker is an app that checks whether the team's task is running normally, puts flags and then checks them after a few rounds.

Actions and arguments are passed to checker as command-line arguments, the first one is always command type, the second is team host.

Checker should terminate with one of the five return codes:

- `101`: `OK` code, everything works
- `102`: `CORRUPT`, service's working correctly, but didn't return flags from previous rounds (returned by GET only)
- `103`: `MUMBLE`, service's not working correctly
- `104`: `DOWN`, could not connect normally
- `110`: `CHECKER_ERROR`, unexpected error in checker
All other return codes are considered to be `CHECKER_ERROR`.

In case of unsuccessful invocation stderr output will be shown on admin section of the checksystem.

**Checker must implement three main actions:**

#### CHECK
Checks that team's service is running normally. Visits some pages, checks registration, login, etc...

Example invocation: `/checkers/task/check.py check 127.0.0.1`

#### PUT
Puts a flag to the team's service.

Example invocation: `/checkers/task/check.py put 127.0.0.1 <flag_id> <flag> [vuln_number]`

If checker returns anything to stdout with `101` exit code, it will be treated as new `flag_id` and will be passed
to all furhter `GET` invocations for currect flag. Returned string could contain arbitrary data including spaces and
newlines. Regardles of the form, it will be placed to `argv[3]`. It's a prefered way to store some usefull data related to the 
stored flag like logins, passwords, tokens, etc.

#### GET
Fetches one random old flag from last flag_lifetime rounds. This action should check if the flag can be acquired correctly.

Example invocation: `/checkers/task/check.py get 127.0.0.1 <flag_id> <flag> [vuln_number]`

