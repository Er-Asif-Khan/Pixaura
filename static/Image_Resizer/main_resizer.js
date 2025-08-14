function validateForm() {
    const form = document.forms["resizeForm"];
    const width = form["width"].value;
    const height = form["height"].value;

    if (width && height) {
        return confirm("⚠️ Warning: Providing both width and height may distort the image. Continue?");
    }
    return true;
}
