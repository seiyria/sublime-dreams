sublime-dreams
==============

A Sublime Text 2 Theme/Build System for Dream Maker (http://byond.com)


Highlighting
============
It highlights a lot of things.

Build System
============
There is currently no build system in place.

Snippet Autocompletion
======================

Currently supported are:

def<tab> 
expands to:

```
#ifndef SYMBOL
#define SYMBOL value
#endif
```

do<tab>
expands to:
```
do

	/* code */
while (/* condition */);
```

for<tab>
expands to:
```
for (var i = 0; i < count; ++i)
```

forin<tab>
expands to:
```
for (var i in 1 to count)
```

forinstep<tab>
expands to:
```
for (var i in 1 to count step 2)
```