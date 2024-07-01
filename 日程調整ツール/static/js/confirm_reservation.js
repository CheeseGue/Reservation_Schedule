document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const startTimes = JSON.parse(decodeURIComponent(urlParams.get('start_times')));
    const endTimes = JSON.parse(decodeURIComponent(urlParams.get('end_times')));
    const reservationDetails = document.getElementById('reservation-details');

    startTimes.forEach((startTime, index) => {
        const endTime = endTimes[index];
        const start = new Date(startTime);
        const end = new Date(endTime);
        const div = document.createElement('div');
        div.textContent = `開始時間: ${start.toLocaleString()} - 終了時間: ${end.toLocaleString()}`;
        reservationDetails.appendChild(div);
    });

    const confirmButton = document.getElementById('confirm-button');
    confirmButton.addEventListener('click', sendReservation);
});

function sendReservation() {
    const urlParams = new URLSearchParams(window.location.search);
    const startTimes = JSON.parse(decodeURIComponent(urlParams.get('start_times')));
    const endTimes = JSON.parse(decodeURIComponent(urlParams.get('end_times')));
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const memo = document.getElementById('memo').value;

    fetch('/send_reservation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start_times: startTimes,
            end_times: endTimes,
            name: name,
            email: email,
            memo: memo
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('予約が確定しました。');
        } else {
            alert('予約に失敗しました。再度お試しください。');
        }
    });
}
