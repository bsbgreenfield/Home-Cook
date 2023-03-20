const ingredients = ['Angelica', 'Savoy cabbage', 'Silver linden', 'Kiwi', 'Allium (Onion)', 'Garden onion', 'Leek', 'Garlic', 'Chives', 'Lemon verbena', 'Cashew nut', 'Pineapple', 'Dill', 'Custard apple', 'Wild celery', 'Peanut', 'Burdock', 'Horseradish', 'Tarragon', 'Mugwort', 'Asparagus', 'Oat', 'Star fruit', 'Brazil nut', 'Common beet', 'Borage', 'Chinese mustard', 'Swede', 'Rape', 'Common cabbage', 'Cauliflower', 'Brussel sprouts', 'Kohlrabi', 'Broccoli', 'Chinese cabbage', 'Turnip', 'Pigeon pea', 'Tea', 'Capers', 'Pepper (C. annuum)', 'Papaya', 'Safflower', 'Caraway', 'Pecan nut', 'Chestnut', 'Roman camomile', 'Chickpea', 'Endive', 'Chicory', 'Chinese cinnamon', 'Ceylon cinnamon', 'Watermelon', 'Lime', 'Lemon', 'Pummelo', 'Sweet orange', 'Coffee', 'Arabica coffee', 'Robusta coffee', 'Coriander', 'Common hazelnut', 'Saffron', 'Muskmelon', 'Cucumber', 'Cucurbita (Gourd)', 'Cumin', 'Turmeric', 'Quince', 'Lemon grass', 'Globe artichoke', 'Wild carrot', 'Japanese persimmon', 'Cardamom', 'Black crowberry', 'Loquat', 'Rocket salad (ssp.)', 'Wax apple', 'Common buckwheat', 'Tartary buckwheat', 'Fig', 'Fennel', 'Strawberry', 'Black huckleberry', 'Soy bean', 'Sunflower', 'Sea-buckthornberry', 'Barley', 'Hyssop', 'Star anise', 'Swamp cabbage', 'Sweet potato', 'Black walnut', 'Common walnut', 'Lettuce', 'Grass pea', 'Sweet bay', 'Lentils', 'Garden cress', 'Lovage', 'Flaxseed', 'Mexican oregano', 'Lichee', 'Lupine', 'Apple', 'Mango', 'German camomile', 'Lemon balm', 'Mentha (Mint)', 'Orange mint', 'Cornmint', 'Spearmint', 'Peppermint', 'Medlar', 'Bitter gourd', 'Mulberry', 'Black mulberry', 'Nutmeg', 'Sweet basil', 'Evening primrose', 'Olive', 'Sweet marjoram', 'Pot marjoram', 'Common oregano', 'Rice', 'Millet', 'Poppy', 'Passion fruit', 'Parsnip', 'Avocado', 'Parsley', 'Scarlet bean', 'Lima bean', 'Common bean', 'Date', 'Black chokeberry', 'Anise', 'Pine nut', 'Pepper (Spice)', 'Pistachio', 'Common pea', 'Purslane', 'Apricot', 'Sweet cherry', 'Sour cherry', 'European plum', 'Almond', 'Peach', 'Guava', 'Pomegranate', 'Pear', 'Radish', 'Garden rhubarb', 'Blackcurrant', 'Redcurrant', 'Gooseberry', 'Watercress', 'Rosemary', 'Cloudberry', 'Red raspberry', 'Black raspberry', 'Sorrel', 'Common sage', 'Black elderberry', 'Summer savory', 'Winter savory', 'Rye', 'Sesame', 'Garden tomato', 'Cherry tomato', 'Garden tomato (var.)', 'Eggplant', 'Potato', 'Rowanberry', 'Sorghum', 'Spinach', 'Cloves', 'Tamarind', 'Dandelion', 'Cocoa bean', 'Common thyme', 'Linden', 'Small-leaf linden', 'Fenugreek', 'Common wheat', 'Lowbush blueberry', 'Sparkleberry', 'Highbush blueberry', 'American cranberry', 'Bilberry', 'Lingonberry', 'Vanilla', 'Common verbena', 'Broad bean', 'Adzuki bean', 'Gram bean', 'Mung bean', 'Climbing bean', 'Cowpea', 'Muscadine grape', 'Common grape', 'Corn', 'Ginger', 'Arctic blackberry', 'Banana', 'Bayberry', 'Elliotts blueberry', 'Canada blueberry', 'Bog bilberry', 'Buffalo currant', 'Celeriac', 'Celery stalks', 'Chinese chives', 'European cranberry', 'Deerberry', 'Ginseng', 'Cascade huckleberry', 'Oval-leaf huckleberry', 'Evergreen huckleberry', 'Red huckleberry', 'Longan', 'Macadamia nut (M. tetraphylla)', 'Garden onion (var.)', 'Summer grape', 'Fox grape', 'Nectarine', 'Peach (var.)', 'Pepper (C. baccatum)', 'Pepper (C. chinense)', 'Pepper (Capsicum)', 'Rambutan', 'Red rice', 'Annual wild rice', 'Swiss chard', 'Lemon thyme', 'Tronchuda cabbage', 'Japanese walnut', 'Welsh onion', 'Hard wheat', 'Shallot', 'Rocket salad', 'Carrot', 'Triticale', 'Black cabbage', 'Half-highbush blueberry', 'Celery leaves', 'Chicory leaves', 'Komatsuna', 'Pak choy', 'Napa cabbage', 'Chicory roots', 'Grapefruit/Pummelo hybrid', 'Grapefruit', 'Jostaberry', 'Kai-lan', 'Italian oregano', 'Oxheart cabbage', 'Daikon radish', 'Black radish', 'Radish (var.)', 'Red beetroot', 'Sweet rowanberry', 'Pineappple sage', 'Skunk currant', 'Beer', 'Other bread', 'Breakfast cereal', 'Other soy product', 'Other cereal product', 'Pasta', 'Biscuit', 'Sourdough', 'Spirit', 'Fortified wine', 'Other alcoholic beverage', 'Abalone', 'Abiyuch', 'Acerola', 'Acorn', 'Winter squash', 'Agar', 'Red king crab', 'Alfalfa', 'Allspice', 'Amaranth', 'Arrowhead', 'Arrowroot', 'Asian pear', 'Atlantic herring', 'Atlantic mackerel', 'Painted comber', 'Atlantic pollock', 'Atlantic wolffish', 'Bamboo shoots', 'Striped bass', 'Beaver', 'Beech nut', 'Beluga whale', 'Bison', 'Black bear', 'Alaska blackfish', 'Blue crab', 'Blue mussel', 'Northern bluefin tuna', 'Bluefish', 'Wild boar', 'Bowhead whale', 'Breadfruit', 'Breadnut tree seed', 'Rapini', 'Brown bear', 'Buffalo', 'Burbot', 'Giant butterbur', 'American butterfish', 'Butternut', 'Butternut squash', 'Calabash', 'Cardoon', 'Caribou', 'Natal plum', 'Carob', 'Common carp', 'Cassava', 'Channel catfish', 'Chayote', 'Cherimoya', 'Chervil', 'Chia', 'Chinese broccoli', 'Chinese chestnut', 'Chinese water chestnut', 'Garland chrysanthemum', 'Cisco', 'Nuttall cockle', 'Coconut', 'Pacific cod', 'Atlantic cod', 'Common octopus', 'Corn salad', 'Cottonseed', 'Catjang pea', 'Malus (Crab apple)', 'Squashberry', 'Atlantic croaker', 'Cusk', 'Cuttlefish', 'Mule deer', 'Devilfish', 'Dock', 'Dolphin fish', 'Freshwater drum', 'Mallard duck', 'Dungeness crab', 'Durian', 'Eastern oyster', 'Freshwater eel', 'Elderberry', 'Elk', 'Emu', 'Oregon yampah', 'European anchovy', 'European chestnut', 'Turbot', 'Fireweed', 'Florida pompano', 'Ginkgo nuts', 'Greylag goose', 'Grape', 'Greenland halibut/turbot', 'Groundcherry', 'Grouper', 'Guinea hen', 'Haddock', 'Hippoglossus (Common halibut)', 'Hazelnut', 'Hickory nut', 'Horse', 'Horseradish tree', 'Alaska blueberry', 'Hyacinth bean', 'Irish moss', 'Pacific jack mackerel', 'Jackfruit', 'Japanese chestnut', 'Java plum', 'Jerusalem artichoke', 'Jujube', 'Jute', 'Kale', 'Kelp', 'King mackerel', 'Kumquat', 'Lambsquarters', 'Leather chiton', 'Wild leek', 'Common ling', 'Lingcod', 'American lobster', 'Loganberry', 'Lotus', 'Sacred lotus', 'White lupine', 'Malabar spinach', 'Mammee apple', 'Purple mangosteen', 'Alpine sweetvetch', 'Milkfish', 'Monkfish', 'Moose', 'Moth bean', 'Mountain yam', 'Striped mullet', 'Muskrat', 'White mustard', 'Mustard spinach', 'New Zealand spinach', 'Nopal', 'Ocean pout', 'North Pacific giant octopus', 'Ohelo berry', 'Okra', 'Tunicate', 'Opossum', 'Ostrich', 'Spotted seal', 'Pacific herring', 'Pacific oyster', 'Pacific rockfish', 'Velvet duck', 'Pepper (C. frutescens)', 'Common persimmon', 'Pheasant', 'Northern pike', 'Pili nut', 'Colorado pinyon', 'Pitanga', 'Plains prickly pear', 'French plantain', 'American pokeweed', 'Polar bear', 'Opium poppy', 'Prairie turnip', 'Prickly pear', 'Quinoa', 'European rabbit', 'Raccoon', 'Rainbow smelt', 'Rainbow trout', 'Malabar plum', 'Rose hip', 'Roselle', 'Orange roughy', 'Sablefish', 'Pink salmon', 'Chum salmon', 'Coho salmon', 'Sockeye salmon', 'Chinook salmon', 'Atlantic salmon', 'Salmonberry', 'Common salsify', 'Sapodilla', 'Mamey sapote', 'Spanish mackerel', 'Pacific sardine', 'Scallop', 'Scup', 'Sea cucumber', 'Steller sea lion', 'Bearded seal', 'Ringed seal', 'Seatrout', 'Sesbania flower', 'American shad', 'Shark', 'Sheefish', 'Sheepshead', 'Hedge mustard', 'Skipjack tuna', 'Snapper', 'Soursop', 'Spelt', 'Spirulina', 'Squab', 'Squirrel', 'Strawberry guava', 'Greater sturgeon', 'White sucker', 'Sugar apple', 'Pumpkinseed sunfish', 'Swordfish', 'Taro', 'Teff', 'Tilefish', 'Mexican groundcherry', 'Towel gourd', 'Turkey', 'Walleye', 'Alaska pollock', 'Wasabi', 'Wax gourd', 'Whelk', 'Coalfish pollock', 'Broad whitefish', 'Whitefish', 'Whiting', 'Wild rice', 'Tea leaf willow', 'Winged bean', 'Yam', 'Jicama', 'Yautia', 'Yellowfin tuna', 'Yellowtail amberjack', 'Pollock', 'Albacore tuna', 'Gadus (Common cod)', 'Atlantic halibut', 'Pacific halibut', 'Pacific salmon', 'Smelt', 'Spiny lobster', 'Snow crab', 'Black-eyed pea', 'Deer', 'Macadamia nut', 'Percoidei (Bass and others)', 'Perciformes (Perch-like fishes)', 'Arctic ground squirrel', 'Rabbit', 'Domestic goat', 'Beefalo', 'Antelope', 'Squid', 'Shrimp', 'Crayfish', 'Flatfish', 'Walrus', 'Alaska wild rhubarb', 'Oriental wheat', 'Yardlong bean', 'Great horned owl', 'Quail', 'Boysenberry', 'Persian lime', 'Feijoa', 'Rowal', 'Jews ear', 'Common mushroom', 'Shiitake', 'Purple laver', 'Wakame', 'Enokitake', 'Epazote', 'Oyster mushroom', 'Cloud ear fungus', 'Maitake', 'Ostrich fern', 'Spot croaker', 'Sourdock', 'Tinda', 'Atlantic menhaden', 'Wheat', 'Common chokecherry', 'Agave', 'Narrowleaf cattail', 'Jellyfish', 'Anchovy', 'Blue whiting', 'Carp bream', 'Chanterelle', 'Sturgeon', 'Charr', 'Cinnamon', 'Crab', 'Common dab', 'Spiny dogfish', 'Anguilliformes (Eel)', 'True frog', 'Garfish', 'Mountain hare', 'Lake trout', 'Lemon sole', 'Clawed lobster', 'Lumpsucker', 'Marine mussel', 'Norway haddock', 'Norway lobster', 'Norway pout', 'Oil palm', 'True oyster', 'Sago palm', 'Persimmon', 'Pikeperch', 'Rock ptarmigan', 'Pacific ocean perch', 'Black salsify', 'True seal', 'Red algae', 'Kombu', 'Snail', 'True sole', 'Catfish', 'Thistle', 'Thunnus (Common tuna)', 'Walnut', 'Conch', 'Grape wine', 'Berry wine', 'Other wine', 'Apple cider', 'Liquor', 'Cheese', 'Milk (Cow)', 'Eggs', 'Yogurt', 'Bean', 'Vodka', 'Whisky', 'Ice cream', 'Gin', 'Honey', 'Liquorice', 'Vinegar', 'Rum', 'Port wine', 'Vermouth', 'Sherry', 'Madeira wine', 'Nougat', 'Toffee', 'Cake', 'Pizza', 'Ymer', 'Other snack food', 'Crisp bread', 'Pastry', 'Dragée', 'Chewing gum', 'Marzipan', 'Salad dressing', 'Sauce', 'Salt', 'Butter', 'Butter substitute', 'Cream', 'Sugar', 'Sausage', 'Meatball', 'Mustard', 'Pate', 'Sugar substitute', 'Meat bouillon', 'Other meat product', 'Whey', 'Casein', 'Fruit preserve', 'Leavening agent', 'Marshmallow', 'Gelatin', 'Water', 'Other fish product', 'Milk (Human)', 'Other beverage', 'Baby food', 'Dumpling', 'Soup', 'Other vegetable product', 'Unclassified food or beverage', 'Syrup', 'Tallow', 'Remoulade', 'Chocolate spread', 'Fruit gum', 'Curry powder', 'Other candy', 'Meringue', 'Lard', 'Other animal fat', 'Other cocoa product', 'Cocoa butter', 'Cocoa powder', 'Cocoa liquor', 'Chocolate', 'Hot chocolate', 'Dried milk', 'Milk (Other mammals)', 'Kefir', 'Buttermilk', 'Other fermented milk', 'Soy sauce', 'Miso', 'Tofu', 'Zwieback', 'Roe', 'Cichlidae (Tilapia)', 'Icing', 'Snack bar', 'Green turtle', 'Energy drink', 'Burrito', 'Hamburger', 'Baked beans', 'Chili', 'Taco', 'Tortilla', 'Nachos', 'Processed cheese', 'Salad', 'Cream substitute', 'Dulce de leche', 'Topping', 'Sweet custard', 'Egg roll', 'Heart of palm', 'Popcorn', 'Potato chip', 'Tortilla chip', 'Corn chip', 'Hibiscus tea', 'Stew', 'Gelatin dessert', 'Junket', 'Falafel', 'Frybread', 'Other frozen dessert', 'Lasagna', 'Morchella (Morel)', 'Pancake', 'Pectin', 'Pudding', 'Waffle', 'Soy milk', 'Meatloaf', 'Sake', 'Cocktail', 'Couscous', 'Bulgur', 'Coffee substitute', 'Coffee mocha', 'Chimichanga', 'Semolina', 'Tapioca pearl', 'Tostada', 'Quesadilla', 'Baked potato', 'Hot dog', 'Spread', 'Enchilada', 'Egg substitute', 'Nutritional drink', 'Other sandwich', 'Ketchup', 'Breakfast sandwich', 'Adobo', 'Macaroni and cheese', 'Butterfat', 'Horned melon', 'Hushpuppy', 'Fruit juice', 'Relish', 'Other fruit product', 'Fruit salad', 'Soy yogurt', 'Vegetarian food', 'Veggie burger', 'Cold cut', 'Mixed nuts', 'Canola', 'Babassu palm', 'Cupuaçu', 'Shea tree', 'Oil-seed Camellia', 'Ucuhuba', 'Phyllo dough', 'Cooking oil', 'Pie crust', 'Pie filling', 'Pie', 'Shortening', 'Soy cream', 'Ice cream cone', 'Molasses', 'Cracker', 'Nance', 'Naranjilla', 'Natto', 'Ravioli', 'Scrapple', 'Other pasta dish', 'Succotash', 'Tamale', 'Rice cake', 'Tree fern', 'Evaporated milk', 'Flour', 'Akutaq', 'Dough', 'Pita bread', 'Focaccia', 'Bagel', 'Other bread product', 'Piki bread', 'French toast', 'Wheat bread', 'Rye bread', 'Oat bread', 'Potato bread', 'Cornbread', 'Corn grits', 'Multigrain bread', 'Rice bread', 'Pan dulce', 'Raisin bread', 'Wonton wrapper', 'Trail mix', 'Greenthread tea', 'Fruit-flavor drink', 'Vegetable juice', 'Horchata', 'Soft drink', 'Frozen yogurt', 'Milkshake', 'Chocolate mousse', 'Dripping', 'Pupusa', 'Empanada', 'Arepa', 'Ascidians', 'Gefilte fish', 'Yellow pond-lily', 'Fish burger', 'Other dish', 'Pot pie', 'Stuffing', 'Edible shell', 'Fudge', 'Candy bar', 'Condensed milk', 'Margarine', 'Margarine-like spread', 'Hummus', 'Potato puffs', 'Potato gratin', 'Milk substitute', 'Pepper (C. pubescens)', 'Soft-necked garlic', 'Cabbage', 'Chinese bayberry', 'Mushrooms', 'Alcoholic beverages', 'Onion-family vegetables', 'Pomes', 'Brassicas', 'Cereals and cereal products', 'Citrus', 'Cocoa and cocoa products', 'Coffee and coffee products', 'Crustaceans', 'Milk and milk products', 'Fats and oils', 'Fishes', 'Herbs and Spices', 'Pulses', 'Animal foods', 'Mollusks', 'Nuts', 'Beverages', 'Fruits', 'Green vegetables', 'Root vegetables', 'Sunburst squash (pattypan squash)', 'Green zucchini', 'Yellow zucchini', 'Green bell pepper', 'Yellow bell pepper', 'Orange bell pepper', 'Red bell pepper', 'Italian sweet red pepper', 'Yellow wax bean', 'Green bean', 'Saskatoon berry', 'Nanking cherry', 'Japanese pumpkin', 'White cabbage', 'Romaine lettuce', 'beef', 'pork', 'salmon', 'tuna', 'steak', 'ground beef']

