document.addEventListener("DOMContentLoaded", () => {
    loadJobs();
});

function loadJobs() {
    fetch('jobs.json')
        .then(response => response.json())
        .then(data => {
            const categories = ['latest_jobs', 'results', 'admit_card', 'answer_key', 'syllabus', 'current_affairs'];
            
            // clear existing list
            categories.forEach(cat => {
                const el = document.getElementById(cat);
                if(el) el.innerHTML = '';
            });

            // render json items
            data.jobs.forEach(item => {
                const targetList = document.getElementById(item.category);
                if (targetList) {
                    const li = document.createElement('li');
                    li.className = 'job-item';
                    li.innerHTML = `<a href="${item.link}" target="_blank">${item.title}</a>`;
                    targetList.appendChild(li);
                }
            });
        })
        .catch(error => console.error('Error loading jobs:', error));
}

function searchJobs() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let items = document.getElementsByClassName('job-item');

    for (let i = 0; i < items.length; i++) {
        let text = items[i].innerText.toLowerCase();
        items[i].style.display = text.includes(input) ? "" : "none";
    }
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.setAttribute('data-theme', newTheme);
    document.getElementById('themeToggle').innerText = newTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
}
