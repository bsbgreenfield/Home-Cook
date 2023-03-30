const userCookbooks = document.querySelector('.cookbook-card')
const recipeSidebar = document.querySelector('.cookbook-display-recipe-sidebar')
const recipeDispHeader = document.querySelector('.recipe-disp-header')
const recipeSelects = document.querySelectorAll('.recipe-sidebar-recipe-select')

let curr_recipe;
const popOutCookbookRecipe = async function(e){
    if (e.currentTarget.className == 'recipe-sidebar-recipe-select' ){


        recipeIngredients.style.display = 'grid'
        recipeInstructions.style.display = 'block'
        recipeComments.style.display = 'none'
        commentDispWrapper.innerHTML = ''
        recipeHeader.innerHTML = ''
        recipeIngredients.innerHTML = ''
        recipeInstructions.innerHTML = ''
    let selectedRecipeId = e.currentTarget.getAttribute('data-recipe-id')

    //save recipe id to global variable so we can access it when copying recipe
    curr_recipe = selectedRecipeId;

    let response = await axios.get(`http://127.0.0.1:5000/api/recipes/${selectedRecipeId}/edit/info`)
    generate_existing_recipe_markup(recipeHeader, recipeIngredients, recipeInstructions, response)
    
    // add button to copy recipe
    let copyRecipeButton = document.createElement('button')
    copyRecipeButton.innerText = 'Copy Recipe'
    copyRecipeButton.className = 'take-recipe'
    let copyRecipeForm = document.createElement('form')
    copyRecipeForm.action = `/api/recipes/${curr_recipe}/copy`
    copyRecipeForm.method = 'POST'
    copyRecipeForm.appendChild(copyRecipeButton)
    recipeDispHeader.appendChild(copyRecipeForm)
    }
}



for (let recipeSelect of recipeSelects){
    recipeSelect.addEventListener('click', popOutCookbookRecipe)
}
