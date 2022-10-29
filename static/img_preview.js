function setOnchange() {
    let imgPreview = document.getElementById('img-preview');
    let imgUpload = document.getElementById('img-upload');
    imgUpload.onchange = event => {
        const [file] = imgUpload.files;
        if (file) {
            console.log(file)
            imgPreview.src = URL.createObjectURL(file);
        }
    };
}