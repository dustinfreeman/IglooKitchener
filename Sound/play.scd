
var distanceVolumeI, chiI, sampleOne, sampleOneBuffer, sampleTwo, sampleTwoBuffer, sampleThree, sampleThreeBuffer, sampleFour, sampleFourBuffer, sampleSensitivity;

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
	var distance, distanceVolume, distanceVolumeStep, dvi, caveheight, chiStep, chi;

	//msg.postln;
	case
	{msg[0] == '/DistToZep'} {
		//"Got a position!".postln;
		//"Position time: % sender: %\nmessage: %\n".postf(time, addr, msg);
		//distance = msg[1].abs + msg[2].abs + msg[3].abs;
		distance = msg[1].abs;
		//"Total pre-distance is: %\n".postf(distance);
		distance = distance / 350000;
		distanceVolume = 1.0 - distance;

		if (distanceVolume < 0) {
			distanceVolume = 0.0;
		};

		//"Total distance is: %\n".postf(distance);
		"Setting volume to: % from %\n".postf(distanceVolume, distanceVolumeI);
		if (distanceVolumeI.isNil) {
			distanceVolumeI = 0.5;
		};

		distanceVolumeStep = (distanceVolume - distanceVolumeI)/90;
		dvi = distanceVolumeI;
		//"DVStep = %\n".postf(distanceVolumeStep);
		{
			90.do ({
				dvi = dvi + distanceVolumeStep;
				//z.set("v", dvi);
				//z.set("v2", dvi);
				s.sendMsg("/n_set", z, "v", dvi);
				s.sendMsg("/n_set", z, "v2", dvi);
				//"Setting volume to % with step %\n".postf(dvi, distanceVolumeStep);
				0.01.wait;
			})
		}.fork;
		//z.set("v", distanceVolume);
		//z.set("v2", distanceVolume);
		distanceVolumeI = distanceVolume;

		"DV is now % and DVI is now %\n\n".postf(distanceVolume, distanceVolumeI);
	}

	{msg[0] == '/CAVEPOS'} {
		caveheight = msg[2];
		caveheight = (caveheight / 150);
		//caveheight = 100 - caveheight;
		"Height is now % and it was before %\n".postf(caveheight, msg[2]);

		if (chiI.isNil) {
			chiI = 0.5;
		};

		chiStep = (caveheight - chiI)/90;
		chi = chiI;
		//"DVStep = %\n".postf(distanceVolumeStep);
		{
			90.do ({
				chi = chi + chiStep;
				s.sendMsg("/n_set", z, "sr", chi);
				//"Setting frequency to % with step %\n".postf(chi, chiStep);
				0.01.wait;
			})
		}.fork;
		chiI = caveheight;

		// Unocmment this and comment out the stuff about steps above to get back to nonsmooth
		//s.sendMsg("/n_set", z, "sr", caveheight);
	}

	{msg[0] == '/DistToIceSheet'} {
		"Dist to ice sheet is %\n".postf(msg[1]);
		linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0).postln;
		sampleOne.set("volume", (linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0)));

	}

	{msg[0] == '/DistToAbandoned'} {
		"Dist to abandoned is %\n".postf(msg[1]);
		linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0).postln;
		sampleTwo.set("volume", (linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0)));

	}

	{msg[0] == '/DistToGlacier'} {
		"Dist to glacier is %\n".postf(msg[1]);
		linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0).postln;
		sampleThree.set("volume", (linlin(msg[1], 0.00, sampleSensitivity, 1.0, 0.0)));

	}

	{msg[0] == '/ZEPROTATION'} {
		//"Got a rotation!".postln
		//"Rotation time: % sender: %\nmessage: %\n".postf(time, addr, msg);
}};

sampleOne.set("volume", 0.0);
sampleTwo.set("volume", 0.0);
sampleThree.set("volume", 0.0);
sampleFour.set("volume", 0.0);

thisProcess.addOSCRecvFunc(f);
//z = Synth.new(\zep);
s.sendMsg("s_new", "zep", z = s.nextNodeID, 0, 1);

