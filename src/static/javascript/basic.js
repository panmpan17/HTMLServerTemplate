BASIC_JS_LOADED = true;

// Form Handling
function GetFormFieldsData(formEle) {
    var data = {};

    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT" || tagName == "TEXTAREA") {
            var field = ele.attributes.getNamedItem("field");

            if (field != null) {
                if (ele.value == "")
                    return null;

                data[field.value] = ele.value;
            }
        }
        else {
            var field = ele.attributes.getNamedItem("field");
            var contentEditable = ele.attributes.getNamedItem("contenteditable");

            if (field != null && contentEditable != null) {
                data[field.value] = ele.innerHTML;
            }
        }
    }

    return data;
}

function FillFormFieldswithData(formEle, data) {
    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT" || tagName == "TEXTAREA") {
            var field = ele.attributes.getNamedItem("field");

            if (field != null) {
                if (data[field.value] != undefined)
                    ele.value = data[field.value];
            }
        }
    }
}

function ClearFormField(formEle) {
    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT" && ele.type != "submit")
            ele.value = "";
        else if (tagName == "TEXTAREA")
            ele.value = "";
        else {
            var contentEditable = ele.attributes.getNamedItem("contenteditable");

            if (contentEditable != null) {
                ele.innerHTML = "";
            }
        }
    }
}


// Restful API
class HTTPResponse {
    constructor(status, responseText) {
        this.status = status;
        this.responseText = responseText;
    }

    jsonlizeResponse() {
        try {
            return JSON.parse(this.responseText);
        }
        catch (e) {
            return null;
        }
    }
}


function stringlizeDictionary(/*Dictionary*/ data) {
    var texts = [];

    for (var key in data) {
        texts.push(`${key}=${encodeURI(data[key])}`);
    }

    return texts.join("&");
}

function Get({ url, data, success, error }) {
    var request = new XMLHttpRequest();
    request.addEventListener("load", function () {
        if (this.status >= 400) {
            if (error != null) error(new HTTPResponse(this.status, this.responseText));
        }
        else {
            if (success != null) success(new HTTPResponse(this.status, this.responseText));
        }
    });
    request.addEventListener("error", function () {
        error(new HTTPResponse(this.status, this.responseText));
    });

    if (data != null) {
        var key = GetCookie("key");
        if (key != "") data.key = key;
        url += "?" + stringlizeDictionary(data);
    }

    request.open("GET", url, true);
    request.send();
}

function Post({ url, data, success, error }) {
    var request = new XMLHttpRequest();
    request.addEventListener("load", function () {
        if (this.status >= 400) {
            if (error != null) error(new HTTPResponse(this.status, this.responseText));
        }
        else {
            if (success != null) success(new HTTPResponse(this.status, this.responseText));
        }
    });
    request.addEventListener("error", function () {
        error(new HTTPResponse(this.status, this.responseText));
    });

    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    if (data != null) {
        var key = GetCookie("key");
        if (key != "") data.key = key;
    }
    request.send(JSON.stringify(data));
}

function Put({ url, data, success, error }) {
    var request = new XMLHttpRequest();
    request.addEventListener("load", function () {
        if (this.status >= 400) {
            if (error != null) error(new HTTPResponse(this.status, this.responseText));
        }
        else {
            if (success != null) success(new HTTPResponse(this.status, this.responseText));
        }
    });
    request.addEventListener("error", function () {
        error(new HTTPResponse(this.status, this.responseText));
    });

    request.open("Put", url, true);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    if (data != null) {
        var key = GetCookie("key");
        if (key != "") data.key = key;
    }
    request.send(JSON.stringify(data));
}

function Delete({ url, data, success, error }) {
    var request = new XMLHttpRequest();
    request.addEventListener("load", function () {
        if (this.status >= 400) {
            if (error != null) error(new HTTPResponse(this.status, this.responseText));
        }
        else {
            if (success != null) success(new HTTPResponse(this.status, this.responseText));
        }
    });
    request.addEventListener("error", function () {
        error(new HTTPResponse(this.status, this.responseText));
    });

    if (data != null) {
        var key = GetCookie("key");
        if (key != "") data.key = key;
        url += "?" + stringlizeDictionary(data);
    }

    request.open("DELETE", url, true);
    request.send();
}


// Cookies
function StoreCookie(name, value, expires = "", path = "/") {
    if (expires == "") expires = "Session";
    else {
        var today = new Date();
        today.setDate(today.getDate() + expires);
        expires = today.toUTCString();
    }

    document.cookie = `${name}=${value}; expires=${expires}; path=${path}`;
}

function GetCookie(name) {
    name += "=";

    var ca = document.cookie.split(';');

    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }

    return "";
}

function DeleteCookie(name, path = "/") {
    document.cookie = `${name}=; expires= Thu, 01 Jan 1970 00:00:00 GMT; path=${path}`;
}

// Date
function ParseDatetime(data) {
    var now = new Date();
    return new Date(data * 1000 - (now.getTimezoneOffset() * 60 * 1000))
}

function GetUrlParams() {
    var paramsString = location.search.replace("?", "").split("&");
    var params = {};

    for (var paramString of paramsString) {
        var index = paramString.indexOf("=");
        params[paramString.substring(0, index)] = decodeURIComponent(paramString.substring(index + 1));
    }

    return params;
}

(function () {
    document.dispatchEvent(new CustomEvent("basic_js_loaded"));
})();