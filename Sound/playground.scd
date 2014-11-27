ServerOptions.devices

//Server.local.options.device = "HDMI"
Server.local.options.sampleRate = 48000; // increase sampling rate (if your hardware supports it)
//Server.local.options.numOutputBusChannels = 30;
Server.local.boot

(
	SynthDef("tutorial-args", { arg freq = 440, out = 0;
		Out.ar(out, SinOsc.ar(freq, 0, 0.2));
	}).send(s);
)


(
o = 0;
x = Array.newClear(50);
y = Array.newClear(50);
while ({o < 30}, {
	"blah".postln;
	x[o] = Synth("tutorial-args", ["out", o, "freq", 660]);
	y[o] = Synth("tutorial-args", ["out", o, "freq", 770]);
	o = o + 1;
})

)

x = Synth("tutorial-args", ["out", 0, "freq", 660]);
y = Synth("tutorial-args", ["out", 0, "freq", 770]);
x = Synth("tutorial-args", ["out", 1, "freq", 660]);
y = Synth("tutorial-args", ["out", 5, "freq", 770]);
x = Synth("tutorial-args", ["out", 3, "freq", 660]);
y = Synth("tutorial-args", ["out", 3, "freq", 100]);

(
var speakerList, x=200, y=150, targx=200, targy=150;
var atorad = (2pi) / 360, rtoang = 360.0 / (2pi);
var targRotate, actRotate, targPoint, actPoint;
var maxShiftPerFrame = 20, frameInterval = 0.01;
var resched = false, count = 0;
var panBus, widthBus, recButton;
var a, b, c, e;

maxShiftPerFrame = maxShiftPerFrame * atorad;
actPoint = Point(x, y) - Point(200, 200);
panBus = Bus.control;
widthBus = Bus.control.set(60);

w = Window.new("5.1 Panner", Rect(128, 64, 400, 450)).front;
w.view.background_(Color.grey(0.3));
w.view.decorator = FlowLayout(w.view.bounds);
speakerList = [[-30, "L"], [30, "R"], [0, "C"], [-110, "Ls"], [110, "Rs"]];
c = UserView.new(w,Rect(0, 0, 400, 380));
c.canFocus = false;

c.drawFunc = {
	Color.grey(0.8).set;
	// draw the speaker layout
	Pen.translate(200,200);
	((actPoint.theta + (0.5pi)).wrap2(pi) * rtoang).round(0.01).asString.drawCenteredIn(Rect.aboutPoint(0@170, 30, 10), Font.new("Arial", 10), Color.grey(0.8));
	Pen.strokeOval(Rect.aboutPoint(0@0, 150, 150));
	Pen.rotate(pi);
	speakerList.do({|spkr|
		Pen.use({
			Pen.rotate(spkr[0] * atorad);
			Pen.moveTo(0@170);
			Pen.strokeRect(r = Rect.aboutPoint(0@170, 30, 10));
			if(spkr[0].abs < 90, {
				Pen.use({
					Pen.translate(0, 170);
					Pen.rotate(pi);
					spkr[1].drawCenteredIn(Rect.aboutPoint(0@0, 30, 10),
						GUI.font.new("Arial", 10), Color.grey(0.8));
				});
			},{
				spkr[1].drawCenteredIn(r, GUI.font.new("Arial", 10), Color.grey(0.8));
			});
		});

	});

	Pen.moveTo(0@0);

	// draw the pan point
	Pen.rotate(actPoint.theta + 0.5pi);
	targPoint = Point(x, y) - Point(200, 200);
	// trunc to avoid loops due to fp math
	targRotate = (targPoint.theta - actPoint.theta).trunc(1e-15);
	// wrap around
	if(targRotate.abs > pi, {targRotate = (2pi - targRotate.abs) * targRotate.sign.neg});
	actRotate = targRotate.clip2(maxShiftPerFrame).trunc(1e-15);
	actPoint = actPoint.rotate(actRotate);
	Pen.rotate(actRotate);
	Pen.lineTo(0@150);
	Pen.stroke;
	Pen.fillOval(Rect.aboutPoint(0@150, 7, 7));
	Pen.addWedge(0@0, 140, neg(e.value * 0.5) * atorad + 0.5pi, e.value * atorad);
	Pen.stroke;
	Color.grey(0.8).alpha_(0.1).set;
	Pen.addWedge(0@0, 140, neg(e.value * 0.5) * atorad + 0.5pi, e.value * atorad);
	Pen.fill;

	if((actRotate.abs > 0), {AppClock.sched(frameInterval, {w.refresh})}, {count = 0;});
	if(count%4 == 0, {panBus.set((actPoint.theta + (0.5pi)).wrap2(pi) * rtoang)});
};
c.mouseMoveAction_({|v,inx,iny| x = inx; y = iny; w.refresh;});
c.mouseDownAction_({|v,inx,iny| x = inx; y = iny; w.refresh;});
e = EZSlider.new(w, 380@20, "Stereo Width", [0, 180].asSpec, {arg ez; widthBus.set(ez.value); w.refresh}, labelWidth: 80);
e.labelView.setProperty(\stringColor,Color.grey(0.8));

w.refresh;

// VBAP

a = VBAPSpeakerArray.new(2, speakerList.collect(_.first));
b = a.loadToBuffer;

SynthDef('VBAP 5 chan', { |azi = 0, ele = 0, spr = 0, width = 60, vbapBuf|
var panned, source;
source = SinOsc.ar([440, 660], 0, Decay2.ar(Impulse.ar([1, 0.9]), 0.1, 0.2));
azi = azi.circleRamp;
panned = VBAP.ar(5, source, vbapBuf, [azi - (0.5 * width), azi + (0.5 * width)], ele, spr);
// 'standard' channel order for 5.1
[0, 1, 2, 4, 5].do({arg bus, i; Out.ar(bus, panned[0][i])});
[0, 1, 2, 4, 5].do({arg bus, i; Out.ar(bus, panned[1][i])});

}).play(s, [vbapBuf: b.bufnum, azi: panBus.asMap, width: widthBus.asMap]);

)