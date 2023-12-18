const sections = document.querySelectorAll("section");

sections.forEach(section => {
    const showBtn = section.querySelector(".show-modal");
    const closeBtn = section.querySelector(".close-btn");

    showBtn.addEventListener("click", (event) => {
        if (event.shiftKey) {
            window.location.href = showBtn.dataset.deleteUrl;
        } else {
            section.classList.add("active");
        }
    });
    closeBtn.addEventListener("click", () => section.classList.remove("active"));
});
