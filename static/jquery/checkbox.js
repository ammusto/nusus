$(document).ready(function(){
    $('form[name="filter"]').submit(function(){
		if ($('input:checkbox').filter(':checked').length < 1){
        alert("Please select at least one filter!");
		return false;
		}
    });
});