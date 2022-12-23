document.addEventListener("DOMContentLoaded", () => {
    console.log("done loading.");
    userNavbar = document.querySelector(".user-navbar");
    dropdownMenu = userNavbar.nextElementSibling;
    dropdownUser = userNavbar.parentNode;
    body = document.querySelector("body");

    userNavbar.addEventListener("mouseover", () => {
        if (!dropdownUser.classList.contains("show")) {
            userNavbar.click();
            userNavbar.focus();
        }
        dropdownUser.addEventListener("mouseleave", () => {
            userNavbar.blur();
            dropdownUser.classList.remove("show");
            dropdownMenu.classList.remove("show");
        }, {once: true});
    })

    if (userNavbar.offsetWidth >= 117) {
        dropdownMenu.style["right"] = "0";
    }

    if (window.location.href.includes("/shapeatint")) {
        labelTitle = document.querySelector("[for='form-title']");
        labelTitle.innerHTML = "Title";

        hr = document.createElement("hr");
        labelCommentCheckbox = document.querySelector("[for='id_allow_comments']");
        labelImage = document.createElement("label");
        labelImage.innerHTML = "Image";
        browseButton = document.querySelector("[type='file']");
        br = document.createElement("br");
        br2 = document.createElement("br");
        labelDesc = document.querySelector("[for='id_desc']");
        labelDesc.innerHTML = "Description (optional)";
        desc = document.querySelector("[name='desc']");
        fileImg = document.querySelector("[name='file_img']");
        urlImg = document.querySelector("[name='url_img']");
        buttons = document.getElementById("file-url-button-slide");
        fileImgButton = document.querySelector("[name='file-img-button']");
        urlImgButton = document.querySelector("[name='url-img-button']");

        urlImg.style.display = "none";
        desc.after(buttons);
        buttons.after(br);
        buttons.after(br2);
        labelImage.setAttribute("for", "file-url-button-slide");
        desc.after(labelImage);
        labelCommentCheckbox.parentNode.insertBefore(hr, labelCommentCheckbox);

        fileImgButton.addEventListener("click", () => {
            fileImg.style.display = "block";
            urlImg.style.display = "none";
        })

        urlImgButton.addEventListener("click", () => {
            urlImg.style.display = "block";
            fileImg.style.display = "none";
        })
    }
})