from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """A view that renders the bag contents page"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""
    # get the quantity from the form and turn it into an interger
    quantity = int(request.POST.get("quantity"))

    # get the url to redirect to from the form
    redirect_url = request.POST.get("redirect_url")

    size = None
    # check if the user selected a size, if so set the size to what was selected
    if "product_size" in request.POST:
        size = request.POST["product_size"]

    # get the bag from the session, if it doesn't exist, create an empty dictionary
    bag = request.session.get("bag", {})
    # Check if size has been added
    if size:
        if item_id in list(
            bag.keys()
        ):  # if the item is already in the bag, add the new size to the existing quantity
            if size in bag[item_id]["items_by_size"].keys():
                bag[item_id]["items_by_size"][
                    size
                ] += quantity  # update the quantity of the size
            else:
                bag[item_id]["items_by_size"][
                    size
                ] = quantity  # add the size to the bag
        else:
            bag[item_id] = {"items_by_size": {size: quantity}}
    else:
        # if the item is already in the bag, add the new quantity to the existing quantity
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        # if the item is not in the bag, add it to the bag with the quantity specified
        else:
            bag[item_id] = quantity

    request.session["bag"] = bag  # save the bag back to the session
    return redirect(redirect_url)  # redirect to the url specified in the form