const ingredientSearchBar = document.querySelector('#ingredient')
const SearchDisplay = document.querySelector('.search-display')
const ingredientSuggestions = document.querySelector('#recipe-build-search')
const ingredientDisplay = document.querySelector('.build-ingredients-display-wrapper')
const custom_ingr_form = document.querySelector('#custom-ingredient-form')
const customIngredientInput = document.querySelector('.custom-ingr-input')
let curr_url = window.location.pathname
function search(str, array) {
    let results = [];
    results = (array.filter(val => val.toLowerCase().includes(str)));
    return results;
}

function searchHandler(e) {
    if (e.currentTarget == ingredientSearchBar) {
        searchLogic('ingredient')
    }

}
function searchLogic(searchType) {
    if (searchType == 'ingredient') {
        ingredientSuggestions.innerHTML = '';
        let resultList = search(ingredientSearchBar.value.toLowerCase(), ingredients)
        if (resultList.length > 0) {
            ingredientSuggestions.style.display = 'grid'
            custom_ingr_form.style.display = 'none'
            showSuggestions(resultList)
        }
        else {
            ingredientSuggestions.style.display = 'none'
            custom_ingr_form.style.display = 'block'
            customIngredientInput.value = ingredientSearchBar.value
        }
    }
    else if (searchType == 'tag') {
        ///something else
    }
}
function showSuggestions(results) {
    for (i = 0; i <= 5; i++) {
        if (results[i] != undefined && ingredientSearchBar.value != '') {
            let suggestion = document.createElement('div');
            suggestion.className = 'ingredient-choice'
            suggestion.innerText = results[i];
            ingredientSuggestions.appendChild(suggestion)
        }
    }
}

