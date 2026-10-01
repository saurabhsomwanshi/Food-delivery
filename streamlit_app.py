import streamlit as st

# Import OOP classes from your project file
from food_delivery import Customer, Restaurant, MenuItem, DeliveryPartner


st.set_page_config(
    page_title="Food Delivery System",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Food Delivery System")
st.caption("Simple Streamlit interface for the Food Delivery OOP project")


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "restaurant" not in st.session_state:
    st.session_state.restaurant = None

if "partner" not in st.session_state:
    st.session_state.partner = None

if "order" not in st.session_state:
    st.session_state.order = None

if "message" not in st.session_state:
    st.session_state.message = ""


# ---------------------------------------------------------
# Sidebar - Create Customer
# ---------------------------------------------------------
st.sidebar.header("👤 Customer")

with st.sidebar.form("customer_form"):
    customer_name = st.text_input("Name", "Priya")
    customer_phone = st.text_input("Phone", "9876543210")
    customer_address = st.text_input("Address", "Bangalore")

    create_customer = st.form_submit_button("Create Customer")

if create_customer:
    st.session_state.customer = Customer(
        customer_name,
        customer_phone,
        customer_address
    )
    st.session_state.message = "Customer created successfully."


# Wallet
if st.session_state.customer:
    st.sidebar.divider()
    st.sidebar.subheader("💰 Wallet")

    st.sidebar.write(
        f"Balance: ₹{st.session_state.customer._wallet_balance:.2f}"
    )

    wallet_amount = st.sidebar.number_input(
        "Add wallet balance",
        min_value=0.0,
        step=50.0
    )

    if st.sidebar.button("Add Money"):
        st.session_state.customer.add_to_wallet(wallet_amount)
        st.session_state.message = (
            f"₹{wallet_amount:.2f} added to wallet."
        )


# ---------------------------------------------------------
# Restaurant setup
# ---------------------------------------------------------
st.header("🍽️ Restaurant")

col1, col2 = st.columns(2)

with col1:
    if st.button("Create Restaurant"):
        restaurant = Restaurant("Bawarchi", "MG Road")

        restaurant.add_item(MenuItem("Biryani", 250, False))
        restaurant.add_item(MenuItem("Kebab", 180, False))
        restaurant.add_item(MenuItem("Paneer Tikka", 220, True))
        restaurant.add_item(MenuItem("Veg Biryani", 200, True))

        st.session_state.restaurant = restaurant
        st.session_state.message = "Restaurant created with menu."


with col2:
    if st.session_state.restaurant:
        st.success(
            f"{st.session_state.restaurant.name} - "
            f"{st.session_state.restaurant.location}"
        )
        st.write(
            "Open:",
            "Yes" if st.session_state.restaurant.is_open() else "No"
        )


# ---------------------------------------------------------
# Show menu
# ---------------------------------------------------------
if st.session_state.restaurant:
    st.subheader("📋 Restaurant Menu")

    menu = st.session_state.restaurant.get_menu()

    for i, item in enumerate(menu):
        veg_text = "🌱 Veg" if item.is_veg else "🍗 Non-Veg"
        st.write(f"**{i + 1}. {item.name}** — ₹{item.price} — {veg_text}")


# ---------------------------------------------------------
# Place Order
# ---------------------------------------------------------
st.header("🛒 Place Order")

if not st.session_state.customer:
    st.info("Create a customer first.")

elif not st.session_state.restaurant:
    st.info("Create the restaurant first.")

else:
    menu = st.session_state.restaurant.get_menu()

    selected_items = st.multiselect(
        "Select food items",
        options=menu,
        format_func=lambda item: f"{item.name} - ₹{item.price}"
    )

    if selected_items:
        subtotal = sum(item.price for item in selected_items)
        gst = subtotal * 0.05
        packaging_fee = 20
        total = subtotal + gst + packaging_fee

        st.write(f"Subtotal: ₹{subtotal:.2f}")
        st.write(f"GST (5%): ₹{gst:.2f}")
        st.write(f"Packaging fee: ₹{packaging_fee:.2f}")
        st.subheader(f"Total: ₹{total:.2f}")

    if st.button("Place Order", type="primary"):
        if not selected_items:
            st.warning("Please select at least one item.")
        else:
            total = (
                sum(item.price for item in selected_items) * 1.05
                + 20
            )

            if st.session_state.customer._wallet_balance < total:
                st.error("Insufficient wallet balance.")
            else:
                # Deduct amount from wallet for this Streamlit demo.
                st.session_state.customer._wallet_balance -= total

                order = st.session_state.customer.place_order(
                    st.session_state.restaurant,
                    selected_items
                )

                st.session_state.order = order
                st.session_state.message = "Order placed successfully."


# ---------------------------------------------------------
# Order details
# ---------------------------------------------------------
if st.session_state.order:
    order = st.session_state.order

    st.header("📦 Order Details")

    subtotal = sum(item.price for item in order._items)
    gst = subtotal * 0.05
    packaging_fee = 20
    total = order.calculate_bill()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Order ID", order._order_id)
    c2.metric("Subtotal", f"₹{subtotal:.2f}")
    c3.metric("GST", f"₹{gst:.2f}")
    c4.metric("Total", f"₹{total:.2f}")

    st.write("**Status:**", order._status)
    st.write("**Estimated time:**", f"{order.estimated_time()} minutes")

    # Show OTP for this demo.
    # In a real application, OTP would be sent privately to the customer.
    st.info(f"Demo OTP: {order._otp}")


# ---------------------------------------------------------
# Delivery Partner
# ---------------------------------------------------------
st.header("🏍️ Delivery Partner")

col1, col2 = st.columns(2)

with col1:
    with st.form("partner_form"):
        partner_name = st.text_input("Partner Name", "Rajesh")
        partner_phone = st.text_input("Partner Phone", "9999999999")
        vehicle = st.selectbox("Vehicle", ["Bike", "Scooter", "Cycle"])

        create_partner = st.form_submit_button("Create Delivery Partner")

    if create_partner:
        st.session_state.partner = DeliveryPartner(
            partner_name,
            partner_phone,
            vehicle
        )
        st.session_state.message = "Delivery partner created."


with col2:
    if st.session_state.partner:
        partner = st.session_state.partner

        st.write(f"**Name:** {partner._name}")
        st.write(f"**Vehicle:** {partner.vehicle}")
        st.write(
            "**Available:**",
            "Yes" if partner.is_available else "No"
        )


# ---------------------------------------------------------
# Accept Order
# ---------------------------------------------------------
if st.session_state.order and st.session_state.partner:
    st.subheader("🚚 Delivery Actions")

    order = st.session_state.order
    partner = st.session_state.partner

    if order._status == "Placed":
        if st.button("Accept Order"):
            if partner.is_available:
                partner.accept_order(order)
                st.session_state.message = "Order accepted by delivery partner."
            else:
                st.error("Delivery partner is not available.")

    elif order._status == "Accepted":
        st.success("Order accepted. Enter OTP to complete delivery.")

        entered_otp = st.number_input(
            "Enter Customer OTP",
            min_value=1000,
            max_value=9999,
            step=1
        )

        if st.button("Complete Delivery", type="primary"):
            # First check OTP so the UI can show a clear result.
            if order.verify_otp(entered_otp):
                partner.deliver(order, entered_otp)

                st.session_state.customer.notify("Order delivered")
                partner.notify("Order delivered")

                st.session_state.message = "Delivery completed successfully."
            else:
                st.error("Incorrect OTP. Delivery is not completed.")

    elif order._status == "Delivered":
        st.success("🎉 Order Delivered Successfully!")
        st.write("Customer has received the order.")


# ---------------------------------------------------------
# Notifications
# ---------------------------------------------------------
if st.session_state.message:
    st.divider()
    st.success(st.session_state.message)


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------
st.sidebar.divider()

if st.sidebar.button("Reset Demo"):
    for key in [
        "customer",
        "restaurant",
        "partner",
        "order",
        "message"
    ]:
        st.session_state[key] = None if key != "message" else ""

    st.rerun()
