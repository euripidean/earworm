window.onload = function(){
const rating = document.querySelector('.rating-wrapper');
if (rating) {
    document.querySelector('.rating-wrapper').addEventListener('click', updateStarRating, false);
}
    
function updateStarRating(evt){
    for(i=0; i < parseInt(evt.target.id); i++){
        const stars = document.querySelectorAll('.rating-wrapper img');
        for(s=0; s < 5; s++){
            stars[s].classList.remove('rating-checked');
        }
        for(j=0; j < parseInt(evt.target.id); j++){
            stars[j].classList.add('rating-checked');
        }
    }
    document.querySelector('#rating').value = evt.target.id;
}

// Scripts for deleting records alerts
const deleteProfile = document.querySelector('#delete-profile');
if (deleteProfile) {
    document.querySelector('#delete-profile').addEventListener('click', deleteAlert, false);
    document.querySelector('#cancel-delete').addEventListener('click', cancelDelete, false);
}

const deleteReview = document.querySelector('#delete-review');
if (deleteReview) {
    document.querySelector('#delete-review').addEventListener('click', deleteAlert, false);
    document.querySelector('#cancel-delete').addEventListener('click', cancelDelete, false);
}

function deleteAlert(e){
    e.preventDefault();
    const deletion = document.getElementById('delete')
    deletion.classList.remove('hidden');
}


function cancelDelete(e){
    e.preventDefault();
    const deletion = document.getElementById('delete')
    deletion.classList.add('hidden');
}
}










