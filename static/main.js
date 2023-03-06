//main page area selectors
const mainRecipeAreaWrapper = document.querySelector('#recipe-disp-grid-wrapper')
const mainRecipeArea = document.querySelector('#recipe-disp-grid');
const recipeSelectArea = document.querySelector('#cookbook-grid')
const selectableCookbooks = document.querySelectorAll('ul')
const keywordSearchForm = document.querySelector('#edamam-search')
const keywordSearchInput = document.querySelector('#edamam-search-input')

//recipe disp selectors
const recipeHeader = document.querySelector('.recipe-disp-header')
const recipeIngredients = document.querySelector('.recipe-disp-ingredients')
const recipeInstructions = document.querySelector('.recipe-disp-instructions')
const loader = document.querySelector('#loading-wheel-wrapper')
const placeholder = document.querySelector('#recipe-disp-placeholder')

//cookbook sidebar selectors
const selectableRecipes = []
const selectableRecipeButtons = [];
for (let cookbook of selectableCookbooks) {
    let innerRecipes = cookbook.querySelectorAll('li');
    selectableRecipes.push(...innerRecipes)
}

//recipe build selectors

/* 
    ***************************************************
    event listeners and async funtions 
    ***************************************************
*/
//event listener to get recipe info 
const popOutRecipe = async function recipePopper(e) {
    if (e.target.tagName === 'BUTTON') {
        e.preventDefault();

        //clear out all other results
        let edamamResults = document.querySelector('#edamam-suggestions-disp')
        if (edamamResults) {
            edamamResults.style.display = 'none'
        }
        mainRecipeArea.style.display = 'grid'

        let placeholderText = document.querySelector('#recipe-disp-placeholder')
        if (placeholderText){
            placeholderText.style.display = 'none'
        }
        // clear out previous recipe info
        recipeHeader.innerHTML = ''
        recipeIngredients.innerHTML = ''
        recipeInstructions.innerHTML = ''

        // get new data and populate mainRecipeArea
        let selectedRecipeId = e.target.getAttribute('data-recipe-id')
        let response = await axios.get(`http://127.0.0.1:5000/api/recipes/${selectedRecipeId}`)

        // recipe header
        let recipeName = document.createElement('h2')
        recipeName.innerText = response.data.recipe.name
        recipeHeader.appendChild(recipeName)

        //recipe ingredients
        console.log(response.data.recipe)
        let recipeIngredientlist = response.data.recipe.ingredients

        for (let ingredient of recipeIngredientlist) {
            let ingredientWrapper = document.createElement('div')
            let newIngredient = document.createElement('label');
            let newIngredientCheckbox = document.createElement('input');
            newIngredient.innerText = ingredient.name, newIngredient.setAttribute('for', `i${ingredient.id}`)
            newIngredientCheckbox.id = `i${ingredient.id}`, newIngredientCheckbox.value = ingredient.price
            newIngredientCheckbox.type = 'checkbox'
            // add onclick event
            ingredientWrapper.appendChild(newIngredient)
            ingredientWrapper.appendChild(newIngredientCheckbox)
            recipeIngredients.appendChild(ingredientWrapper)
        }

        //recipe instructions
        let recipeInstructionList = response.data.recipe.instructions
        let instructionUl = document.createElement('ul')
        for (let instruction of recipeInstructionList) {
            let newInstruction = document.createElement('li')
            newInstruction.innerText = instruction.text
            instructionUl.appendChild(newInstruction)
        }
        recipeInstructions.appendChild(instructionUl)
    }
}
if (recipeSelectArea ){

    recipeSelectArea.addEventListener('click', popOutRecipe)
}


// create new recipe from keyword
const searchKeyword = async function edamamSearch(e) {
    e.preventDefault();
    mainRecipeArea.style.display = 'none'
    let keywordTerm = keywordSearchInput.value;
    placeholder.style.display = 'none'
    loader.style.display = 'block'
    response = await axios.get('https://api.edamam.com/api/recipes/v2', {
        params: { 'type': 'public', 'q': `${keywordTerm}`, 'app_id': 'a1ddc0d6', 'app_key': '83e158597d16faaf1e56c3d40aa514f8' }
    })
    console.log(response)

    // add a new grid area to show the edamam suggestions
    const edamamSuggestionsArea = document.createElement('div')
    edamamSuggestionsArea.id = 'edamam-suggestions-disp'
    edamamSuggestionsArea.style.display = 'none'

    // append first five results to the grid
    hits = []
    for (i = 0; i < 6; i++) {
        hits.push(response.data.hits[i])
    }
    const completedRecipeCards = extractEdamamData(hits) // returns an array of cards
    for (card of completedRecipeCards) {
        edamamSuggestionsArea.appendChild(card)
    }
    mainRecipeAreaWrapper.appendChild(edamamSuggestionsArea)

    loader.style.display = 'none'
    edamamSuggestionsArea.style.display = 'grid'


}

