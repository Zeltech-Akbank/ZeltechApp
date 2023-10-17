
$(document).on('click', '.duzenle', function() {
    let id = $(this).data('id');
    let teyit = $(`.teyit[data-id="${id}"]`).is(':checked') ? 'Evet' : 'Hayır';
    let karsilandi = $(`.karsilandi[data-id="${id}"]`).is(':checked') ? 'Evet' : 'Hayır';

    $.ajax({
        url: `/duzenle/${id}`,
        method: 'POST',
        data: {
            teyit: teyit,
            karsilandi: karsilandi
        },
        success: function(response) {
            if (response.status === 'success') {
                alert('Değişiklikler başarıyla kaydedildi!');
            } else {
                alert('Bir hata oluştu.');
            }
        }
    });
});

function filtreUygula() {
    var teyitEvet = $("#filterTeyitEvet").is(':checked');
    var karsilandiEvet = $("#filterKarsilandiEvet").is(':checked');

    var searchValue = $("#searchInput").val().toLowerCase();

    $("tbody tr").each(function() {
        var currentRow = $(this);
        var teyitValue = currentRow.find('.teyit').val();
        var karsilandiValue = currentRow.find('.karsilandi').val();

        var showRow = true;

        if (searchValue && !currentRow.text().toLowerCase().includes(searchValue)) {
            showRow = false;
        }

        if (teyitEvet && teyitValue !== 'Evet') {
            showRow = false;
        }

        if (karsilandiEvet && karsilandiValue !== 'Evet') {
            showRow = false;
        }

        if (showRow) {
            currentRow.show();
        } else {
            currentRow.hide();
        }
    });
}

$("#searchInput").on("keyup", filtreUygula);  // Arama için keyup olayını dinle
