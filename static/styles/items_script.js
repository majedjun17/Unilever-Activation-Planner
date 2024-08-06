document.addEventListener("DOMContentLoaded", () => {
    selectedSubcards = new Set();
});


function hideCards() {
    const container = document.getElementById('card-container');
    const button = document.getElementById('toggle-button');
    container.style.display = 'none';
    button.style.display = 'block';
    document.getElementById('submit-button').style.display = 'block';
    document.getElementById('cardForm').style.display = 'block';

}

function toggleCards() {

    const container = document.getElementById('card-container');
    const button = document.getElementById('toggle-button');
    const subcardContainer = document.getElementById('subcard-container');
    if (container.style.display === 'none') {
        container.style.display = 'flex';
        button.style.display = 'none';
        subcardContainer.style.display = 'none';
        document.getElementById('submit-button').style.display = 'none';
        document.getElementById('cardForm').style.display = 'none';
    } else {
        container.style.display = 'none';
        button.style.display = 'block';
    }
}

function fetchSubcards(item) {
    hideCards();
    fetch('/get_cards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selection: item })
        })
        .then(response => response.json())
        .then(data => {
            const subcardContainer = document.getElementById('subcard-container');
            subcardContainer.style.display = 'flex';
            subcardContainer.innerHTML = ''; // Clear previous subcards
            data.forEach(subitem => {
                const subcard = document.createElement('div');
                subcard.className = 'subcard';
                subcard.id = subitem.name;
                subcard.innerText = subitem.name;
                subcard.title = subitem.tooltip; // Set the tooltip
                subcard.onclick = () => toggleSubcard(subitem.name);
                subcardContainer.appendChild(subcard);
                if (selectedSubcards.has(subitem.name)) {
                    subcard.classList.add('selected');
                }
            });
        });
}

function toggleSubcard(subitem) {
    const subcard = document.getElementById(subitem);
    if (selectedSubcards.has(subitem)) {
        selectedSubcards.delete(subitem);
        subcard.classList.remove('selected');
    } else {
        selectedSubcards.add(subitem);
        subcard.classList.add('selected');
    }
    document.getElementById('selectedCards').value = Array.from(selectedSubcards).join(',');
}


function submitSelected() {
    // Collect the selected subcards and send them to another route
    const selectedArray = Array.from(selectedSubcards);
    console.log('Selected subcards:', selectedArray);
    // Send selectedArray to another route
}