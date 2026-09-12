// alert("javascript is connected");
const products=[];
products.push({
    image:"images/headphones.jpg",
    name : "WirelessHeadphones",
    price    : 1900,
    rating   : 4.5,
    reviews  : 128,
    category : "Electronics",
});
products.push({
    image:"images/headphones.jpg",
    name : "laptop",
    price    : 2900,
    rating   : 4.5,
    reviews  : 129,
    category : "Electronics",
});
products.push({
    image:"images/headphones.jpg",
    name : "LED",
    price    : 29000,
    rating   : 4.5,
    reviews  : 17,
    category : "Electronics",
});
products.push({
    image:"images/headphones.jpg",
    name : "LED",
    price    : 29000,
    rating   : 4.5,
    reviews  : 17,
    category : "Electronics",
});
products.push({
    image:"images/headphones.jpg",
    name : "LED",
    price    : 29000,
    rating   : 4.5,
    reviews  : 17,
    category : "Electronics",
});
const cart=[];
for(const product of products){
    const card=document.createElement("div");
    const container=document.getElementById("product-container")
    card.className="product-card";
    card.innerHTML=`
    <img src="${product.image}">
    <h2>${product.name}</h2>
    <p>${product.rating}</p>
    <p>${product.price}</p>
    <button>AddCart</button>
    
    `;
    const button=card.querySelector("button");
    const quantity=0;
    button.addEventListener("click",function(){
        if(!cart.includes(product)){
            quantity+=1;
            cart.push({product,quantity});
        }
        // cart.push(product);
        quantity+=1;
        
        console.log(cart);
    });
    container.appendChild(card);
    

}