if (keywordSearchForm){
    keywordSearchForm.addEventListener('submit', searchKeyword)
}


function generateSuggestionsMarkup(recipeUri, recipeName, recipeImage, recipeSource, recipeCuisine, ingredients) {
    const cardWrapper = document.createElement('div')
    const recipeCard = document.createElement('div')
    recipeCard.className = 'edamam-recipe-card'
    const cardInner = document.createElement('div')
    cardInner.className = 'edamam-card-inner'
    const imageWrapper = document.createElement('div')
    imageWrapper.className = 'edamam-image-wrapper'
    const cardContents = document.createElement('div')
    cardContents.className = 'edamam-card-contents'

    //image
    const image = document.createElement('img')
    image.setAttribute('src', `${recipeImage}`)
    imageWrapper.appendChild(image)

    //contents
    const name = document.createElement('p')
    name.innerText = recipeName
    cardContents.appendChild(name)

    const link = document.createElement('a')
    link.innerText = recipeSource
    link.href = `${recipeUri}`
    cardContents.appendChild(link)

    const cuisines = document.createElement('div')
    const cuisine1 = document.createElement('span')
    cuisine1.innerText = recipeCuisine[0]
    cuisines.appendChild(cuisine1)
    if (recipeCuisine[1]) {
        const cuisine2 = document.createElement('span')
        cuisine2.innerText = recipeCuisine[1]
        cuisines.appendChild(cuisine2)
    }
    cardContents.appendChild(cuisines)

    const ingredientWrapper = document.createElement('div')
    const ingredientList = document.createElement('ul')
    ingredientWrapper.appendChild(ingredientList)
    for (let ingredient of ingredients) {
        let ingredientLi = document.createElement('li')
        ingredientLi.innerText = ingredient
        ingredientList.appendChild(ingredientLi)
    }
    cardContents.appendChild(ingredientWrapper)


    cardInner.appendChild(imageWrapper)
    cardInner.appendChild(cardContents)
    recipeCard.appendChild(cardInner)
    cardWrapper.appendChild(recipeCard)

    return cardWrapper
}
function extractEdamamData(hits) {
    const cards = []
    //extract the data needed from the given hits from edamam
    for (let hit of hits) {
        let recipeUrl = hit.recipe.url
        let recipeName = hit.recipe.label
        let recipeImage = hit.recipe.image
        let recipeSource = hit.recipe.source

        recipeCuisine = []
        for (i = 0; i < 2; i++) {
            recipeCuisine.push(hit.recipe.cuisineType[i])
        }

        let ingredients = []
        for (let ingredient of hit.recipe.ingredients) {
            ingredients.push(ingredient.food)
        }

        const newCard = generateSuggestionsMarkup(recipeUrl,
            recipeName,
            recipeImage,
            recipeSource,
            recipeCuisine,
            ingredients)
        cards.push(newCard)
    }
    return cards
}

// collapsable rows and columns
const expandRecipeRow = function expandRow(e) {
    if (e.target.className.baseVal == 'expand-svg') {
        let recipesDiv = e.target.parentElement.nextElementSibling;
        if (recipesDiv.style.display == "") {
            recipesDiv.style.display = 'block'
        }
        else {
            recipesDiv.style.display = ''
        }
    }

    else if (e.target.className.baseVal == 'svg-clicker') {
        let recipesDiv = e.target.parentElement.parentElement.nextElementSibling;
        if (recipesDiv.style.display == "") {
            recipesDiv.style.display = 'block'
        }
        else {
            recipesDiv.style.display = ''
        }
    }
}
if (recipeSelectArea){
    recipeSelectArea.addEventListener('click', expandRecipeRow)
}

