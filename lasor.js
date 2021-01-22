/* Lasor stuff*/

var lastUnit="";

function round4(num) {
	return (Math.round((num + Number.EPSILON) * 10000) / 10000);
}

function round2(num) {
	return (Math.round((num + Number.EPSILON) * 100) / 100);
}

function src_unit_update() {
	var u = document.getElementById("input_unit");
	var w = document.getElementById("input_dest_width");
	var h = document.getElementById("input_dest_height");
	var dpi = document.getElementById("input_dpi").value;

	console.log("Change from",lastUnit,"to",u.value);
	if ((lastUnit == "centimeters") && (u.value == "pixels")) {
		w.value = Math.round((w.value / 2.54) * dpi);
		h.value = Math.round((h.value / 2.54) *dpi);
	}
	else if ((lastUnit == "pixels") && (u.value == "centimeters")) {
		w.value = round2(w.value / dpi * 2.54);
		h.value = round2(h.value / dpi * 2.54);
	}
	else if ((lastUnit == "pixels") && (u.value == "inches")) {
		w.value = Math.round(w.value / dpi);
		h.value = Math.round(h.value / dpi);
	}
	else if ((lastUnit == "inches") && (u.value == "pixels")) {
		w.value = round4(w.value * dpi);
		h.value = round4(h.value * dpi)
	}
	else if ((lastUnit == "inches") && (u.value == "centimeters")) {
		w.value = round2(w.value *2.54);
		h.value = round2(h.value *2.54)
	}
	else if ((lastUnit == "centimeters") && (u.value == "inches")) {
		w.value = round4(w.value /2.54);
		h.value = round4(h.value /2.54)
	}
	lastUnit=u.value;
}

function src_unit_focus() {
	var u = document.getElementById("input_unit");

	console.log("Focus got",u.value);
	lastUnit=u.value;
}
/*
 * Wood	Engrave	14%	350	0.085
 * Acrylic	Engrave	55%	300	0.065
 * Glass	Engrave	12%	462	0.055
 */
function change_res_type() {
	var u = document.getElementById("input_res_type").value;

	console.log("Res type is",u);
	var dpi = document.getElementById("input_dpi");
	var sg = document.getElementById("input_scangap");

	if (u=="wood") {
		dpi.value = 350;
		sg.value=0.085;
		dpi.setAttribute("readonly",true);
		sg.setAttribute("readonly",true);
	}
	else if (u=="glass") {
		dpi.value = 462;
		sg.value=0.055;
		dpi.setAttribute("readonly",true);
		sg.setAttribute("readonly",true);
	}
	else if (u=="acrylic") {
		dpi.value = 300;
		sg.value=0.065;
		dpi.setAttribute("readonly",true);
		sg.setAttribute("readonly",true);
	}
	else if (u=="custom") {
		dpi.removeAttribute("readonly");
		sg.removeAttribute("readonly");
	}

}

/* WHen we change the destination width, change the dest height, proportionaly */
function change_width() {
	var w = document.getElementById("input_width").value;
	var h = document.getElementById("input_height").value;
	var dw = document.getElementById("input_dest_width").value;
	var dh = document.getElementById("input_dest_height");

	dh.value = (h*dw/w)
}

/* WHen we change the destination height, change the dest width, proportionaly */
function change_height() {
	var w = document.getElementById("input_width").value;
	var h = document.getElementById("input_height").value;
	var dh = document.getElementById("input_dest_height").value;
	var dw = document.getElementById("input_dest_width");

	dw.value = (w*dh/h)
}
function change_brightness() {
	var t = document.getElementById("input_brightness");
	var s = document.getElementById("input_brightness_slider");
	s.value = t.value;
}

function change_black_threshold() {
	var t = document.getElementById("input_black_threshold");
	var s = document.getElementById("input_black_threshold_slider");
	s.value = t.value;
}

function change_white_threshold() {
	var t = document.getElementById("input_white_threshold");
	var s = document.getElementById("input_white_threshold_slider");
	s.value = t.value;
}

function change_contrast() {
	var t = document.getElementById("input_contrast");
	var s = document.getElementById("input_contrast_slider");
	s.value = t.value;
}

function change_threshold_slider() {
	var t = document.getElementById("input_threshold");
	var s = document.getElementById("input_threshold_slider");
	t.value = s.value;
}

function change_white_threshold_slider() {
	var t = document.getElementById("input_white_threshold");
	var s = document.getElementById("input_white_threshold_slider");
	t.value = s.value;
}

function change_black_threshold_slider() {
	var t = document.getElementById("input_black_threshold");
	var s = document.getElementById("input_black_threshold_slider");
	t.value = s.value;
}

function change_brightness_slider() {
	var t = document.getElementById("input_brightness");
	var s = document.getElementById("input_brightness_slider");
	t.value = s.value;
}

function change_contrast_slider() {
	var t = document.getElementById("input_contrast");
	var s = document.getElementById("input_contrast_slider");
	t.value = s.value;
}
function change_scangap() {
	var dpi = document.getElementById("input_dpi");
	var sg = document.getElementById("input_scangap");
	document.getElementById("input_res_type").value ="custom"

	dpi.value = 25.4/(sg.value);
}
function change_dpi() {
	var dpi = document.getElementById("input_dpi");
	var sg = document.getElementById("input_scangap");
	document.getElementById("input_res_type").value ="custom"

	sg.value = 25.4/(dpi.value);
}

function change_dither() {
	var d = document.getElementById("input_dither");
	var g = document.getElementById("threshold_group");
	console.log(d.value);
	if (d.value == "Simple BW Threshold") {
		g.style.display="flex";
	}
	else
		g.style.display="none";
}
