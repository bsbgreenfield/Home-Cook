userCookbooks = document.querySelector('.cookbook-card')
recipeSidebar = document.querySelector('.cookbook-display-recipe-sidebar')

const popOutCookbookRecipe = async function(e){
    if (e.target.className == 'recipe-sidebar-recipe-select' ){
        recipeHeader.innerHTML = ''
        recipeIngredients.innerHTML = ''
        recipeInstructions.innerHTML = ''
    let selectedRecipeId = e.target.getAttribute('data-recipe-id')
    let response = await axios.get(`http://127.0.0.1:5000/api/recipes/${selectedRecipeId}/edit/info`)
    generate_existing_recipe_markup(recipeHeader, recipeIngredients, recipeInstructions, response)
    }
}


recipeSidebar.addEventListener('click', popOutCookbookRecipe)