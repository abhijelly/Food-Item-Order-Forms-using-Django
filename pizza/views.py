from textwrap import fill
from django.shortcuts import render
from django.forms import formset_factory

from .models import Pizza

from .forms import PizzaForm, MultiplePizzaForm

def home(request):
    return render(request, "pizza/home.html")

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == "POST":
        filled_form = PizzaForm(request.POST) # form contains the filled data
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            print("created_pizza_id: {}".format(created_pizza_pk))

            # Show a confirmation note
            note = "Success! Your %s %s and %s pizza order has been placed" %(filled_form.cleaned_data["size"],
            filled_form.cleaned_data["topping1"],
            filled_form.cleaned_data["topping2"],)

            filled_form = PizzaForm()
        else:
            created_pizza_pk = None
            note = "Your pizza order has failed. Try again."
        return render(request, "pizza/order.html", {"created_pizza_pk": created_pizza_pk, "pizzaform": filled_form, "note": note, "mutiple_form":multiple_form})

    else:
        form = PizzaForm()
        return render(request, "pizza/order.html", {"pizzaform": form, "multiple_form": multiple_form})

def pizzas(request):
    number_of_pizzas = 2
    
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data["number"]
    
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas) # formset_factory creates a class
    formset = PizzaFormSet() 

    if request.method == "POST":
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data["topping1"]) # prints topping 1 on the terminal``
                note = "Pizzas has been ordered!"
        else:
            note = "Order was not placed, please try again :("
        
        return render(request, "pizza/pizzas.html", {"note": note, "formset": formset})
    else:
        return render(request, "pizza/pizzas.html", {"formset": formset})

def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    
    if request.method == "POST":
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "Your order has been updated"
            return render(request, "pizza/edit_order.html", {"note": note, "pizzaform": form, "pizza":pizza})
        
    return render(request, "pizza/edit_order.html", {"pizzaform": form, "pizza": pizza})
        