async function useSuggestion(e) {
    console.log(e.target)
    if (e.target.className == 'ingredient-choice') {
        generateIngredientMarkup(e.target.innerText)
    }
}

async function addCustomIngredient(e) {
    e.preventDefault()
    generateIngredientMarkup(customIngredientInput.value)
}


async function generateIngredientMarkup(ingredientInputValue) {
    let ingredientName = ingredientInputValue
    let newIngredient = document.createElement('div')
    newIngredient.classList.add('added-ingredient')
    newIngredient.innerText = ingredientName


    // delete button
    let delete_ingedrient_btn = document.createElement('div')
    delete_ingedrient_btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206 8.313 3.666 3.666 8.237-8.318 8.285 8.203z"/></svg>'
    delete_ingedrient_btn.className = 'delete-ingredient'
    newIngredient.appendChild(delete_ingedrient_btn)

    // quantity input
    let quantityForm = document.createElement('div')
    quantityForm.className = 'ingredient-quantity-container'

    let quantityInput = document.createElement('input')
    quantityInput.placeholder = '-'
    let measureInput = document.createElement('input')
    measureInput.placeholder = '-'
    quantityInput.className = 'ingredient-quantity', measureInput.className = 'ingredient-measure';
    quantityInput.readOnly = true, measureInput.readOnly = true;
    quantityForm.appendChild(quantityInput), quantityForm.appendChild(measureInput)
    let saveQuantityButton = document.createElement('button')
    saveQuantityButton.innerText = 'add an amount'
    quantityForm.appendChild(saveQuantityButton)

    newIngredient.appendChild(quantityForm)

    let response = await axios.post(`http://127.0.0.1:5000/api${curr_url}/${ingredientName}/add`)
    console.log(response)

    SearchDisplay.innerText = 'Search For an Ingredient:'
    SearchDisplay.style.color = ''

    // take response data and set data ingredient id attribute, then append html elements
    newIngredient.setAttribute('data-ingredient-id', response.data.ingredient_ident)
    ingredientDisplay.appendChild(newIngredient)
    newIngredient.addEventListener('click', editIngredient)
    ingredientSearchBar.value = ''
    custom_ingr_form.style.display = 'none'
    ingredientSuggestions.innerHTML = ''
    ingredientSuggestions.style.display = 'grid'
}

