function masquerTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'none';
}

function afficherTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'table';
}

function toggleTable(idTableau, idArrow) {
    var tableau = document.getElementById(idTableau);
    if (tableau.style.display === 'none') {
        afficherTableau(idTableau);
    } else {
        masquerTableau(idTableau);
    }
    
    toggleArrow(idArrow);
}

function toggleArrow(idArrow) {
    var arrow = document.getElementById(idArrow);
    arrow.textContent = arrow.textContent.includes('⬇️') ? arrow.textContent.replace('⬇️', '⬆️') : arrow.textContent.replace('⬆️', '⬇️');
}

document.getElementById('facile-arrow').addEventListener('click', function() {
    toggleTable('table_facile', 'facile-arrow');
});

document.getElementById('moyen-arrow').addEventListener('click', function() {
    toggleTable('table_moyen', 'moyen-arrow');
});

document.getElementById('difficile-arrow').addEventListener('click', function() {
    toggleTable('table_difficile', 'difficile-arrow');
});
