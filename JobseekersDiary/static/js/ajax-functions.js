$(document).ready(function () {

    var activitiesList = getActivitiesList();
    drawActivitiesTable(activitiesList);

    function drawActivitiesTable(activitiesList) {
        $.each(data, function (key, val) {
            console.log(data);
        });
    }

    function getActivitiesList() {
        $.ajax({
            url: '/api/rest/activities',
            type: 'GET',
            success: function (data) {
                return data;
            },
            error: function (error) {
                console.log(error);
            }
        });
    }

    $('button').click(function () {
        var company = $('#company_name').val();
        var position = $('#position_name').val();
        var date = $('#date').val();
        var description = $('#description').val();
        $.ajax({
            url: '/api/rest/activities',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

});