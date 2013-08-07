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
#define macro(x, y) return x + y

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
	}
/*
	blocks are not currently highlit correctly because the regex looks for braces
*/
	do_a_thing();

/*
	do/while loop
*/
		do {
			x++
		} while(y<100)


/*
	blocks are not currently highlit correctly because the regex looks for braces
*/
		sleep(10);
		spawn(20);
		//	world << "test"

/*
	for loop
*/
		for(var/x=0; x<100, x++)
			world << TRUE
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
	
	

