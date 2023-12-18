const sections = document.querySelectorAll("section");

sections.forEach(section => {
    const overlay = section.querySelector(".overlay");
    const showBtn = section.querySelector(".show-modal");
    const closeBtn = section.querySelector(".close-btn");

    showBtn.addEventListener("click", () => section.classList.add("active"));
    closeBtn.addEventListener("click", () => section.classList.remove("active"));

    overlay.addEventListener("click", (event) => {
        if (event.target === overlay) {
            section.classList.remove("active");
        }
    });
});