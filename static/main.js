const baseURL = 'http://127.0.0.1:5000'

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
const recipeComments = document.querySelector('.recipe-disp-comments')
const loader = document.querySelector('#loading-wheel-wrapper')
const placeholder = document.querySelector('#recipe-disp-placeholder')
const commentDispWrapper = document.querySelector('.comment-disp-wrapper')

let currentRecipeData; // will be set in popOutRecipe

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
    if (e.target.className === 'main-recipe-selector') {
        e.preventDefault();

        //clear out all other results
        let edamamResults = document.querySelector('#edamam-suggestions-disp')
        if (edamamResults) {
            edamamResults.style.display = 'none'
        }
        mainRecipeArea.style.display = 'grid'

        let placeholderText = document.querySelector('#recipe-disp-placeholder')
        if (placeholderText) {
            placeholderText.style.display = 'none'
        }

        recipeComments.style.display = 'none'
        // clear out previous recipe info
        recipeHeader.innerHTML = ''
        recipeIngredients.innerHTML = ''
        recipeInstructions.innerHTML = ''
        commentDispWrapper.innerHTML = ''

        // get new data and populate mainRecipeArea
        let selectedRecipeId = e.target.getAttribute('data-recipe-id')
        let response = await axios.get(`${baseURL}/api/recipes/${selectedRecipeId}/edit/info`)
        generate_existing_recipe_markup(recipeHeader, recipeIngredients, recipeInstructions, response)
    }
}

async function generate_existing_recipe_markup(pageRecipeHeader, pageRecipeIngredients, pageRecipeInstructions, response) {
    /** generate markup for when user chooses to 'pop out' recipe without editing it */
    currentRecipeData = response.data.recipe
    console.log(currentRecipeData)
    // recipe header
    let recipeName = document.createElement('h2')
    recipeName.innerText = response.data.recipe.name
    let editLink = document.createElement('a')
    editLink.href = `/recipes/${response.data.recipe.id}/edit`
    editLink.innerText = 'edit'
    editLink.className = 'edit-recipe-link'
    pageRecipeHeader.appendChild(editLink)
    pageRecipeHeader.appendChild(recipeName)

    // recipe tab and comment tab within header
    let tabContainer = document.createElement('span')
    tabContainer.className = 'tab-container'
    let recipeTab = document.createElement('div')
    let commentTab = document.createElement('div')
    recipeTab.innerText = 'Recipe', commentTab.innerText = `View Comments (${response.data.recipe.comments.length})`
    recipeTab.className = 'view-tab-recipe active-recipe-tab', commentTab.className = 'view-tab-comment'
    recipeTab.addEventListener('click', switchTabs), commentTab.addEventListener('click', switchTabs)
    tabContainer.appendChild(recipeTab), tabContainer.appendChild(commentTab)
    recipeHeader.appendChild(tabContainer)

    //recipe ingredients
    let recipeIngredientlist = response.data.recipe.ingredients
    for (let ingredient of recipeIngredientlist) {
        let ingredientWrapper = document.createElement('div')
        let newIngredient = document.createElement('div');
        newIngredient.className = 'new-ingredient'
        let newIngredientName = document.createElement('div')
        newIngredientName.innerText = ingredient.name

        //get ingredient amounts if they exist
        let newIngredientAmount = document.createElement('div')
        newIngredientAmount.className = 'ext-ingredient-amount'
        let quantity = '';
        let measure = '';
        let prep = '';
        if (ingredient.quantity) quantity = ingredient.quantity
        if (ingredient.measure) measure = ingredient.measure
        if (ingredient.prep) prep = ingredient.prep
        newIngredientAmount.innerText = `( ${quantity} ${measure} ${prep} )`
        newIngredient.appendChild(newIngredientName), newIngredient.appendChild(newIngredientAmount)
        let newIngredientCheckbox = document.createElement('input');
        newIngredient.setAttribute('for', `i${ingredient.id}`)
        newIngredientCheckbox.id = `i${ingredient.id}`
        newIngredientCheckbox.className = 'ingr-checkbox'
        newIngredientCheckbox.type = 'checkbox'

        ingredientWrapper.appendChild(newIngredient)
        pageRecipeIngredients.appendChild(ingredientWrapper)
    }
    //recipe instructions
    let recipeInstructionList = response.data.recipe.instructions
    let instructionUl = document.createElement('ol')
    for (let instruction of recipeInstructionList) {
        let newInstruction = document.createElement('li')
        newInstruction.innerText = instruction.text
        instructionUl.appendChild(newInstruction)
    }
    pageRecipeInstructions.appendChild(instructionUl)
}

const switchTabs = function (e) {
    const recipeTab = document.querySelector('.view-tab-recipe')
    const commentTab = document.querySelector('.view-tab-comment')
    recipeTab.classList.toggle('active-recipe-tab'), commentTab.classList.toggle('active-recipe-tab')

    // change disp of recipe
    if (e.target == commentTab) {
        recipeIngredients.style.display = 'none'
        recipeInstructions.style.display = 'none'
        recipeComments.style.display = 'grid'
        displayComments(currentRecipeData)
    }
    else {
        commentDispWrapper.innerHTML = ''
        recipeComments.style.display = 'none'
        recipeIngredients.style.display = 'grid'
        recipeInstructions.style.display = 'block'
    }
}

function displayComments(recipeData) {
    //display comment data
    for (let comment of recipeData.comments) {
        generateCommentMarkup(comment.commenter_name,
            comment.commenter_id,
            comment.commenter_profile_pic,
            comment.text)
    }
}

