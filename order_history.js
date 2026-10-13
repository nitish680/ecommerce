
const message = document.getElementById("message");
const ordersContainer = document.getElementById("orders-container");

async function loadOrderHistory() {
    const token = localStorage.getItem("token");

    // Check whether the customer is logged in
    if (!token) {
        window.location.href="login.html";
        return;
    }

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/orders/history",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (response.status === 401) {
            localStorage.removeItem("token");
            localStorage.removeItem("user_name");
            localStorage.removeItem("user_role");

            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load orders.");
        }

        const orders = data.orders;

        message.textContent = "";

        if (orders.length === 0) {
            message.textContent = "You haven't placed any orders yet.";
            return;
        }

        for (const order of orders) {
            const card = document.createElement("section");
            card.className = "order-card";

            const date = order.created_time
                ? new Date(order.created_time).toLocaleString()
                : "Date unavailable";

            const header = document.createElement("div");
            header.className = "order-header";

            const orderInfo = document.createElement("div");
            const orderId = document.createElement("h3");
            orderId.textContent = `Order #${order.order_id}`;

            const orderDate = document.createElement("p");
            orderDate.textContent = date;

            orderInfo.append(orderId, orderDate);

            const status = document.createElement("span");
            status.className = "status";
            status.textContent = order.status;

            header.append(orderInfo, status);
            card.appendChild(header);

            const itemsContainer = document.createElement("div");
            itemsContainer.className = "order-items";

            for (const item of order.items) {
                const itemRow = document.createElement("div");
                itemRow.className = "order-item";

                const name = document.createElement("span");
                name.textContent =
                    `${item.product_name} × ${item.quantity}`;

                const price = document.createElement("span");
                price.textContent =
                    `₹${Number(item.total).toFixed(2)}`;

                itemRow.append(name, price);
                itemsContainer.appendChild(itemRow);
            }

            card.appendChild(itemsContainer);

            const total = document.createElement("div");
            total.className = "order-total";
            total.textContent =
                `Order Total: ₹${Number(order.total_amount).toFixed(2)}`;

            card.appendChild(total);
            ordersContainer.appendChild(card);
        }

    } catch (error) {
        message.textContent = error.message;
    }
}

let logbtn=document.getElementById("logout_btn");
if (logbtn) {
    logbtn.addEventListener("click",function(){
        localStorage.removeItem("token");
        localStorage.removeItem("user_name");
        localStorage.removeItem("user_role");
        window.location.href="login.html";
    });
}
loadOrderHistory();
