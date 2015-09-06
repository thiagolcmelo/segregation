var validaMuraki = function() {
    if (!$('#segregationCoefficient').val()) {
        $('#segregationCoefficient').focus();
        return false;
    } else if (!$('#concentration').val()) {
        $('#concentration').focus();
        return false;
    } else if (!$('#wellLength').val()) {
        $('#wellLength').focus();
        return false;
    } else if (!$('#rightBarrierLength').val()) {
        $('#rightBarrierLength').focus();
        return false;
    }
    return true;
};