/* Lasor stuff*/

var lastUnit="";
function src_unit_update() {
	var u = document.getElementById("input_unit");

	console.log("Change from",lastUnit,"to",u.value);
}

function src_unit_focus() {
	var u = document.getElementById("input_unit");

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

function change_brightness() {
	var t = document.getElementById("input_brightness");
	var s = document.getElementById("input_brightness_slider");
	s.value = t.value;
}

function change_contrast() {
	var t = document.getElementById("input_contrast");
	var s = document.getElementById("input_contrast_slider");
	s.value = t.value;
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
