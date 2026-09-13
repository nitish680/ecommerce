// alert("javascript is connected");
console.log("script.js loaded");
const products=[];

products.push({
    id:5,
    image:"images/headphones.jpg",
    name : "WirelessHeadphones",
    price    : 1900,
    rating   : 4.5,
    reviews  : 128,
    category : "Electronics",
});
products.push({
    id:4,
    image:"images/headphones.jpg",
    name : "laptop",
    price    : 2900,
    rating   : 4.5,
    reviews  : 129,
    category : "Electronics",
});
products.push({
    id:3,
    image:"images/headphones.jpg",
    name : "LED",
    price    : 29000,
    rating   : 4.5,
    reviews  : 17,
    category : "Electronics",
});
products.push({
    id:2,
    image:"images/headphones.jpg",
    name : "LED",
    price    : 29000,
    rating   : 4.5,
    reviews  : 17,
    category : "Electronics",
});
products.push({
    id:1,
    image:"images/headphones.jpg",
    name : "LED",
    price    : 29000,
    rating   : 4.5,
    reviews  : 17,
    category : "Electronics",
});
let cart = JSON.parse(localStorage.getItem("cart")) || [];

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
    
    button.addEventListener("click",function(){
        console.log("BUTTON CLICKED:", product.name);
        cart = JSON.parse(localStorage.getItem("cart")) || [];
        const existingitem =cart.find(function(item){
            return item.product.id === product.id;
        });
        if(existingitem){
            existingitem.quantity++;
            
        }
        else{
            const quantity=1;
            cart.push({product,quantity});
        }
        // cart.push(product);
        
        console.log(cart);
        localStorage.setItem("cart",JSON.stringify(cart));
    });
    container.appendChild(card);
    

}

