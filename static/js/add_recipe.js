document.addEventListener("DOMContentLoaded", function() {
    const addIngredientButton = document.getElementById("addIngredient");
    const ingredientsContainer = document.getElementById("ingredients");

    addIngredientButton.addEventListener("click", function() {
        const ingredientTemplate = document.querySelector(".ingredient").cloneNode(true);
        ingredientsContainer.appendChild(ingredientTemplate);
    });
});
