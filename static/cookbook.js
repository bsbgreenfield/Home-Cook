const recipeItems = document.querySelectorAll('.cookbook-recipe-item')

const removeRecipe = async function(e){
    if (e.target.tagName == 'svg' || e.target.tagName == 'path'){
        const selectedDiv = e.currentTarget
        let thisCookbookId = selectedDiv.getAttribute('data-parent-cookbook')
        let currRecipeId = selectedDiv.getAttribute('data-curr-recipe')
        let response = await axios.post(`/api/cookbooks/${thisCookbookId}/remove_recipe/${currRecipeId}`)
        if (response.data == 'recipe-removed'){
            selectedDiv.remove()
        }
    }
}

for (let recipeItem of recipeItems){
    recipeItem.addEventListener('click', removeRecipe)
}