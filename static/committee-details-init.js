$( document ).ready(function() {
	$("#baseweight-display").knob({
		'draw' : function() {
			$(this.i).val(this.cv + '%')
		},
		width: 170, height: 170, readOnly: true, min: -100, max: 100, displayInput: true});
	$("#hsfweight-display").knob({
		'draw' : function() {
			$(this.i).val(this.cv + '%')
		},
		width: 130, height: 130, readOnly: true, min: -100, max: 100, displayInput: true});
	$("#usfweight-display").knob({
		'draw' : function() {
			$(this.i).val(this.cv + '%')
		},
		width: 130, height: 130, readOnly: true, min: -100, max: 100, displayInput: true});
});