/* The actual sounds! */

SynthDef.new("background", { arg freq= 440, out = 0;
	/*
	Out.ar(out,
		//SinOsc.ar(freq, 0, 0.2)

	);
	*/
}).store;

SynthDef(\zep, {arg sr=40, v = 0.5, vibdc = 120, r = 0.1, vn = 0.02, v2 = 0.5, pan = 0, out = 0;
	y = FBSineL.ar(SampleRate.ir/sr) * v;
	z = SinOsc.ar(Vibrato.ar(DC.ar(vibdc),r,vn),0,v2 + 0.2);
	p = Pan2.ar(y+z, pan);
	Out.ar(out, p);
}).store;


SynthDef(\wind, {arg oscSpeed = 0.1, otherOsc = 400, out= 0, pan = 0;
	y = RLPF.ar(WhiteNoise.ar(), abs(SinOsc.ar(oscSpeed, 0, otherOsc)), 1);
	p = Pan2.ar(y, pan);
	Out.ar(out, p);
}).store;

SynthDef(\help_PlayBuf, {arg out = 0, bufnum = 0, volume = 1.0;
	p = Pan2.ar(PlayBuf.ar(1, bufnum, BufRateScale.kr(bufnum), loop: 1.0), 0, volume);
	Out.ar(out,p
    )
}).store;