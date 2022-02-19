function myToggle() {
    var el = document.getElementById('add-item');
    if(el.style.display === 'none') {
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}