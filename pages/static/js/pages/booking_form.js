document.addEventListener('DOMContentLoaded', function () {
    const wantsFlightSelect = document.querySelector('#id_booking_wants_flight');
    const fromAirportSelect = document.querySelector('#id_booking_from_airport');
    const pickupSelect = document.querySelector('#id_booking_airport_pickup');
    const dropoffSelect = document.querySelector('#id_booking_airport_dropoff');
    const fromAirportGroup = document.getElementById('booking-from-airport-group');
    const pickupGroup = document.getElementById('booking-pickup-group');
    const dropoffGroup = document.getElementById('booking-dropoff-group');

    function toggleFlightFields() {
        const isChecked = wantsFlightSelect?.value === 'True';
        fromAirportGroup.style.display = isChecked ? 'block' : 'none';
        pickupGroup.style.display = isChecked ? 'block' : 'none';
        dropoffGroup.style.display = isChecked ? 'block' : 'none';

        const airportSelected = fromAirportSelect?.value !== '';
        const enableAirportOptions = isChecked && airportSelected;
        pickupSelect.disabled = !enableAirportOptions;
        dropoffSelect.disabled = !enableAirportOptions;
    }

    const wantsCarRentalSelect = document.querySelector('#id_booking_car_rental');
    const rentDaysGroup = document.getElementById('booking-rent-days-group');

    function toggleRentalFields() {
        rentDaysGroup.style.display = wantsCarRentalSelect?.value === 'True' ? 'block' : 'none';
    }

    // === INITIALIZE TOGGLES ===
    wantsFlightSelect?.addEventListener('change', () => {
        toggleFlightFields();
        updatePrice();
    });
    fromAirportSelect?.addEventListener('change', () => {
        toggleFlightFields();
        updatePrice();
    });
    toggleFlightFields();

    wantsCarRentalSelect?.addEventListener('change', () => {
        toggleRentalFields();
        updatePrice();
    });
    toggleRentalFields();

    const totalPriceSpan = document.getElementById('total-price');
    const ticketPriceSpan = document.getElementById('ticket-price');
    const mealPlanPriceSpan = document.getElementById('meal-plan-price');
    const airportPriceSpan = document.getElementById('airport-price');
    const carRentalPriceSpan = document.getElementById('car-rental-price');
    const adultTicketTotalSpan = document.getElementById('adult-ticket-total');
    const childTicketTotalSpan = document.getElementById('child-ticket-total');

    const pricingData = document.getElementById('booking-pricing-data');

    const adultTicketsInput = document.getElementById('id_booking_tickets_adult');
    const childTicketsInput = document.getElementById('id_booking_tickets_child');
    const mealPlanSelect = document.getElementById('id_booking_meal_plan');
    const carRentalDaysInput = document.getElementById('id_booking_car_rental_days');

    const adultUnitPrice = parseFloat(pricingData?.dataset.adultUnitPrice) || 0;
    const childUnitPrice = parseFloat(pricingData?.dataset.childUnitPrice) || 0;
    const duration = parseInt(pricingData?.dataset.duration) || 1;

    const mealPrices = {
        None: parseFloat(pricingData?.dataset.mealNone) || 0,
        BB: parseFloat(pricingData?.dataset.mealBb) || 0,
        HB: parseFloat(pricingData?.dataset.mealHb) || 0,
        FB: parseFloat(pricingData?.dataset.mealFb) || 0,
        AI: parseFloat(pricingData?.dataset.mealAi) || 0
    };

    function updateMealPlanOptionsPricePerPerson() {
        const mealPriceSpans = {
            'BB': document.getElementById('meal-bb-price'),
            'HB': document.getElementById('meal-hb-price'),
            'FB': document.getElementById('meal-fb-price'),
            'AI': document.getElementById('meal-ai-price'),
        };

        for (const plan in mealPriceSpans) {
            const span = mealPriceSpans[plan];
            const perPersonTotal = (mealPrices[plan] || 0) * duration;
            if (span) {
                span.textContent = perPersonTotal.toFixed(2);
            }
        }
    }

    updateMealPlanOptionsPricePerPerson();

    const carRentalPerDay = parseFloat(pricingData?.dataset.carRentalCost) || 0;
    const airportPickupCost = parseFloat(pricingData?.dataset.airportPickup) || 0;
    const airportDropoffCost = parseFloat(pricingData?.dataset.airportDropoff) || 0;
    const toCountry = pricingData?.dataset.toCountry || '';
    const toContinent = pricingData?.dataset.toContinent || '';

    const airportJsonTag = document.getElementById('airport-json');
    const airportData = JSON.parse(airportJsonTag.textContent);

    function calculateFlightCost() {
        const airportId = fromAirportSelect?.value;
        if (!airportId || !airportData[airportId]) return 0;

        const airport = airportData[airportId];
        const fromCountry = airport.country;
        const fromContinent = airport.continent;
        const baseTicket = airport.standard_ticket;

        if (fromContinent !== toContinent) {
            return baseTicket * 1.5;
        } else if (fromCountry !== toCountry) {
            return baseTicket * 1.3;
        } else {
            return baseTicket;
        }
    }

    function updatePrice() {
        const adultTickets = parseInt(adultTicketsInput?.value) || 0;
        const childTickets = parseInt(childTicketsInput?.value) || 0;
        const totalTickets = adultTickets + childTickets;

        const selectedMealPlan = mealPlanSelect?.value || 'None';
        const mealPricePerPerson = mealPrices[selectedMealPlan] || 0;

        const wantsCarRental = wantsCarRentalSelect?.value === 'True';
        const rentalDays = parseInt(carRentalDaysInput?.value) || 0;
        const rentalTotal = wantsCarRental ? rentalDays * carRentalPerDay : 0;

        const ticketTotal = (adultTickets * adultUnitPrice) + (childTickets * childUnitPrice);
        const mealTotal = totalTickets * mealPricePerPerson * duration;

        const wantsFlight = wantsFlightSelect?.value === 'True';
        const fromAirportSelected = fromAirportSelect?.value !== '';
        const wantsPickup = pickupSelect?.value === 'True';
        const wantsDropoff = dropoffSelect?.value === 'True';

        const adultTotal = adultTickets * adultUnitPrice;
        const childTotal = childTickets * childUnitPrice;

        let airportServiceTotal = 0;
        if (wantsFlight && fromAirportSelected) {
            if (wantsPickup) airportServiceTotal += airportPickupCost * totalTickets;
            if (wantsDropoff) airportServiceTotal += airportDropoffCost * totalTickets;
        }

        let flightTotal = 0;
        if (wantsFlight && fromAirportSelected) {
            flightTotal = calculateFlightCost() * totalTickets;
        }

        const total = ticketTotal + mealTotal + rentalTotal + airportServiceTotal + flightTotal;

        totalPriceSpan.textContent = total.toFixed(2);
        ticketPriceSpan.textContent = ticketTotal.toFixed(2);
        mealPlanPriceSpan.textContent = mealTotal.toFixed(2);
        airportPriceSpan.textContent = (airportServiceTotal + flightTotal).toFixed(2);
        const airportServicePriceSpan = document.getElementById('airport-service-price');
        const flightTicketPriceSpan = document.getElementById('flight-ticket-price');

        if (airportServicePriceSpan) {
            airportServicePriceSpan.textContent = airportServiceTotal.toFixed(2);
        }
        if (flightTicketPriceSpan) {
            flightTicketPriceSpan.textContent = flightTotal.toFixed(2);
        }
        carRentalPriceSpan.textContent = rentalTotal.toFixed(2);
        adultTicketTotalSpan.textContent = adultTotal.toFixed(2);
        childTicketTotalSpan.textContent = childTotal.toFixed(2);
    }

    adultTicketsInput?.addEventListener('input', updatePrice);
    childTicketsInput?.addEventListener('input', updatePrice);
    mealPlanSelect?.addEventListener('change', updatePrice);
    carRentalDaysInput?.addEventListener('input', updatePrice);
    pickupSelect?.addEventListener('change', updatePrice);
    dropoffSelect?.addEventListener('change', updatePrice);

    updatePrice();
});
