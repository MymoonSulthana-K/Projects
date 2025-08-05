import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import random
from connection import insert_ticket_details, view_ticket_details, get_price_by_show_and_category

app = FastAPI()

# Define data models for ticket booking requests
class TicketBookingRequest(BaseModel):
    name: str
    tickets: str
    date: str
    shows : str
    category_id : str

class TicketViewRequest(BaseModel):
    number: float

buffer = []
ticket_id = random.randint(1, 1000)
while ticket_id in buffer:
    ticket_id = random.randint(1, 1000)
buffer.append(ticket_id)

@app.get("/webhook")
async def read_root():
    return {"message": "Welcome to the TicketBot API. Use POST to access the webhook!"}

@app.post("/webhook")
async def handle_webhook(request: dict):
    # Log the incoming request for debugging
    print("Incoming request:", json.dumps(request, indent=2))
    
    # Extract intent from the request
    intent = request.get("queryResult", {}).get("intent", {}).get("displayName")
    
    # Handle different intents
    if intent == "view_ticket:ongoing-viewing":
        return await handle_view_ticket(request.get("queryResult").get("parameters", {}))
    
    elif intent == "book_ticket - shows":
        output_contexts = request.get("queryResult").get("outputContexts", [])
        context_suffix = "ongoing-booking"

        specific_context = next(
            (context for context in output_contexts if context['name'].endswith(context_suffix)), 
            None
        )

        if specific_context:
            return await handle_book_ticket(specific_context.get("parameters", {}))
        else:
            return "Context not found"
    
    raise HTTPException(status_code=400, detail="Intent not recognized")

async def handle_view_ticket(parameters: dict):
    # Create a TicketViewRequest instance from parameters
    ticket_view_request = TicketViewRequest(**parameters)
    ticket_id = str(int(ticket_view_request.number))

    # Retrieve ticket details from the database
    ticket_details = view_ticket_details(ticket_id)

    if not ticket_details:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Return the ticket details in the response
    return {
        "fulfillmentText": (
            f"Ticket ID: {ticket_details[0]}\n"
            f"Name: {ticket_details[1]}\n"
            f"Quantity: {ticket_details[6]}\n"
            f"Date: {datetime.fromisoformat(str(ticket_details[4])).date()}\n"
            f"Total Price: Rs.{ticket_details[5]:.2f}"
        )
    }

async def handle_book_ticket(parameters: dict):
    # Extract relevant fields, including nested ones, from the parameters
    name = parameters['person'].get('name')  # Extract the name from person
    tickets = parameters.get('tickets')
    date = parameters.get('date')
    shows = parameters.get('shows')
    category_id = parameters.get('category_id')

    # Create a TicketBookingRequest instance manually with the extracted data
    ticket_booking_request = TicketBookingRequest(
        name=name,
        tickets=tickets,
        date=date,
        shows=shows,
        category_id=category_id
    )

    # Retrieve show_id and category_id
    dt = datetime.fromisoformat(date)
    date_only = dt.date()
    show_id = int(shows)
    category_id = int(category_id)
    quantity = int(tickets)

    # Retrieve price based on show_id and category_id
    price_info = get_price_by_show_and_category(show_id, category_id)

    if price_info is None:
        raise HTTPException(status_code=404, detail="Price not found for the given show and category")

    total_price = price_info * quantity

    # Create a new ticket and insert it into the database
    insert_ticket_details(ticket_id,name, category_id, show_id,date_only, total_price,quantity)

    # Return a response indicating the booking was successful
    return {
        "fulfillmentText": (
            f"Booking successful! Your Ticket ID is: {ticket_id}\n"
            f"Name: {ticket_booking_request.name}\n"
            f"Quantity: {ticket_booking_request.tickets}\n"
            f"Total Price: Rs.{total_price:.2f}"
            "\nClick to pay : https://i.postimg.cc/d382wYnB/pay.jpg",
        )
}

