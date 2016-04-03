function format_json_string(string) {
    return string
        .trim()
        .replace(/(\r\n|\n|\r)/gm, "")
        .replace(/"/gm, "'");
}

function escape_backslash(string) {
    return string
        .replace(/([^\\])\\([^\\])/gm, "$1\\\\$2");
}