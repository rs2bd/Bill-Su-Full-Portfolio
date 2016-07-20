/**
 * Created by billsu on 11/4/15.
 */

function loadJSON(path) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                success(JSON.parse(xhr.responseText));
            }
            else {
                error(xhr);
            }
        }
    };
    xhr.open('GET', path, true);
    xhr.send();
}