/* ***************************************************************************************
    Get recipe data on load
*/
async function getRecipeInfo() {
    // get recipe data, then get ingredient data
    let recipeInfo = await axios.get(`http://127.0.0.1:5000/api${curr_url}/info`)
    console.log(recipeInfo)
    let recipeSpecificIngredientinfo = await axios.get(`http://127.0.0.1:5000/api${curr_url}/ingredient_info`)
    console.log(recipeSpecificIngredientinfo.data)

    // run rebuildRecipeMarkupOnLoad with ingredient data
    for (let ingredient of recipeInfo.data.recipe.ingredients) {
        let ingredientData = recipeSpecificIngredientinfo.data['ingredientData'][ingredient.ingredient_ident]
        rebuildRecipeMarkupOnLoad(ingredientData)       
    }
}

function rebuildRecipeMarkupOnLoad(ingredientData) {
    // set class, id attribute, and text
    let newIngredient = document.createElement('div')
    newIngredient.classList.add('added-ingredient')
    newIngredient.setAttribute('data-ingredient-id', `${ingredientData.recipe_instance}`)
    newIngredient.innerText = ingredientData.name

    // add delete button
    let delete_ingedrient_btn = document.createElement('div')
    delete_ingedrient_btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206 8.313 3.666 3.666 8.237-8.318 8.285 8.203z"/></svg>'
    delete_ingedrient_btn.className = 'delete-ingredient'
    newIngredient.appendChild(delete_ingedrient_btn)

    // quantity display and form
    let quantityFormWrapper = document.createElement('div')
    quantityFormWrapper.className = 'ingredient-quantity-container'


    let inputContainer = document.createElement('div')

    // get quantity info from ingredientData
    // set paceholders '-' if no data found
    let quantityInput = document.createElement('input')
    let measureInput = document.createElement('input')
    quantityInput.className = 'ingredient-quantity', measureInput.className = 'ingredient-measure';
    if (ingredientData.quantity != null) {
        quantityInput.value = ingredientData.quantity
    }
    else {
        quantityInput.placeholder = '-'
    }
    if (ingredientData.measure != null) {
        measureInput.value = ingredientData.measure
    }
    else {
        measureInput.placeholder = '-'
    }
    quantityInput.readOnly = true, measureInput.readOnly = true;
    inputContainer.appendChild(quantityInput), inputContainer.appendChild(measureInput)

    let saveQuantityButton = document.createElement('button')
    saveQuantityButton.innerText = 'edit'
    inputContainer.appendChild(saveQuantityButton)
    quantityFormWrapper.appendChild(inputContainer)

    newIngredient.appendChild(quantityFormWrapper)
    newIngredient.addEventListener('click', editIngredient)

    ingredientDisplay.appendChild(newIngredient)
}

