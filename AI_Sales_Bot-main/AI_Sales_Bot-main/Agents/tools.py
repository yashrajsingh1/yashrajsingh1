import json
import stripe
from fuzzywuzzy import process
from langchain.agents import tool

# Load Product Catalog
with open("product_catalog.json", "r") as file:
    PRODUCT_CATALOG = json.load(file)


@tool
def get_product_info(search_term: str) -> dict:
    """Retrieve product details by product ID, name, or category."""
    for product in PRODUCT_CATALOG:
        if product["id"] == search_term:
            return product

    product_names = [product["name"] for product in PRODUCT_CATALOG]
    best_match, score = process.extractOne(search_term, product_names)
    if score > 70:
        for product in PRODUCT_CATALOG:
            if product["name"] == best_match:
                return product

    return {"error": "Product not found"}


@tool
def generate_stripe_payment_link(product_id: str, customer_email: str) -> str:
    """Generate Stripe payment link for a product."""
    product = get_product_info(product_id)
    if "error" in product:
        return product["error"]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': product['stripe_price_id'],
                'quantity': 1,
            }],
            mode='payment',
            customer_email=customer_email,
            success_url='https://yourdomain.com/success',
            cancel_url='https://yourdomain.com/cancel',
        )
        return session.url
    except Exception as e:
        return f"Error creating payment link: {str(e)}"


@tool
def check_mindware_compatibility(customer_industry: str) -> str:
    """Check solution compatibility with customer's industry through Mindware."""
    compatible_industries = ["technology",
                             "finance", "healthcare", "education"]
    return "Compatible" if customer_industry.lower() in compatible_industries else "Not Compatible"


@tool
def schedule_demo(customer_email: str, preferred_date: str) -> str:
    """Schedule product demo (mock implementation). Date format: YYYY-MM-DD"""
    return f"Demo scheduled for {preferred_date}. Confirmation sent to {customer_email}."


@tool
def send_email(customer_email: str, subject: str, body: str) -> str:
    """Send email to customer (mock implementation)."""
    return f"Email sent to {customer_email}: {subject} - {body[:50]}..."


@tool
def process_refund(payment_id: str) -> str:
    """Process payment refund using Stripe."""
    try:
        refund = stripe.Refund.create(payment_intent=payment_id)
        return f"Refund processed: {refund.id}"
    except stripe.error.StripeError as e:
        return f"Error processing refund: {e.user_message}"


@tool
def check_system_requirements(os: str, ram_gb: int) -> str:
    """Check system compatibility."""
    compatible = ram_gb >= 8 and os.lower() in ["windows 10", "linux", "macos"]
    return "System compatible" if compatible else "System incompatible"


@tool
def get_installation_guide(product_id: str) -> str:
    """Retrieve product installation guide."""
    product = get_product_info(product_id)
    return product.get("installation_url", "https://example.com/installation")


@tool
def collect_feedback(feedback: str) -> str:
    """Collect customer feedback."""
    return f"Feedback received: {feedback}"
