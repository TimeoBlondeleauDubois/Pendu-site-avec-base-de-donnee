
function masquerTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'none';
}

function afficherTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'table';
}

document.querySelector('.table-section:nth-child(1) .title-container2').addEventListener('click', function() {
    var tableauFacile = document.getElementById('table_facile');
    if (tableauFacile.style.display === 'none') {
        afficherTableau('table_facile');
    } else {
        masquerTableau('table_facile');
    }
});

document.querySelector('.table-section:nth-child(2) .title-container2').addEventListener('click', function() {
    var tableauMoyen = document.getElementById('table_moyen');
    if (tableauMoyen.style.display === 'none') {
        afficherTableau('table_moyen');
    } else {
        masquerTableau('table_moyen');
    }
});

document.querySelector('.table-section:nth-child(3) .title-container2').addEventListener('click', function() {
    var tableauDifficile = document.getElementById('table_difficile');
    if (tableauDifficile.style.display === 'none') {
        afficherTableau('table_difficile');
    } else {
        masquerTableau('table_difficile');
    }
});

// Détecter le clic sur le titre "Facile" et basculer la direction de la flèche
document.getElementById('facile-arrow').addEventListener('click', function() {
    var arrow = document.getElementById(facile-arrow);
    arrow.textContent = arrow.textContent === 'Facile: ⬇️' ? 'Facile:⬆️' : 'Facile:⬇️';
});

// Détecter le clic sur le titre "Moyen" et basculer la direction de la flèche
document.getElementById('moyen-arrow').addEventListener('click', function() {
    var arrow = document.getElementById(moyen-arrow);
    arrow.textContent = arrow.textContent === 'Moyen: ⬇️' ? 'Moyen:⬆️' : 'Moyen:⬇️';
});

// Détecter le clic sur le titre "Difficile" et basculer la direction de la flèche
document.getElementById('difficile-arrow').addEventListener('click', function() {
    var arrow = document.getElementById(difficile-arrow);
    arrow.textContent = arrow.textContent === 'Difficile: ⬇️' ? 'Difficile:⬆️' : 'Difficile:⬇️';
});
