function displayErrors(errors) {
    $('.errorlist').hide();
    $.each(errors, function(field, messages) {
        let errContainer = $("#id_" + field);
        let errorList = $("<ul>").addClass("errorlist");
        $.each(messages, function(index, message) {
            errorList.append("<li>" + message + "</li>");
        });
        errContainer.parent().append(errorList);
    });
}