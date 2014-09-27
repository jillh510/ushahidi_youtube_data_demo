/* Copyright (C) 2014, Jill Huchital
*/
// utility functions
//
//
//
//

function get_root_url() {
    return "http://127.0.0.1:5000";
}

function do_api_call(api_call, params, onReturn, onError) {
    var http = new XMLHttpRequest(),
        root_url = get_root_url(),
        stringified_params = JSON.stringify(params),
        url = root_url + "/api/1.0/" + api_call;

    http.open("POST", url, true);
    //Send the proper header information along with the request
    http.setRequestHeader("Content-type", "application/json");

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            if (onReturn) {
                onReturn(JSON.parse(http.responseText));
            }
        } else if (http.status != 200) {
            if (onError) {
                onError('Bad server call');
            }
        }
    }
    http.send(stringified_params);
}
