document.querySelectorAll('.yardim-tipi').forEach(select => {
    select.addEventListener('change', function() {
        const bedenSelect = this.parentNode.querySelector('.beden');
        if (['Erkek Giysi', 'Erkek İç Çamaşır', 'Kadın Giysi', 'Kadın İç Çamaşır', 'Çocuk Giysisi', 'Çocuk İç Çamaşır'].includes(this.value)) {
            bedenSelect.classList.remove('d-none');

            const isChildClothing = this.value === 'Çocuk Giysisi' || this.value === 'Çocuk İç Çamaşır';
            bedenSelect.querySelectorAll('.erkek-kadin').forEach(opt => opt.classList.toggle('d-none', isChildClothing));
            bedenSelect.querySelectorAll('.cocuk').forEach(opt => opt.classList.toggle('d-none', !isChildClothing));

            // İlk uygun seçeneği otomatik olarak seç
            bedenSelect.value = bedenSelect.querySelector('option:not(.d-none)').value;
        } else {
            bedenSelect.classList.add('d-none');
        }
    });
});

document.getElementById('add-yardim').addEventListener('click', function() {
    const yardimRow = document.createElement('div');
    yardimRow.className = 'yardim-row mb-3 d-flex align-items-center';

    // Create the "yardim-tipi" dropdown
    const yardimTipi = document.createElement('select');
    yardimTipi.className = 'form-control yardim-tipi mr-2';
    yardimTipi.name = 'yardim-tipi[]';
    yardimTipi.required = true;
    [
        'Çadır', 'Battaniye', 'Yorgan', 'Su', 'Jeneratör',
        'Erkek Giysi', 'Erkek İç Çamaşır', 'Kadın Giysi',
        'Kadın İç Çamaşır', 'Çocuk Giysisi', 'Çocuk İç Çamaşır'
    ].forEach(optionText => {
        const option = document.createElement('option');
        option.value = optionText;
        option.textContent = optionText;
        yardimTipi.appendChild(option);
    });

    // Create the "yardim-miktar" input
    const yardimMiktar = document.createElement('input');
    yardimMiktar.type = 'number';
    yardimMiktar.className = 'form-control yardim-miktar mr-2';
    yardimMiktar.name = 'yardim-miktar[]';
    yardimMiktar.required = true;
    yardimMiktar.placeholder = 'Miktar';
    yardimMiktar.min = '1';

    // Create the "beden" dropdown
    const beden = document.createElement('select');
    beden.className = 'form-control beden mr-2 d-none'; // Start with d-none to hide it initially
    beden.name = 'beden[]';

    const erkekKadinBedenleri = ['S', 'M', 'L', 'XL'];
    const cocukBedenleri = ['1-3 Ay', '3-6 Ay', '6-9 Ay', '1-3 Yaş', '3-6 Yaş', '6-9 Yaş', '9 - 12 Yaş', '13 Yaş'];

    erkekKadinBedenleri.forEach(optionText => {
        const option = document.createElement('option');
        option.value = optionText;
        option.textContent = optionText;
        option.className = 'erkek-kadin';
        beden.appendChild(option);
    });

    cocukBedenleri.forEach(optionText => {
        const option = document.createElement('option');
        option.value = optionText;
        option.textContent = optionText;
        option.className = 'cocuk d-none';
        beden.appendChild(option);
    });

    // Adjust 'beden' options based on the initial 'yardim-tipi' selection
    adjustBedenOptions(yardimTipi, beden);

    yardimTipi.addEventListener('change', function() {
        adjustBedenOptions(yardimTipi, beden);
    });

    // Create the "Sil" button
    const removeBtn = document.createElement('button');
    removeBtn.className = 'btn btn-danger remove-yardim';
    removeBtn.textContent = 'Sil';
    removeBtn.type = 'button';
    removeBtn.addEventListener('click', function() {
        yardimRow.remove();
    });

    yardimRow.appendChild(yardimTipi);
    yardimRow.appendChild(yardimMiktar);
    yardimRow.appendChild(beden);
    yardimRow.appendChild(removeBtn);

    document.getElementById('yardimlar').appendChild(yardimRow);
});

function adjustBedenOptions(yardimTipiElement, bedenElement) {
    if (['Erkek Giysi', 'Erkek İç Çamaşır', 'Kadın Giysi', 'Kadın İç Çamaşır'].includes(yardimTipiElement.value)) {
        bedenElement.classList.remove('d-none');
        bedenElement.querySelectorAll('option').forEach(o => o.classList.add('d-none'));
        bedenElement.querySelectorAll('.erkek-kadin').forEach(o => o.classList.remove('d-none'));
        bedenElement.value = 'S'; // Varsayılan beden değeri 'S' olarak belirlenir.
    } else if (['Çocuk Giysisi', 'Çocuk İç Çamaşır'].includes(yardimTipiElement.value)) {
        bedenElement.classList.remove('d-none');
        bedenElement.querySelectorAll('option').forEach(o => o.classList.add('d-none'));
        bedenElement.querySelectorAll('.cocuk').forEach(o => o.classList.remove('d-none'));
        bedenElement.value = bedenElement.querySelector('.cocuk:not(.d-none)').value; // Çocuk bedenleri için varsayılan değeri ayarla
    } else {
        bedenElement.classList.add('d-none');
    }
}