var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var championId = this.dataset.product
        var action = this.dataset.action
        console.log('championId:',championId,'action:',action)

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            addCookieItem(championId, action)
        }else{

            updateUserOrder(championId, action)

        }
    })

}

function addCookieItem(championId, action){
    console.log('USER IS A GUEST')

    if (action == 'add'){
        if (cart[championId] == undefined){
            cart[championId] = {'quantity':1}
        }else{
            cart[championId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[championId]['quantity'] -= 1

        if (cart[championId]['quantity'] <= 0){
            console.log('item removed')
            delete cart[championId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
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
