
document.addEventListener("DOMContentLoaded", () => {
    const categoryLinks = document.querySelectorAll(
        ".category-item[data-category]"
    );

    const productColumns = document.querySelectorAll(
        ".product-column[data-category]"
    );

    categoryLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const selectedCategory = link.dataset.category;

            // Clicking a category filters products on the page.
            // Use the section link for the general "all products" view.
            event.preventDefault();

            productColumns.forEach((column) => {
                const category = column.dataset.category;
                const matches =
                    category === selectedCategory;

                column.hidden = !matches;
            });

            document.querySelector("#products")?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        });
    });

    // Reveal cards smoothly when they enter the viewport.
    const cards = document.querySelectorAll(".product-card");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12 }
        );

        cards.forEach((card) => observer.observe(card));
    } else {
        cards.forEach((card) => card.classList.add("is-visible"));
    }
});
