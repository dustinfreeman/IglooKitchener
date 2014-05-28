/*

Windows startup location
C:\\SuperCollider\\startup.scd (or similar, depending on the location of the SuperCollider installation)

Mac startup location
~/Library/Application Support/SuperCollider/startup.scd
*/

s = Server("caveServer", NetAddr("127.0.0.1", 57110));
s.addr; // returns the proper address
s.boot;
s.startAliveThread;
s.notify = true;
s.makeWindow;
s.initTree;
f = {Group.new(s.defaultGroup)};
ServerTree.add(f);
v = s.volume;
v.gui;

s.serverRunning;
	"~/path/to/repository/sounds.scd".standardizePath.load;
	"/path/to/repository/play.scd".standardizePath.load;
};