const editIngredient = function (e) {
    e.preventDefault()
    console.log(e.target.tagName)
    // if edit button is clicked, make inputs editable, add save event listener
    if (e.target.tagName == 'BUTTON') {
        e.target.innerText = 'save';
        let measure = e.target.previousSibling
        let quantity = e.target.previousSibling.previousSibling
        measure.style.backgroundColor = 'white', quantity.style.backgroundColor = 'white'
        measure.readOnly = false, quantity.readOnly = false
        e.currentTarget.removeEventListener('click', editIngredient)
        e.currentTarget.addEventListener('click', saveIngredientQuantity)
    }
    else if (e.target.tagName == 'svg' || e.target.tagName == 'path') {
        // if delete button is pressed, run delete_ingredient_logic with ingredient id
        let ingredient_ident = e.currentTarget.getAttribute('data-ingredient-id')
        console.log(ingredient_ident)
        delete_ingredient_logic(ingredient_ident)
        e.currentTarget.remove()
    }
}

const saveIngredientQuantity = async function (e) {
    e.preventDefault()
    if (e.target.tagName == 'BUTTON') {
        e.target.innerText = 'edit';
        let measure = e.target.previousSibling
        let quantity = e.target.previousSibling.previousSibling
        measure.style.backgroundColor = 'transparent', quantity.style.backgroundColor = 'transparent'
        measure.readOnly = true, quantity.readOnly = true
        let ingredientId = e.currentTarget.getAttribute('data-ingredient-id')
        
        // store quantity info in variables, create object with ingredient info
        let newQuantity = quantity.value
        let newMeasure = measure.value
        let data = {
            'ingredient_ident': ingredientId,
            "quantity": newQuantity,
            "measure": newMeasure,
        }
        let response = await axios.post(`http://127.0.0.1:5000/api${curr_url}/updateIngredient`,
            json = data)
        console.log(response)
        quantity.value = `${response.data.quantity}`
        measure.value = `${response.data.measure}`
        let selectedIngredient = document.querySelector(`[data-ingredient-id = "${response.data.ingredient_ident}"]`)
        selectedIngredient.addEventListener('click', editIngredient)
        selectedIngredient.removeEventListener('click', saveIngredientQuantity)
    }
}

