let currentDate = new Date();

function formatDate(date) {
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

function loadCalendar() {
    const startDate = new Date(currentDate);
    const endDate = new Date(currentDate);
    endDate.setDate(endDate.getDate() + 6);
    
    fetch('/get_free_busy_times', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start_date: startDate.toISOString(),
            end_date: endDate.toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        renderCalendar(startDate, data);
    });
}

function renderCalendar(startDate, busyTimes) {
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = '';
    
    const days = ['Time'];
    for (let i = 0; i < 7; i++) {
        const currentDate = new Date(startDate);
        currentDate.setDate(currentDate.getDate() + i);
        const formattedDate = `${currentDate.getMonth() + 1}/${currentDate.getDate()}(${['日', '月', '火', '水', '木', '金', '土'][currentDate.getDay()]})`;
        days.push(formattedDate);
    }
    
    for (let i = 0; i < days.length; i++) {
        const div = document.createElement('div');
        div.textContent = days[i];
        calendar.appendChild(div);
    }
    
    for (let i = 0; i < 48; i++) {
        const timeSlot = document.createElement('div');
        timeSlot.className = 'time-slot';
        timeSlot.textContent = `${String(i / 2 | 0).padStart(2, '0')}:${i % 2 === 0 ? '00' : '30'}`;
        calendar.appendChild(timeSlot);
        
        for (let d = 0; d < 7; d++) {
            const currentDate = new Date(startDate);
            currentDate.setDate(currentDate.getDate() + d);
            const startTime = new Date(currentDate);
            startTime.setHours(i / 2 | 0, i % 2 === 0 ? 0 : 30, 0, 0);
            const endTime = new Date(startTime);
            endTime.setMinutes(endTime.getMinutes() + 30);

            const isBusy = busyTimes.some(busy => {
                const busyStart = new Date(busy[0]);
                const busyEnd = new Date(busy[1]);
                return startTime < busyEnd && endTime > busyStart;
            });
            
            const slot = document.createElement('div');
            slot.className = isBusy ? 'busy' : 'free';
            slot.dataset.startTime = startTime.toISOString();
            slot.dataset.endTime = endTime.toISOString();
            if (!isBusy) {
                slot.onclick = () => selectSlot(slot);
            }
            calendar.appendChild(slot);
        }
    }
}

function selectSlot(slot) {
    const selected = document.querySelector('.selected');
    if (selected) {
        selected.classList.remove('selected');
        selected.classList.add('free');
    }
    slot.classList.remove('free');
    slot.classList.add('selected');
}

function confirmReservation() {
    const selectedSlot = document.querySelector('.selected');
    if (selectedSlot) {
        const startTime = selectedSlot.dataset.startTime;
        const endTime = selectedSlot.dataset.endTime;
        const reservationUrl = `/confirm_reservation.html?start_times=${encodeURIComponent(JSON.stringify([startTime]))}&end_times=${encodeURIComponent(JSON.stringify([endTime]))}`;
        window.location.href = reservationUrl;
    } else {
        alert('時間を選択してください。');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadCalendar();
});

function changeWeek(direction) {
    currentDate.setDate(currentDate.getDate() + direction * 7);
    loadCalendar();
}