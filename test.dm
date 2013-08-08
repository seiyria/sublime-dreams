/*
	TODO
		-highlight built in procs/keywords (like world)
		-embedded expressions should highlight the embedded expression as a deeper color
		-escaped brackets should not be highlit
		-leftmost expressions (like /datum) that aren't already a keyword
		-parameter highlighting
*/

// this is a test file to make sure the DM syntax is correctly highlighted

/*
	this is a multi line comment
	it has multiple lines
	it also has some keywords in it like for, to, do
	and some comment starters! /*
*/

//warning macro
#warning TEST

//macro functions
#define test cake
#define MACRO(x, y) return x + y

//nested macros
#ifdef test
	#define cake 2
#endif

/*
	variables
		global
		const

		string
			double quote
			single quote
		number (all numbers (integers, decimals) should be hilighted. However, in DM the negative symbol in negs is not; things like 1.#INF, where only the 1 is hilighted)
*/
var
	global
		x = 500  
	const
		y = "test string"

	icon = 'test icon'

/*
top level type definition
	variables
		list
		new objects

	procs
		proc name
*/
datum
	var
		//is this even allowed in DM?
		t = 0xBEEFFACE
		u = 01000
		y = x ? z
		test = new list()
		obj/cake/pie = new()

	proc
		functionName(x, y, defaultArg = 1) {
			return 5
		}

proc

/*
	a proc with braces
*/
	braced_function() {

/*
	function call with semicolon
*/
		sleep(20);
/*
	do/while loop in braces
*/
		do {
			x++
		} while(y<100)
	}
/*
	blocks are not currently highlit correctly because the regex looks for braces
*/
	do_a_thing()

/*
	do/while loop
*/
		do
			x++
		while(y < 100)

/*
	constants checking
*/
		var
			x = SOUTHEAST
			y = UP
			z = BLIND
			a = SEE_MOBS
			b = SEE_OBJS
			c = SEEINVIS
			d = MOB_PERSPECTIVE
			e = EYE_PERSPECTIVE
			f = FLOAT_LAYER
			g = EFFECTS_LAYER
			h = TOPDOWN_MAP
			i = ISOMETRIC_MAP
			j = NO_STEPS
			k = FORWARD_STEPS
			l = MALE
			m = FEMALE
			n = MOUSE_INACTIVE_POINTER
			o = MOUSE_ACTIVE_POINTER
			p = MOUSE_DRAG_POINTER
			q = MOUSE_LEFT_BUTTON
			r = MOUSE_RIGHT_BUTTON
			s = MOUSE_CTRL_KEY
			t = MOUSE_SHIFT_KEY
			u = CONTROL_FREAK_ALL
			v = CONTROL_FREAK_SKIN
			w = MS_WINDOWS
			xx = ASSERT
			yy = SOUND_MUTE
			zz = SOUND_PAUSED
			aa = ICON_ADD
			bb = ICON_AND
			cc = ICON_OVERLAY
			dd = ICON_UNDERLAY


/*
	blocks are not currently highlit correctly because the regex looks for braces
*/
		sleep(10)
		spawn(20)

/*
	for loop
*/
		for(var/x=0; x<100, x++)
			world << TRUE
			src << x
			usr << "a string!"
/*
	for loop with to/step, step should only be hilighted in the case it's after "for("
*/
		for(var/x=1 to 10 step 4)

/*
	switch statement
*/
			switch(x)
/*
	break from switch
*/
				if(1) break
				if(2) world << "never happens"
/*
	cases that aren't supposed to highlight
*/
				default
				case
/*
	text macros
*/
			world << "\r \n"
/*
	while loop
*/
		while(TRUE)
			world << "this is the song that never ends!"
/*
	return statement
*/
		return 5
/*
	text document syntax
*/
        world << {"poop
        	poop
        	poop"}
/*	
	escaped line end
*/
	world << "poop \
		poop"
	
/*
	embedded expressions 
*/
	world << "poop: [x]"
/*
	escaped things
*/
	world << "poop: \[x]" // only first bracket cancels the expression
	world << "poop \"hi\" " //both quotes have to be escaped
