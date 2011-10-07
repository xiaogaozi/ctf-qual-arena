(function() {
    function getQuestions()
    {
        $.getJSON('/questions', function(data) {
            $('#questions').empty();

            var html = '\
<tr>\
    <th>Grab Bag</th>\
    <th>Retro Revisited</th>\
    <th>Binary L33tness</th>\
    <th>Pwtent Pwnables</th>\
    <th>Forensics</th>\
</tr>';

            $.each(data, function(i, qlist) {
                html += '<tr>';
                $.each(qlist, function(j, q) {
                    html += '<td class="' + q.class + '">' + q.score + '<span title="desc" style="display: none;">' + q.desc + '</span><span title="id" style="display: none;">' + q.id + '</span></td>';
                });
                html += '</tr>';
            });

            $('#questions').html(html);
        });
    }

    function getLeaders()
    {
        $.getJSON('/leaders', function(data) {
            $('#rank ol.leaders').empty();

            var html = '';
            $.each(data, function(i, team) {
                html += '<li>' + team.name + ' (' + team.score +')</li>';
            });

            $('#rank ol.leaders').html(html);
        });
    }

    $(document).ready(function() {
        getQuestions();
        setInterval(getQuestions, 30 * 60 * 1000);
        $('#questions td.open').live('click', function() {
            $('#questions td.selected').removeClass('selected');
            $(this).addClass('selected');
            $('#detail .desc p').html($(this).find('span[title="desc"]').html());
            $('#detail form input[name="q_id"]').attr('value', $(this).find('span[title="id"]').html());
        });
        getLeaders();
        setInterval(getLeaders, 60 * 60 * 1000);
    });
})();