$(document).ready(function() {
    $('#select-all').click(function() {
        var checked = this.checked;
        $('input[type=checkbox]').each(function() {
        this.checked = checked;
    });
    })
});