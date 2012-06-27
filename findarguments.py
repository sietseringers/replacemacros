#!/usr/bin/python

import sys, os, optparse, re
import pprint
from functools import partial

pp = pprint.PrettyPrinter(indent=4)

# 
def findarguments(text, argscount=0, startpos=0):
	"""Find the arguments given to a macro in given text.

	Optional arguments must always be enclosed between square brackets, but
	required arguments need not be. This command assumes that all command names
	consist only of letters (lower- and uppercase). Comments within the arguments
	are not allowed.

	Arguments:
	text -- the text to find the arguments in
	argscount -- the number of required arguments that the argument will take
	startpos -- the starting position of the first argument, i.e. the position
	            of the first character after the name of the array."""

	args = []

	start = 0
	end = 0
	count = 0
	reqargscount = 0
	kind = ''
	close = ''

	i = startpos

	# We loop through the text, one character at a time, and we look for:
	# - commands, i.e. \foobar. These are considered to be single required
	#   arguments.
	# - single characters. These are again considered to be single required
	#   arguments.
	# - anything within {} or [].
	# We do this until the end of the text is reached; or until the maximum
	# number of required arguments has been reached (perhaps including an
	# optional argument before we exit the loop). We ignore whitespaces occuring
	# between arguments.
	while i < len(text):
		# We're between arguments and encountered a space; ignore it
		if count == 0 and re.match(r'\s', text[i]):
			i += 1
			continue

		# We're between arguments and encounter a \ : this means the next argument
		# is a required one, consisting of a macro, without any curly braces
		# around it. We consider it in its entirety to be the next argument.
		if count == 0 and text[i] == '\\':
			match = re.match(r'(\\[a-zA-Z]*)', text[i:])
			# Set the position to after the command, minus one, because i += 1
			# at the end of the while loop
			i += match.end() - 1

			# We have to go through at least one iteration of attempting to find
			# arguments, even if the maximum number of required arguments already
			# has been found, because the first argument may be an optional one.
			# Thus, if we have found something that seems to be a required
			# argument, store it only when we still need to find more required
			# arguments.                                                     (*)
			if reqargscount < argscount:
				arg = {'text': match.group(1), 'required': True }
				args.append(arg)
				reqargscount += 1
				end = i

		# We're between arguments, and the next character is not a space or a
		# backslash. If it is also not an opening brace, then this means it is
		# an ordinary character. We consider this character to be the required
		# argument
		elif count == 0 and text[i] != '[' and text[i] != '{':
			if reqargscount < argscount: # See (*)
				arg = {'text': text[i], 'required': True }
				args.append(arg)
				reqargscount += 1
				end = i

		# We found an opening bracket
		if text[i] == '[' or text[i] == '{':
			if count == 0: # We are between arguments and have found a new one
				#print "Open bracket found: %d %s" % (i, text[i])
				start = i
				close = ']' if text[start] == '[' else '}'
			# If we find the same bracket again, increase the counter.
			if text[i] == text[start]:
				count += 1

		# We found a closing bracket
		if text[i] == close:
			count -= 1
			if count == 0: # Last bracket found; end of the argument
				#print "Close bracket found: %d %s" % (i, text[i])
				arg = {'text': text[start+1:i], 'required': False if text[start] == '[' else True }
				if arg['required'] and reqargscount < argscount: # See (*)
					reqargscount += 1
					args.append(arg)
					end = i
				elif not arg['required']:
					args.append(arg)
					end = i

		# We have found all required arguments; we're done
		if count == 0 and reqargscount == argscount:
			break

		i += 1

	#pp.pprint(args)
	return (args, end + 1)
