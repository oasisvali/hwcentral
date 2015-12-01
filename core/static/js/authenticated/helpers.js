function extract_id(dom_obj) {
    var id = dom_obj.text().trim();
    if (isNaN(id)) {
        console.error("The extracted id is not a number! HOLDER ->");
        console.error(dom_obj);
        return null;
    }
    return id;
}

function extract_text(dom_obj) {
    var text = dom_obj.text().trim();
    if (text) {
        return text;
    }
    console.error("The extracted text is empty! HOLDER ->");
    console.error(dom_obj);
    return null;
}