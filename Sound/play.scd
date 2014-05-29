
var distanceVolumeI, chiI, sampleOne, sampleOneBuffer, sampleTwo, sampleTwoBuffer, sampleThree, sampleThreeBuffer, sampleFour, sampleFourBuffer, sampleSensitivity, windNoise;

/* Set the sensitivity for the distances to objects */
sampleSensitivity = 100000;


sampleOneBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "aalesund.wav");
sampleOne = Synth.new("\help_PlayBuf", [\out, 0, \bufnum, sampleOneBuffer]);

sampleTwoBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "fiercearcticwind.aif");
sampleTwo = Synth.new("\help_PlayBuf", [\out, 0, \bufnum, sampleTwoBuffer]);

sampleThreeBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "iceberg-fragment-svalbard.wav");
sampleThree = Synth.new("\help_PlayBuf", [\out, 0, \bufnum, sampleThreeBuffer]);

sampleFourBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "windwinter.wav");
sampleFour = Synth.new("\help_PlayBuf", [\out, 0, \bufnum, sampleFourBuffer]);

f = { |msg, time, addr|
	var distance, distanceVolume, distanceVolumeStep, dvi, caveheight, chiStep, chi, gas, brake;

	//msg.postln;
	gas = false;
	brake = false;

	case
	{msg[0] == '/DistToZep'} {
		// This is how far you are away from the zep. I get values 0 to 1
		"Got a position!".postln;
		msg.postln;
		//"Position time: % sender: %\nmessage: %\n".postf(time, addr, msg);
		//distance = msg[1].abs + msg[2].abs + msg[3].abs;
		distance = msg[1].abs;
		distance = linlin(msg[1], 0.0, 1.0, 180, 35);

		distanceVolume = distance;

		if (distanceVolumeI.isNil) {
			distanceVolumeI = 0;
		};

		distanceVolumeStep = (distanceVolume - distanceVolumeI)/90;
		dvi = distanceVolumeI;
		//"DVStep = %\n".postf(distanceVolumeStep);
		{
			90.do ({
				dvi = dvi + distanceVolumeStep;
				//s.sendMsg("/n_set", z, "v", dvi);
				//s.sendMsg("/n_set", z, "v2", dvi);
				//Uncomment this one
				//s.sendMsg("/n_set", z, "sr", dvi);
				//"Setting volume to % with step %\n".postf(dvi, distanceVolumeStep);
				0.01.wait;
			})
		}.fork;
		//z.set("v", distanceVolume);
		//z.set("v2", distanceVolume);
		distanceVolumeI = distanceVolume;

		"DV is now % and DVI is now %\n\n".postf(distanceVolume, distanceVolumeI);
	}

	{msg[0] == '/ZEPROTATION'} {
		//This is the zep rotation. I get values 0 - 1

		//"Got a rotation!".postln
		//"Rotation time: % sender: %\nmessage: %\n".postf(time, addr, msg);
	}


	{msg[0] == '/WindSpeed'} {
		//Wind speed. 0 - 1, usually less than 0.1, 1.0 is CRAZY.
		"Wind ".post;
		linlin(msg[1], 0.0, 1.0, 400, 3000).postln;
		s.sendMsg("/n_set", windNoise, "otherOsc", (linlin(msg[1], 0.0, 1.0, 400, 2000)));

	}

	// GasOn when gas is on, GasOff when gas is off, same with brakes.
/*
	{msg[0] == '/GasOn' } {
		if (gas == false) {
			gas = true;
			s.sendMsg("/n_set", z, "v", 0.03);
			s.sendMsg("/n_set", z, "v2", 0.03);
		}
	}

	{msg[0] == '/GasOff' } {
		if (gas == true) {
			gas = false;
			s.sendMsg("/n_set", z, "v", 0.01);
			s.sendMsg("/n_set", z, "v2", 0.01);
		}
	}

	{msg[0] == '/BrakeOn' } {
		if (brake == false) {
			brake = true;
			s.sendMsg("/n_set", z, "v", 0);
			s.sendMsg("/n_set", z, "v2", 0);
		}
	}

	{msg[0] == '/BrakeOff' } {
		if (brake == false) {
			brake = true;
			s.sendMsg("/n_set", z, "v", 0.01);
			s.sendMsg("/n_set", z, "v2", 0.01);
		}
	}
*/
	{msg[0] == '/DistToIceSheet'} {
		"Dist to ice sheet is %\n".postf(msg[1]);
		//linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0).postln;
		sampleOne.set("volume", (linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0)));

	}

	{msg[0] == '/DistToAbandoned'} {
		"Dist to abandoned is %\n".postf(msg[1]);
		//linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0).postln;
		sampleTwo.set("volume", (linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0)));

	}

	{msg[0] == '/DistToGlacier'} {
		"Dist to glacier is %\n".postf(msg[1]);
		//linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0).postln;
		sampleThree.set("volume", (linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0)));

	}
};

sampleOne.set("volume", 0.0);
sampleTwo.set("volume", 0.0);
sampleThree.set("volume", 0.0);
sampleFour.set("volume", 0.0);

thisProcess.addOSCRecvFunc(f);
//z = Synth.new(\zep);
//s.sendMsg("s_new", "zep", z = 1010, 0, 1);
//z.set(\v, 0.01);
//z.set(\v2, 0.01);
s.sendMsg("s_new", "wind", windNoise = 1012, 0, 1);

