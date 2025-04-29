// Get elements
const body = document.body;
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-menu a');
const searchIcon = document.querySelector('.search-icon');
const searchContainer = document.querySelector('.modal-search-container');
const closeButton = document.querySelector('.search-modal-close');

// Toggles hamburger menu
function toggleMenu() {
    const isOpening = !hamburger.classList.contains('active');
    navMenu.classList.toggle('visible');
    hamburger.classList.toggle('active');
    body.classList.toggle('no-scroll');

    updateSearchIconVisibility(); // Ensure correct visibility based on state
}

// Closes hamburger menu
function closeMenu() {
    navMenu.classList.remove('visible');
    hamburger.classList.remove('active');
    body.classList.remove('no-scroll');

    updateSearchIconVisibility();
}

// Opens search modal
function openSearchModal() {
    searchContainer.classList.add('visible');
    document.documentElement.classList.add('no-scroll');
    body.classList.add('no-scroll');

    updateSearchIconVisibility();
}

// Closes search modal
function closeSearchModal() {
    searchContainer.classList.remove('visible');
    document.documentElement.classList.remove('no-scroll');
    body.classList.remove('no-scroll');

    updateSearchIconVisibility();
}

// Updates search icon visibility based on UI state
function updateSearchIconVisibility() {
    const isMenuOpen = hamburger.classList.contains('active');
    const isSearchOpen = searchContainer.classList.contains('visible');

    if (!isMenuOpen && !isSearchOpen) {
        searchIcon.classList.remove('hidden');
    } else {
        searchIcon.classList.add('hidden');
    }
}

// Event listeners
hamburger.addEventListener('click', toggleMenu);
navLinks.forEach(link => link.addEventListener('click', closeMenu));
searchIcon.addEventListener('click', openSearchModal);
closeButton.addEventListener('click', closeSearchModal);

// ESC key closes both
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeMenu();
        closeSearchModal();
    }
});

// Click outside nav closes hamburger menu
document.addEventListener('click', (event) => {
    if (!navMenu.contains(event.target) && !hamburger.contains(event.target)) {
        closeMenu();
    }

    // Close search modal if background clicked
    if (event.target === searchContainer) {
        closeSearchModal();
    }
});



































// ### search form handling ### // ----------------------------------------

//1. Populate locations -----------------------------------------
const continentSelect = document.getElementById('id_continent');
    const countrySelect = document.getElementById('id_country');
    const citySelect = document.getElementById('id_city');

    function populateSelect(selectEl, items, label) {
        selectEl.innerHTML = `<option value="">${label}</option>`;
        items.forEach(item => {
            selectEl.innerHTML += `<option value="${item.id}">${item.name}</option>`;
        });
    }

    // Handle Continent change
    continentSelect.addEventListener('change', () => {
        const contId = parseInt(continentSelect.value);

        // If a continent is selected, filter countries by continent
        const filteredCountries = contId ? COUNTRIES.filter(c => c.continent_id === contId) : COUNTRIES;
        populateSelect(countrySelect, filteredCountries, 'Country');

        // Filter cities based on selected continent (if any)
        const filteredCities = contId ? CITIES.filter(city => city.continent_id === contId) : CITIES;
        populateSelect(citySelect, filteredCities, 'City');
    });

    // Handle Country change
    countrySelect.addEventListener('change', () => {
        const countryId = parseInt(countrySelect.value);
        const country = COUNTRIES.find(c => c.id === countryId);

        if (country) {
            // Auto-set continent based on country selection
            continentSelect.value = country.continent_id;

            // Filter cities based on selected country
            const filteredCities = CITIES.filter(city => city.country_id === countryId);
            populateSelect(citySelect, filteredCities, 'City');
        } else {
            // If no country is selected, reset cities to match selected continent or all
            const contId = parseInt(continentSelect.value);
            const filteredCities = contId ? CITIES.filter(city => city.continent_id === contId) : CITIES;
            populateSelect(citySelect, filteredCities, 'City');
        }
    });

    // Handle City change
    citySelect.addEventListener('change', () => {
        const cityId = parseInt(citySelect.value);
        const city = CITIES.find(c => c.id === cityId);

        if (city) {
            // Auto-set country and continent based on selected city
            countrySelect.value = city.country_id;
            continentSelect.value = city.continent_id;
        }
    });

    // Initial load (ensure cities are populated based on the selected continent or country)
    document.addEventListener('DOMContentLoaded', () => {
        const initialContinent = continentSelect.value;
        const initialCountry = countrySelect.value;

        if (initialContinent) {
            continentSelect.dispatchEvent(new Event('change'));
        }

        if (initialCountry) {
            countrySelect.dispatchEvent(new Event('change'));
        }
    });
//
//
//

//2. select dates (departure date not greater than return date or before tomorrow) ------------
document.addEventListener("DOMContentLoaded", function () {
    const depInput = document.getElementById("id_departure_date");
    const retInput = document.getElementById("id_return_date");

    function updateMinReturn() {
        if (depInput.value) {
            retInput.min = depInput.value;
        }
    }

    function updateMaxDeparture() {
        // Set the departure date's max equal to the return date's value
        if (retInput.value) {
            depInput.max = retInput.value;
        }
    }

    function enforceDateOrder() {
        // If the departure date is later than the return date, reset the departure date
        if (depInput.value && retInput.value && depInput.value > retInput.value) {
            alert("Departure date must be before return date!");
            depInput.value = ""; // Reset departure date or choose to handle differently
        } 
    }

    // Initial sync on load
    updateMinReturn();
    updateMaxDeparture();

    // Sync on change
    depInput.addEventListener("change", () => {
        updateMinReturn();
        enforceDateOrder();
    });

    retInput.addEventListener("change", () => {
        updateMaxDeparture();
        enforceDateOrder();
    });
});
//
//
//

//3. wants flight, set budget but no from_airport ------------------------------
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#modal-search-form');
    const wantsFlightSelect = document.querySelector('select[name="wants_flight"]');  // Change from radios to select
    const budgetInput = document.querySelector('input[name="budget"]');
    const airportSelect = document.querySelector('select[name="from_airport"]');
    const modalErrorMessage = document.getElementById('modal-error-message');

    form.addEventListener('submit', (event) => {
        let wantsFlight = wantsFlightSelect.value;  // Get the value from the select dropdown
        let budget = budgetInput.value;
        let airportSelected = airportSelect.value;

        // Clear any previous error messages
        modalErrorMessage.style.display = 'none';
        modalErrorMessage.textContent = '';

        // Check if wants_flight is 'yes', a budget is set, and no airport is selected
        if (wantsFlight === 'yes' && budget && !airportSelected) {
            // Prevent form submission
            event.preventDefault();
            // Show error message
            modalErrorMessage.textContent = 'Please select a departure airport to calculate accurate flight costs for your budget.';
            modalErrorMessage.style.display = 'block';
        }
    });
});



// III.
    //////////////
   //   Back   //
  //  Button  //
 //          //
//////////////   

function handleBack() {
    // If there's browser history, go back
    if (window.history.length > 1) {
        window.history.back();
    } else {
        // Otherwise, redirect to home or another default page
        window.location.href = '/';
    }
}     // --->    <button onclick="handleBack()">← Back</button>















