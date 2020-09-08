var update_btns = document.getElementsByClassName('update-cart')

for (var i = 0; i < update_btns.length; i++){

	update_btns[i].addEventListener('click', function(){
		var product_id = this.dataset.product
		var action = this.dataset.action 

		console.log("user:", user)

		 if (user == 'AnonymousUser') {
		 	addtoCookie(product_id, action)
		 }

		 else {
		 	updateUserOrder(product_id, action)
		 }
	})
}

function addtoCookie(product_id,action){
	 if (action == 'add') {
	 	if (cart[product_id] == undefined) {

	 		cart[product_id] = {'quantity' : 1}
	 	}

	 	else{
	 		cart[product_id]['quantity'] += 1
	 	}
	 }

	 else if (action == 'remove') {
	 	cart[product_id]['quantity'] -= 1

	 	if (cart[product_id]['quantity'] <= 0 ) {
	 		delete cart[product_id];

	 }

	}

	 /* the cookie status is updated every 
	 time the method is called */

	 console.log("cart:", cart)

	 document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	 window.location.reload(true);
}


function updateUserOrder(product_id,action){
	var url = 'update_url'

	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},

		body:JSON.stringify({"product_id":product_id,"action":action})
	})

	.then((response) => response.json())
	.then((data) =>{
		console.log('data:',data)
		location.reload(true)
	})
}

