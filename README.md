replacemacros
=============

In a LaTeX document, replaces all occurences of your custom macros with their definitions. Useful if you are writing an article and no macros of your own are allowed.

usage: replacemacros inputfile [outputfile]

Scans the inputfile for \newcommand's and \def's, and then replaces occurences
of those commands in the body of text with their definitions. If no outputfile
is given, the result is printed in stdout.

Some restrictions:
- In lines that define commands, the last } of the line MUST be the end of the
  definition of the command.
- \def's with arguments are not supported, use \newcommand for those.
- In the body, when a command is used, its arguments MUST be given with {}
  around them.
- When using a command, angular braces are not allowed within required
  arguments, and square brackets are not allowed within optional arguments.

No guarantee of correctness of the output is guaranteed. Always check manually.
