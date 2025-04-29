# Service for Travel Agency ✅❌⏳✏️

## Brief Description of the System
As part of the project, create a system that allows users to search for trips by given criteria and purchase them.

## Main System Functions
- ⏳ **Main Page**
- ✅ **Configuring the Trip Offer (Administrator)**
- ✅ **Searching for Trips by Given Criteria**
- ✅ **"Purchase" of the Trip** – Calculate amount to pay based on the number of people 
- **(Optional) Additional Services**: ✅ Car rental, ❌optional trips
- ❌ **(Optional) Configuration of Passport and Visa Restrictions**

## Technologies
- ✅ Django
- ❌ **(Optional)** Frontend in Angular and Django REST Framework

## Basic Entities (Proposal)
- **Continent**
  - ✅ name
- **Country**
  - ✅ name
  - ✅ belonging to the continent (foreign key)
- **City**
  - ✅ name
  - ✅ belonging to the country (foreign key)
- **Hotel**
  - ✅ name
  - ✅ standard (stars)
  - ✅ description
  - ✅ belonging to the city (foreign key)
- **Airport**
  - ✅ name
  - ✅ belonging to the city (foreign key)
- **Trip**
  - ✅ where from (City, Airport)
  - ✅ where to (City, Hotel, Airport)
  - ✅ departure date
  - ✅ return date
  - ✅ length of stay
  - ✅ type: (BB – bed & breakfast, HB – half board, FB – full board, AI – all inclusive)
  - ✅ price for an adult
  - ✅ price for a child
  - ✅ promoted
  - ✅ number of places for adults 
  - ✅ number of places for children
  - ✏️ number of places for adults and children are set in booking model trip has tickets for both, clean method insures per trip 1 adult exists
- **Purchase of a Trip**
  - ✅ trip
  - ✅ participant details
  - ✅ amount

## Functionalities ✅❌⏳✏️
- **Home Page**
  - ✅ Presentation of promoted trips
  - ⏳ Presentation of upcoming trips (globally)
  - ⏳ Presentation of upcoming trips (by continents)
  - ⏳ Presentation of upcoming trips (by country)
  - ⏳ Presentation of recently purchased trips
  - ⏳ **(Optional)** Presentation of trips with a reduced price (mechanism should be added)
  - ⏳ **(Optional)** Presentation of trips with only 1 or 2 places left
  - Each of the following lists should present, for example, 3 entries + link to 'see more' directing to search results according to a given criterion (e.g., clicking the Tenerife link should redirect to the page with results of searching trips to Tenerife)
  - Continent, country, city, hotel should be clickable and lead to search results
  - After clicking on a specific tour, detailed information is presented
  - **(Optional)** Below the trip, present trips to the same place, but with a later date
  - **(Optional)** Below the trip, present trips to other hotels from this city
  - **(Optional)** Below the trip, present trips to other cities from this country

- **Setting up a Tour Offer**
  - The administrator (on a separate page) can add and edit tours
  - The form should make it possible to enter all the parameters of the trip
  - You must pre-configure the database of continents, countries, cities, airports, and hotels
  - **(Optional)** Separate sites for managing continents, countries, cities, airports, and hotels

- **Searching for Trips by Given Criteria**
  - All clickable elements (continents, countries, cities, hotels) direct to search results page
  - In addition, the page has a form for filtering and sorting results
  - You can search for trips by:
    - City (airport) of departure
    - City (hotel) of stay
    - Departure date (optional range)
    - Return date (optional range)
    - Type (BB, HB, FB, AI)
    - Hotel standard
    - Number of days
  - You can sort by:
    - Price
    - Departure date
  - **(Optional)** As the number of trips increases, you can implement paging search results

- **Purchase of a Trip**
  - After choosing a specific trip, you can purchase it
  - Specify the number of adults and children
  - If there are enough places available, the trip will be “purchased”
  - The number of free places will be reduced
  - The price for a trip will be calculated (based on the number of people)
  - Purchased trips are presented on the administrative page/pages
  - **(Optional)** You can group these trips accordingly and add a simple search engine

## Additional Requirements
- It is necessary to ensure an aesthetic and functional way of presenting data
- Data collected from users should be pre-validated