function generateCommentMarkup(commenter_name, commenter_id, commenter_profile_pic, comment_text) {
    let listCommentItem = document.createElement('div')
    let commenterWrapper = document.createElement('div')
    let commenterLink = document.createElement('a')
    let commenterProfilePic = document.createElement('img')
    let commentMessageArea = document.createElement('div')
    let commentText = document.createElement('p')

    listCommentItem.className = 'list-comment-item'
    commenterLink.className = 'commenter-link'
    commenterProfilePic.className = 'commenter-profile-pic'
    commentMessageArea.className = 'comment-message-area'

    commenterLink.innerText = commenter_name
    commenterLink.href = `/users/${commenter_id}/profile`
    commenterProfilePic.src = commenter_profile_pic
    commentText.innerText = comment_text

    commentMessageArea.appendChild(commentText)
    commenterLink.prepend(commenterProfilePic)
    commenterWrapper.appendChild(commenterLink)
    listCommentItem.appendChild(commenterWrapper)
    listCommentItem.appendChild(commentMessageArea)
    commentDispWrapper.prepend(listCommentItem)
}

let commentForm = document.querySelector('.comment-form')
let commentInput = document.querySelector('.comment-input')
commentForm.addEventListener('submit', async function (e) {
    e.preventDefault()
    body = { 'text': commentInput.value }
    let response = await axios.post(`/recipes/${currentRecipeData.id}/comments/add`, json = body)
    commentInput.value = ''
    console.log(response)
    generateCommentMarkup(response.data.commenter_name,
        response.data.commenter,
        response.data.commenter_profile_pic,
        response.data.text)

    commentDispWrapper.prepend('')
})

let hits = []
// create new recipe from keyword
const searchKeyword = async function edamamSearch(e) {
    e.preventDefault();
    previousSuggestions = document.querySelector('#edamam-suggestions-disp')
    if (previousSuggestions) {
        previousSuggestions.remove()
    }
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

    // append first 20 results to the grid

    for (i = 0; i < 19; i++) {
        if (response.data.hits[i]) {
            hits.push(response.data.hits[i])
        }
    }
    if (hits.length > 0) {
        const completedRecipeCards = extractEdamamData(hits) // returns an array of cards
        for (card of completedRecipeCards) {
            edamamSuggestionsArea.appendChild(card)
        }
        mainRecipeAreaWrapper.appendChild(edamamSuggestionsArea)

        loader.style.display = 'none'
        edamamSuggestionsArea.style.display = 'grid'
    }
    else {
        loader.style.display = 'none'
        placeholder.firstElementChild.innerText = 'No recipes found'
        placeholder.style.display = 'flex'
    }
}
keywordSearchForm.addEventListener('submit', searchKeyword)


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
        newCard.firstChild.setAttribute('data-recipe-index', hits.indexOf(hit))
        cards.push(newCard)
    }
    return cards
}


function generateSuggestionsMarkup(recipeUri, recipeName, recipeImage, recipeSource, recipeCuisine, ingredients) {
    /** 
    * Create markup for edamam cards
    */
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
    link.className = 'recipe-link'
    link.innerText = recipeSource
    link.href = `${recipeUri}`
    cardContents.appendChild(link)

    // tags
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
    recipeCard.addEventListener('click', useEdamamRecipe)
    cardWrapper.appendChild(recipeCard)

    return cardWrapper
}

const useEdamamRecipe = async function (e) {
    /**
     * When an edamam card is clicked (unless the link is clicked)
     */
    if (e.target.className != 'recipe-link') {
        let hitIndex = e.currentTarget.getAttribute('data-recipe-index')
        let recipeData = hits[hitIndex].recipe
        let recipeCuisine = []
        for (i = 0; i < 2; i++) {
            recipeCuisine.push(recipeData.cuisineType[i])
        }

        let ingredients = []
        for (let ingredient of recipeData.ingredients) {
            let new_ingredient = { 'food': ingredient.food, 'quantity': ingredient.quantity, 'measure': ingredient.measure }
            ingredients.push(new_ingredient)
        }
        tinyJson = {
            'name': recipeData.label,
            'recipeUrl': recipeData.url,
            'recipe_source': recipeData.source,
            'recipe_image': recipeData.image,
            'recipe_cuisine': recipeCuisine,
            'health_labels': recipeData.healthLabels,
            'ingredients': ingredients,
        }
        response = await axios.post('/recipes/build/edamam', json = tinyJson)
        window.location.href = `${baseURL}${response.data}`
    }
}
recipeSelectArea.addEventListener('click', popOutRecipe)

// collapsable rows and columns
const expandRecipeRow = function expandRow(e) {
    if (e.target.classList.contains('cookbook-expand')) {
        let recipesDiv = e.target.parentElement.nextElementSibling;
        if (recipesDiv.style.display == "") {
            recipesDiv.style.display = 'block'
            e.target.classList.add('rotated-svg')
        }
        else {
            recipesDiv.style.display = ''
            e.target.classList.remove('rotated-svg')
        }
    }

    else if (e.target.className.baseVal == 'svg-clicker') {
        let recipesDiv = e.target.parentElement.parentElement.nextElementSibling;
        if (recipesDiv.style.display == "") {
            recipesDiv.style.display = 'block'
            e.target.parentElement.classList.add('rotated-svg')
        }
        else {
            recipesDiv.style.display = ''
            e.target.parentElement.classList.remove('rotated-svg')
        }
    }
}

recipeIngredients.addEventListener('click', (e)=>{
    e.target.parentElement.classList.toggle('crossed')
})

recipeSelectArea.addEventListener('click', expandRecipeRow)