async function delete_ingredient_logic(ingredient_ident) {
    let body = {'ingredient_ident': ingredient_ident }
    await axios.post(`http://127.0.0.1:5000/api${curr_url}/delete_ingredient`, json = body)
}


const delete_tag = async function(e){
    let tag_goner = e.currentTarget
    let tagId = e.currentTarget.getAttribute('data-tag-id')
    let body = {'tag_id': tagId}
    console.log(tagId, e.currentTarget)
    let response = await axios.post(`http://127.0.0.1:5000/api${curr_url}/delete_tag`, json = body)
    if (response.data == 'success'){
        tag_goner.remove()
    }
}

// add event listeners to the tags for deletion
const allTags = document.querySelectorAll('.tag')
for (let tag of allTags){
    tag.addEventListener('click', delete_tag)
}


ingredientSearchBar.addEventListener('keyup', searchHandler);
ingredientSuggestions.addEventListener('click', useSuggestion);
custom_ingr_form.addEventListener('submit', addCustomIngredient);

// instructions
const instructionArea = document.querySelector('.build-instructions')
const instructionInputArea = document.querySelector('#build-instructions-container')
const newInstructionButton = document.querySelector('.new-instruction')


const newInstructionLineClicker = function newInstructionLine(e) {
    let instructionCount = instructionInputArea.childElementCount + 1
    let instructionLine = document.createElement('div')
    instructionLine.className = 'instruction-line'
    let instructionLabel = document.createElement('label')
    instructionLabel.innerText = `${instructionCount}.`
    instructionLine.appendChild(instructionLabel)
    let instructionTextArea = document.createElement('textarea')
    instructionTextArea.className = 'instruction-input'
    instructionLine.appendChild(instructionTextArea)
    instructionInputArea.appendChild(instructionLine)
}

