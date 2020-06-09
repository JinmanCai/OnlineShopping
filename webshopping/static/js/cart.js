var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var championId = this.dataset.product
        var action = this.dataset.action
        console.log('championId:',championId,'action:',action)

        console.log('USER:', user)
        if(user === 'AnonymosUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(championId,action)
        }
    })

}

function updateUserOrder(championId,action){
    console.log('user is logged in, sending data')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'championId':championId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })

}
