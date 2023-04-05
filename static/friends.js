// follow and unfollow users
const currentSearchedUsers = document.querySelectorAll('.user-card-wrapper')
let curr_url = window.location.pathname

const selectSearchedUser = function(e){
    let user_id = e.currentTarget.getAttribute('data-user-id')
    if( e.target.tagName == 'BUTTON'){
        e.preventDefault()
        followUser(user_id)
    }
}


async function followUser(user_id){
    let response = await axios.post(`${baseURL}/api${curr_url}/add/${user_id}`)
    console.log(response)
}

async function unfollowUser(user_id){
    let response = await axios.post(`${baseURL}/api${curr_url}/remove/${user_id}`)
}
/* for (let card of currentSearchedUsers){
    card.addEventListener('click', selectSearchedUser)
} */

// switch between following and followers tab

const friendTabs = document.querySelectorAll('.profile-tab')
const followingTab = friendTabs[0]
const followerTab = friendTabs[1]

const followingListContainer = document.querySelector('#following-list-container')
const followerListContainer = document.querySelector('#followers-list-container')

function switchTabs(e){
    if (e.currentTarget == followingTab && !(e.currentTarget.classList.contains('active-tab'))){
        followingTab.classList.toggle('active-tab')
        followerTab.classList.toggle('active-tab')
        followingListContainer.style.display = 'grid'
        followerListContainer.style.display = 'none'
    }
    else if (e.currentTarget == followerTab && !(e.currentTarget.classList.contains('active-tab'))){
        followerTab.classList.toggle('active-tab')
        followingTab.classList.toggle('active-tab')
        followingListContainer.style.display = 'none'
        followerListContainer.style.display = 'grid'
    }
    
}

for (tab of friendTabs){
    tab.addEventListener('click', switchTabs)
}