newInstructionButton.addEventListener('click', newInstructionLineClicker)



// submit 
const saveRecipeButton = document.querySelector('.submit')

const saveInstructionInfo = async function (e) {
    let recipeId = e.currentTarget.getAttribute('data-curr-recipe')
    let data = { 'recipe_id': recipeId,'instructions': [] }
    let instructionData = Array.prototype.slice.call(instructionInputArea.children)
    instructionData.forEach(element => {
        let instructionText = element.querySelector('.instruction-input')
        if (instructionText) {
            data['instructions'].push(instructionText.value)
        }
    });
    await axios.post(`http://127.0.0.1:5000/api/save_instructions`, json = data)
}
saveRecipeButton.addEventListener('click', saveInstructionInfo)

/* const get_kroger_access_token = async function(){
    let resp = await axios.get('/api/get_access_token')
    let token = resp.data.access_token
    access_token = token
}

krogerSearchButton = document.querySelector('#kroger')


const search_kroger_ingredients = async function(e){
    e.preventDefault()
    let keyword = ingredientSearchBar.value
    console.log('accesstoken',access_token)
    let resp = await axios.get(`/api/ingredients/search/${keyword}/${access_token}`)
    console.log(resp)
}

krogerSearchButton.addEventListener('click', search_kroger_ingredients) */

getRecipeInfo()