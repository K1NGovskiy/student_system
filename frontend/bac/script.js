
// API_URL - адрес backend
const API_URL = 'http://localhost:8000';

// Функция для загрузки данных с сервера
async function loadData(endpoint) {
    let url = API_URL + endpoint;
    
    // Добавляем параметры фильтрации для разных страниц
    if (window.location.href.includes('students')) {
        const groupFilter = document.getElementById('groupFilter');
        if (groupFilter && groupFilter.value) {
            url += `?group_name=${encodeURIComponent(groupFilter.value)}`;
        }
    } else if (window.location.href.includes('grades')) {
        const courseFilter = document.getElementById('courseFilter');
        const studentFilter = document.getElementById('studentFilter');
        const params = new URLSearchParams();
        if (courseFilter && courseFilter.value) {
            params.append('course_name', courseFilter.value);
        }
        if (studentFilter && studentFilter.value) {
            params.append('student_name', studentFilter.value);
        }
        if (params.toString()) {
            url += '?' + params.toString();
        }
    }
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Ответ сервера не OK: ' + response.status);
        const data = await response.json();
        console.log('Данные от API:', data);
        renderTable(data);
    } catch (error) {
        console.error('Ошибка:', error);
        renderTable([]);
    }
}

// Функция для отрисовки таблицы
function renderTable(data) {
    const tableBody = document.getElementById('dataTable');
    tableBody.innerHTML = '';
    
    if (!data || data.length === 0) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = 4;
        cell.textContent = 'Нет данных';
        cell.className = 'text-center';
        row.appendChild(cell);
        tableBody.appendChild(row);
        return;
    }
    
    data.forEach(item => {
        const row = document.createElement('tr');
        let columns = [];
        
        if (window.location.href.includes('students')) {
            columns = [item._id, item.full_name, item.group_name];
        } else if (window.location.href.includes('courses')) {
            columns = [item._id, item.name, item.teacher_name];
        } else if (window.location.href.includes('grades')) {
            columns = [item._id, item.student_name, item.course_name, item.grade];
        } else if (window.location.href.includes('summary')) {
            columns = [item.student_name, item.course_name, item.teacher_name, item.grade];
        } else if (window.location.href.includes('average')) {
            // Для страницы average используем специализированную функцию
            loadAverageData();
            return;
        }
        
        columns.forEach(col => {
            const cell = document.createElement('td');
            cell.textContent = col !== undefined && col !== null ? col : 'N/A';
            row.appendChild(cell);
        });
        tableBody.appendChild(row);
    });
}

// Специальная функция для страницы среднего балла (для обратной совместимости)
async function loadAverageData() {
    try {
        const response = await fetch(API_URL + '/average/');
        if (!response.ok) throw new Error('Ошибка сервера');
        const data = await response.json();
        
        const tableBody = document.getElementById('dataTable');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        if (!data || data.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 2;
            cell.textContent = 'Нет данных о средних баллах';
            cell.className = 'text-center';
            row.appendChild(cell);
            tableBody.appendChild(row);
            return;
        }
        
        data.forEach(item => {
            const row = document.createElement('tr');
            
            // Группа
            const groupCell = document.createElement('td');
            groupCell.textContent = item.group_name || 'Неизвестная группа';
            
            // Средний балл
            const avgCell = document.createElement('td');
            if (item.avg_grade !== undefined && item.avg_grade !== null) {
                avgCell.textContent = Number(item.avg_grade).toFixed(2);
            } else {
                avgCell.textContent = 'Нет данных';
            }
            
            row.appendChild(groupCell);
            row.appendChild(avgCell);
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Ошибка загрузки среднего балла:', error);
        const tableBody = document.getElementById('dataTable');
        if (tableBody) {
            tableBody.innerHTML = '';
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 2;
            cell.textContent = 'Ошибка загрузки данных';
            cell.className = 'text-center text-danger';
            row.appendChild(cell);
            tableBody.appendChild(row);
        }
    }
}
