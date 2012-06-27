replacemacros
=============

In a LaTeX document, replaces all occurences of your custom macros with their definitions. Useful if you are writing an article and no macros of your own are allowed.

usage: replacemacros inputfile [outputfile]

Scans the inputfile for \newcommand's and \def's, and then replaces occurences
of those commands in the body of text with their definitions. If no outputfile
is given, the result is printed in stdout.

\def's with arguments are not supported, use \newcommand for those.

No guarantee of correctness of the output is guaranteed. Always check manually.
