$(document).ready(function () {
    $('input[title!=""]').hint();
    $('.example').click(function(){
        $('#URI_input').attr('value',$(this).text());
    });
    
    $('.panel-toggle-collapse').click(function(){
        $(this).parent().next().slideToggle('fast');
        $(this).toggleClass('panel-toggle-collapse').toggleClass('panel-toggle-expand');
    });
    
    $('.show-more').click(function(){
        $(this).parent().next('.more').toggle();
        $(this).toggleClass('show-more-label').toggleClass('hide-more-label');
        if($(this).hasClass('show-more-label')) {
            $(this).html('Show more...');
        } else {
            $(this).html('Hide more...');
        }
    });
    
    $(function() {
        var found_obj = $('#result_string:contains("a Real World Object")');
        var found_doc = $('#result_string:contains("a Document")');
        if(found_obj.length==1){   
            $("#result-icon").html('<img src="/static/images/icon-objects.png" />');      
        } else if(found_doc.length==1){   
            $("#result-icon").html('<img src="/static/images/icon-documents.png" />');      
        } else {
            $("#result-icon").html('<img src="/static/images/icon-warning-big.png" />');
        }

    });
});