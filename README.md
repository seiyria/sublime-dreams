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
* DMF files

Themes
======
We provide two themes: Dark Dreams and Light Dreams. Light Dreams is what a DM programmer is most familiar with - it's the exact same color scheme. Dark Dreams is a dark theme that matches DMs specific syntax, except in a dark theme.

Build System
============
The build system currently only has the option to build an individual file or an environment. It searches for an environment by checking each parent folder recursively until it finds a .dme file. If it does not find one, it will only compile the current file. If multiple environments are found in the same folder, the first one will be chosen.

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

Potential Future Features
=========================
*  Kill old DreamSeeker before compilation, and run a new DreamSeeker
*  Auto-reboot DreamDaemon on build
*  Auto-join DreamDaemon as self
*  Auto-join DreamDaemon with x keys/guests
