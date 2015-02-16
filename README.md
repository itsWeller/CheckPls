# CheckPls
Some delicious py for dessert; a CSE 131 test script for Project 2.

CheckPls is a utility script that matches your code against testrunner_client's
to make testing just a little bit easier. Saves constant output for offline testing 
and throws whitespace, comments, and caution to the wind.

## Dependencies
Python 2.6+, diff
Only tested on OS X / *Nix, but it should work on Windows with some tweaking.

This depends on your code generator having the same logical structure as TRC's. You may 
generate perfectly valid and correct assembly and have this script reject you - don't take it personally. 

## Usage and Sample Output
``` sh
chrisweller at air in ~/Workspace/cse131 on develop!
± python checkPls.py proj2tests
[assy.rc]: Passed!
[compy.rc]: Passed!
[func.rc]: Passed!
-- [funk_basic.rc] Differences found:
	MY: set		0, %l7
	TR: set     	-4, %l7
[funk_basic.rc]: Failure.
[globret.rc]: Passed!
[if.rc]: Passed!
[iffy.rc]: Passed!
[iffy2.rc]: Passed!
-- [incy.rc] Differences found:
	MY: set		0, %l7
	TR: set     	-44, %l7
[incy.rc]: Failure.
-- [loopy.rc] Differences found:
	TR: ld      	[%l7], %l7
	TR: ld      	[%o1], %o1
[loopy.rc]: Failure.
[math.rc]: Passed!
[mathy.rc]: Passed!
[matlab.rc]: Passed!
-- [ret.rc] Differences found:
	MY: set		0, %l7
	TR: set     	-4, %l7
[ret.rc]: Failure.
[s1.rc]: Passed!
-- [s2.rc] Differences found:
	MY: set		0, %l7
	TR: set     	-24, %l7
[s2.rc]: Failure.
[sinny.rc]: Passed!
-- [var1.rc] Differences found:
	MY: set		0, %l7
	TR: set     	-28, %l7
[var1.rc]: Failure.

Testing completed successfully.
12/18 tests passing.
```
