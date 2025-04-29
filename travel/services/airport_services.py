def calculate_plane_ticket_cost(standard_ticket_price, from_country, from_continent, to_country, to_continent):
    price_outside_country = 0.30   # 30% more
    price_outside_continent = 0.50 # 50% more

    is_same_continent = from_continent == to_continent
    is_same_country = from_country == to_country

    if is_same_continent and not is_same_country:
        return standard_ticket_price + (price_outside_country * standard_ticket_price)
    elif not is_same_continent:
        return standard_ticket_price + (price_outside_continent * standard_ticket_price)

    return standard_ticket_price