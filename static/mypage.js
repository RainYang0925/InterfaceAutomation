$(document).ready(function() {
    var message = $('<div></div>');
    var hide_link = $('<a>隐藏</a>');
    var atag = $('<a></a>');
    atag.attr('href', '#message');
    message.attr('id', 'message');
    hide_link.css('display', 'none');
    hide_link.attr({
      id: 'hide_link',
      href: ''
    });
    //note.insertBefore('table');
    $(document.body).append(hide_link);
    $(document.body).append(message);
    $("td").bind('click', function(event) {
      $(this).append(atag);
      message.text($(this).text());
      hide_link.show();
      message.show();
    });

    $("#hide_link").bind('click', function(event) {
        message.hide();
        hide_link.hide();
        return false;
    });
//--------------------echarts------------------------------
    mychart = echarts.init(document.getElementById('summarypic'));
    var successNum = $('#success').text();
    var failNum = $('#fail').text();
    var errorNum = $('#error').text()
    var option = {
        title : {
            text : ""
        },
        tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b} : {c} ({d}%)"
        },
        legend:{
            zlevel:10
        },
        series : [
        {
            name: 'case概要',
            type: 'pie',
            radius: '75%',
            data:[
                {value:successNum, name:'成功数'},
                {value:failNum, name:'失败数'},
                {value:errorNum, name:'错误数'}
            ].sort(function (a, b) { return a.value - b.value})
        }
    ]
}
    mychart.setOption(option);
//-----------------------echarts------------------------------
//---------------------------DataTables---------------------------------
    $('#detailtable').DataTable({
        "order": [6, 'asc'],
        "processing": true,
    });

//---------------------------DataTables end---------------------------------
});





