sublime-dreams
==============

A Sublime Text 2 Theme/Build System for Dream Maker (http://byond.com)

Highlighting
============
Currently correctly highlighting:
* All language keywords
* Pre-processor macros
* Strings (single and double quote)
* Proc names (including built-in procs)
* Numeric variables
* Built-in functions
* Language constants
* Embedded expressions
* Operators (most themes ignore these)

The theme that works best (according to the few I tried) is Sunburst.

Build System
============
A build system is included that, at the moment, compiles the currently opened .dm file into a .dmb. It also supports running the .dmb in Dream Seeker, or opening it in Dream Daemon so you can run it from there. It does not support compiling an entire environment yet.

Snippet Autocompletion
======================

Currently supported are:

def\<tab> 
expands to:

```
#ifndef SYMBOL
#define SYMBOL value
#endif
```

if\<tab>
expands to:
```
if (/* condition */)
	/* code */
```

do\<tab>
expands to:
```
do
	/* code */
while (/* condition */);
```

for\<tab>
expands to:
```
for (var i = 0; i < count; ++i)
	/* code */
```

forin\<tab>
expands to:
```
for (var i in 1 to count)
	/* code */
```

forinstep\<tab>
expands to:
```
for (var i in 1 to count step 2)
	/* code */
```

To make the most of the snippet auto-completion, after the initial tab, keep hitting tab to change positions.

Got useful snippets? Send a pull request!