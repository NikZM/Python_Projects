$(function() {
    $('button').click(function() {
        var company = $('#company_name').val();
        var position = $('#position_name').val();
        var date = $('#date').val();
        $.ajax({
            url: '/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});