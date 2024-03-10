// Function to parse CSV data
function parseCSV(csv) {
    const lines = csv.split("\n");

    // Check if there is at least one line in the CSV
    if (lines.length < 2) {
        return null; // Return null if there is no data
    }

    const lastLine = lines[lines.length - 2]; // Get the last line (skip the empty line at the end)
    const lastLineData = lastLine.split(",");

    const timestamp = lastLineData[0];
    const personCount = parseInt(lastLineData[1]);

    return { timestamp, personCount };
}

// Function to create and display the element
function createElement(last_data) {
    // Get the existing element or null if it doesn't exist
    const titleElement = document.getElementById('personCountTitle');

    if (titleElement) {
        // If the element already exists, update its content
        titleElement.textContent = `Date: ${last_data.timestamp}, PersonCount: ${last_data.personCount}`;
    } else {
        // If the element doesn't exist, create a new one
        const newTitleElement = document.createElement('h2');
        newTitleElement.textContent = `Date: ${last_data.timestamp}, PersonCount: ${last_data.personCount}`;
        newTitleElement.style.textAlign = 'center';
        newTitleElement.id = 'personCountTitle'; // Assign an ID to facilitate identification

        // Get the main container (may vary depending on your HTML structure)
        const containerElement = document.body;

        // Add the new element to the main container
        containerElement.appendChild(newTitleElement);
    }
}

// Function to parse timestamps in the format "YYYY-MM-DD HH:mm:ss"
function parseTimestamp(timestampStr) {
    if (timestampStr.trim() === '') {
        return null; // Return null for empty timestamps
    }
    const [fechaStr, horaStr] = timestampStr.split(' ');
    const [anio, mes, dia] = fechaStr.split('-').map(Number);
    const [horas, minutos, segundos] = horaStr.split(':').map(Number);
    return new Date(anio, mes - 1, dia, horas, minutos, segundos);
}

// Function to fetch new data and reload the chart
function fetchDataAndReloadChart() {
    // Get and process the CSV file
    fetch('database/data.csv')
        .then(response => response.text())
        .then(csv => {
            const last_data = parseCSV(csv);

            // Display the last date and PersonCount in the console
            console.log('Date:', last_data.timestamp);
            console.log('PersonCount:', last_data.personCount);

            // Create and display the chart
            createElement(last_data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to reload the image every second
function reloadImage() {
    const elementoImagen = document.getElementById('reloadImage');

    // Function to add a timestamp or random parameter to the image URL
    function addTimestampToUrl(url) {
        const timestamp = new Date().getTime(); // Get current timestamp
        return url + '?' + timestamp;
    }

    // Use setInterval to reload the image every second
    setInterval(function () {
        elementoImagen.src = addTimestampToUrl(elementoImagen.src);
        fetchDataAndReloadChart();
    }, 5000); // 5000 milliseconds = 5 seconds
}

// Call the reloadImage function to start reloading the image
reloadImage();
