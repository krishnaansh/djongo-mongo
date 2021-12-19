"""Handle Stripe Payment Gateway"""

# python imports
import os

# Third Party import
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, response
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# local import
from odata.models import Product, Payment, Customer
from Project.settings import STRIPE_SECRET_KEY, STRIPE_PUBLISH_KEY, DOMAIN_URL

stripe.api_key = STRIPE_SECRET_KEY


class StipeCheckoutSession(TemplateView):
    """Stripe Checkout View for stripe checkout payment"""

    template_name = "stripe.html"

    def get_context_data(self, **kwargs):
        context = super(StipeCheckoutSession, self).get_context_data(**kwargs)
        context["product_ids"] = self.request.GET.get("p_ids")
        context["quantity"] = self.request.GET.get("qty")
        context["STRIPE_PUBLISH_KEY"] = STRIPE_PUBLISH_KEY

        return context


class CreateCheckoutSession(APIView):
    """Class to create CheckoutSession

    Args:
        APIView (class): ResT framework APIView class
    """

    def get(self, request):
        try:
            domain_url = DOMAIN_URL
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            product_ids = self.request.GET.get("p_ids")
            quantities = self.request.GET.get("qty")
            if product_ids:
                quantities = quantities.split(",")
                cart_items = []
                i = 0
                for product in product_ids.split(","):
                    single_pro = Product.get(product)
                    if single_pro:
                        cart_items.append(
                            {
                                "name": single_pro.product_name,
                                "quantity": quantities[i],
                                "currency": "eur",
                                "amount": single_pro.price * 100,
                            }
                        )
                        i = i + 1
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url
                + "stripe/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "stripe/cancelled",
                payment_method_types=["card"],
                mode="payment",
                line_items=cart_items,
            )
            return response.Response({"sessionId": checkout_session["id"]})
        except Exception as e:
            return response.Response(error=str(e), status=status.HTTP_403_FORBIDDEN)


class StripeWebHookView(APIView):
    def post(self, request):
        payload = request.POST
        sig_header = request.headers.get("Stripe-Signature")
        STRIPE_WEBHOOK_SECRET = "whsec_0SGVwxVCbmjZuGDFmZruPV8v1xGSqHVf"
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )

        except ValueError as e:
            # Invalid payload
            return response.Response(
                {"msg": "Invalid payload", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return response.Response(
                {"msg": "Invalid payload", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            print("Payment was successful.")
            # TODO: run some custom code here

        return "Success", 200


def success(request):
    stripe_session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    cust = stripe.Customer.retrieve(stripe_session.customer)
    customer = Customer.get(cust.email)
    import uuid, datetime

    if customer:
        data = {
            "customer": customer,
            "order": uuid.uuid4().hex[:6].upper(),
            "invoice": dict(stripe_session),
            "amount": stripe_session.amount_total / 100,
            "payment_type": "card/stripe",
            "date_of_payment": datetime.datetime.now(),
            "status": stripe_session.payment_status,
        }
        payment_data = Payment.objects.create(**data)

    return "/"
