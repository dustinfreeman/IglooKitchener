/* The actual sounds! */

SynthDef.new("background", { arg freq= 440, out = 0;
	/*
	Out.ar(out,
		//SinOsc.ar(freq, 0, 0.2)

	);
	*/
}).store;

SynthDef(\zep, {arg sr=40, v = 0.01, vibdc = 120, r = 0.1, vn = 0.02, v2 = 0.01, pan = 0, out = 0;
	y = FBSineL.ar(SampleRate.ir/sr) * v;
	z = SinOsc.ar(Vibrato.ar(DC.ar(vibdc),r,vn),0,v2 + 0.2);
	p = Pan2.ar(y+z, pan);
	Out.ar(out, p);
}).store;


SynthDef(\wind, {arg oscSpeed = 0.001, otherOsc = 400, out= 0, pan = 0;
	y = RLPF.ar(WhiteNoise.ar(), abs(SinOsc.ar(oscSpeed, 0, otherOsc)), 1);
	p = Pan2.ar(y, pan);
	Out.ar(out, p);
}).store;

SynthDef(\help_PlayBuf, {arg out = 0, bufnum = 0, volume = 1.0;
	p = Pan2.ar(PlayBuf.ar(1, bufnum, BufRateScale.kr(bufnum), loop: 1.0), 0, volume);
	Out.ar(out,p
    )
}).store;


// Uncomment below to play with sounds

/*
z = Synth.new(\zep);

// SR is bassy stuff, range 35-180
z.set(\sr, 35);
z.set(\sr, 100);
z.set(\sr, 180);

// V is volume - 0.1 to 1.0
z.set(\v, 0.8);
z.set(\v, 0.1);
z.set(\v2, 0.1);

// VIBDC is I have no idea.
z.set(\vibdc, 1000)

// R is also no idea
z.set(\r, 100.0);

// VN is sounds a bit like the propeller, a bit dizzying, 0.02 to 0.5
z.set(\vn, 0.02);
z.set(\vn, 0.5);

// v2 is sets tonal quality, 0.5 sounds best
z.set(\v2, 0.5);

x = Synth.new(\wind);
x.set(\oscSpeed, 0.001);
x.set(\otherOsc, 3000);
*/
