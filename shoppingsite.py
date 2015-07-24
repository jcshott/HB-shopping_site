"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)
                           
                            


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    if "cart" not in session.keys():
        flash("Please add items to cart.")
        return redirect("/melons") 
    else:
        melon_count = {}

        for melon_id in session['cart']:
            melon_count[melon_id] = melon_count.get(melon_id, 0) + 1
            # the_melon = model.Melon.get_by_id(melon_id)

        final_total = 0
        type_total = {}
        for item, frequency in melon_count.items():
            melon_price = model.Melon.get_by_id(item).price
            melon_name = model.Melon.get_by_id(item).common_name
            total = float(frequency) * float(melon_price)
            type_total[melon_name] = [frequency, melon_price, total]
            final_total += total
    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing melons added

    return render_template("cart.html", total=final_total, order_dict=type_total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    session.setdefault('cart', []).append(id)
    flash("Melon successfully added")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    customer = model.Customer.get_by_email(email)

    if customer == None:
        flash("no such email")
        return redirect("/login")
    elif customer.password != password:
        flash("incorrect password")
        return redirect("/login")
    else:
        flash("Successful login!")
        session["logged_in_customer_email"] = True
        return redirect("/melons")

@app.route("/logout")
def process_logout():
    if "logged_in_customer_email" in session:
        return True
    else:
        return False


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
