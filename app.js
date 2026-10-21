/* ═══════════════════════════════════════
   FITSPHERE — app.js
   Full interactive logic
═══════════════════════════════════════ */

// ── Navigation ──────────────────────────────────────────────
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const pageTitle = document.getElementById('page-title');

const pageTitles = {
  dashboard: 'Dashboard',
  membership: 'Membership',
  attendance: 'Attendance',
  workouts: 'AI Workouts',
  progress: 'Body Progress',
  diet: 'Diet Tracker',
  heatmap: 'Performance',
  trainers: 'Trainers',
  schedule: 'Scheduler',
  revenue: 'Revenue',
  reminders: 'Reminders',
};

function navigateTo(page) {
  pages.forEach(p => p.classList.remove('active'));
  navItems.forEach(n => n.classList.remove('active'));
  const targetPage = document.getElementById('page-' + page);
  const targetNav = document.getElementById('nav-' + page);
  if (targetPage) targetPage.classList.add('active');
  if (targetNav) targetNav.classList.add('active');
  pageTitle.textContent = pageTitles[page] || page;
  if (sidebar.classList.contains('open')) sidebar.classList.remove('open');

  // Lazy-init pages on first visit
  if (page === 'membership' && !membersLoaded) renderMembers();
  if (page === 'attendance' && !attendanceLoaded) renderAttendance();
  if (page === 'workouts' && !workoutsLoaded) renderWorkouts();
  if (page === 'progress' && !progressLoaded) renderProgress();
  if (page === 'diet' && !dietLoaded) renderDiet();
  if (page === 'heatmap' && !heatmapLoaded) renderHeatmap();
  if (page === 'trainers' && !trainersLoaded) renderTrainers();
  if (page === 'schedule' && !scheduleLoaded) renderSchedule();
  if (page === 'revenue' && !revenueLoaded) renderRevenue();
  if (page === 'reminders' && !remindersLoaded) renderReminders();
}

navItems.forEach(item => {
  item.addEventListener('click', e => {
    e.preventDefault();
    navigateTo(item.dataset.page);
  });
});

document.querySelectorAll('[data-page]').forEach(el => {
  if (!el.classList.contains('nav-item')) {
    el.addEventListener('click', e => {
      e.preventDefault();
      navigateTo(el.dataset.page);
    });
  }
});

// ── Sidebar Mobile Toggle ────────────────────────────────────
const sidebar = document.getElementById('sidebar');
document.getElementById('menu-toggle').addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

// ── Animated Counters ────────────────────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.target);
  const prefix = el.dataset.prefix || '';
  const duration = 1800;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 4);
    const value = Math.floor(eased * target);
    el.textContent = prefix + value.toLocaleString('en-IN');
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = prefix + target.toLocaleString('en-IN');
  }
  requestAnimationFrame(update);
}

document.querySelectorAll('.stat-num').forEach(el => {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(el);
        observer.disconnect();
      }
    });
  });
  observer.observe(el);
});

// ── Weekly Bar Chart ─────────────────────────────────────────
const weekData = [
  { day: 'Mon', checkins: 185, sessions: 42 },
  { day: 'Tue', checkins: 210, sessions: 55 },
  { day: 'Wed', checkins: 195, sessions: 48 },
  { day: 'Thu', checkins: 230, sessions: 62 },
  { day: 'Fri', checkins: 247, sessions: 56 },
  { day: 'Sat', checkins: 290, sessions: 74 },
  { day: 'Sun', checkins: 160, sessions: 38 },
];

function renderWeeklyChart() {
  const chart = document.getElementById('weekly-chart');
  if (!chart) return;
  const maxVal = Math.max(...weekData.map(d => d.checkins));
  chart.innerHTML = weekData.map(d => {
    const hCheckin = Math.round((d.checkins / maxVal) * 110);
    const hSession = Math.round((d.sessions / maxVal) * 110);
    return `
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;height:140px">
        <div style="flex:1;display:flex;align-items:flex-end;gap:3px;width:100%">
          <div class="bar-col blue-bar" style="height:${hCheckin}px"></div>
          <div class="bar-col cyan-bar" style="height:${hSession}px"></div>
        </div>
        <span class="bar-label">${d.day}</span>
      </div>`;
  }).join('');
}
renderWeeklyChart();

// ── Live Activity Feed ───────────────────────────────────────
const activityEvents = [
  { name: 'Rahul Sharma', action: 'checked in', type: 'green', time: 'Just now' },
  { name: 'Priya Mehta', action: 'completed HIIT session', type: 'blue', time: '2m ago' },
  { name: 'Arjun Patel', action: 'booked trainer session', type: 'orange', time: '5m ago' },
  { name: 'Sneha Kapoor', action: 'logged meal', type: 'green', time: '8m ago' },
  { name: 'Vikram Singh', action: 'renewed membership', type: 'blue', time: '12m ago' },
  { name: 'Riya Bose', action: 'checked out', type: 'red', time: '15m ago' },
  { name: 'Dev Khanna', action: 'started Yoga class', type: 'green', time: '18m ago' },
];

function renderActivityFeed() {
  const feed = document.getElementById('activity-feed');
  if (!feed) return;
  feed.innerHTML = activityEvents.map(ev => `
    <div class="activity-item">
      <div class="activity-dot ${ev.type}"></div>
      <div class="activity-text"><strong>${ev.name}</strong> ${ev.action}</div>
      <div class="activity-time">${ev.time}</div>
    </div>
  `).join('');
}
renderActivityFeed();

// Simulate live updates
let newActivityNames = ['Anjali Roy', 'Mohan Das', 'Kiran Patel', 'Nisha Gupta', 'Suresh Kumar'];
let actIdx = 0;
setInterval(() => {
  const feed = document.getElementById('activity-feed');
  if (!feed || !document.getElementById('page-dashboard').classList.contains('active')) return;
  const actions = ['checked in', 'completed a workout', 'booked a session', 'logged a meal', 'checked out'];
  const types = ['green', 'blue', 'orange', 'green', 'red'];
  const rand = Math.floor(Math.random() * actions.length);
  const newItem = document.createElement('div');
  newItem.className = 'activity-item';
  newItem.innerHTML = `
    <div class="activity-dot ${types[rand]}"></div>
    <div class="activity-text"><strong>${newActivityNames[actIdx % newActivityNames.length]}</strong> ${actions[rand]}</div>
    <div class="activity-time">Just now</div>
  `;
  feed.prepend(newItem);
  actIdx++;
  if (feed.children.length > 10) feed.lastChild.remove();
}, 5000);

// ── Members ──────────────────────────────────────────────────
let membersLoaded = false;
const memberData = [
  { name: 'Rahul Sharma', phone: '+91 98765 43210', plan: 'Elite', status: 'active', goal: 'Muscle Gain', sessions: 42, attendance: 98, joined: 'Jan 2025', avatar: 'R', grad: 'linear-gradient(135deg,#f59e0b,#ef4444)' },
  { name: 'Priya Mehta', phone: '+91 87654 32109', plan: 'Pro', status: 'active', goal: 'Weight Loss', sessions: 38, attendance: 95, joined: 'Mar 2025', avatar: 'P', grad: 'linear-gradient(135deg,#8b5cf6,#3b82f6)' },
  { name: 'Arjun Patel', phone: '+91 76543 21098', plan: 'Elite', status: 'active', goal: 'Endurance', sessions: 35, attendance: 92, joined: 'Feb 2025', avatar: 'A', grad: 'linear-gradient(135deg,#10b981,#06b6d4)' },
  { name: 'Sneha Kapoor', phone: '+91 65432 10987', plan: 'Pro', status: 'active', goal: 'Flexibility', sessions: 33, attendance: 91, joined: 'Apr 2025', avatar: 'S', grad: 'linear-gradient(135deg,#f97316,#eab308)' },
  { name: 'Vikram Singh', phone: '+91 54321 09876', plan: 'Basic', status: 'active', goal: 'General Fitness', sessions: 30, attendance: 89, joined: 'May 2025', avatar: 'V', grad: 'linear-gradient(135deg,#ec4899,#8b5cf6)' },
  { name: 'Riya Bose', phone: '+91 43210 98765', plan: 'Pro', status: 'expired', goal: 'Weight Loss', sessions: 18, attendance: 72, joined: 'Jun 2024', avatar: 'R', grad: 'linear-gradient(135deg,#06b6d4,#3b82f6)' },
  { name: 'Dev Khanna', phone: '+91 32109 87654', plan: 'Basic', status: 'active', goal: 'Muscle Gain', sessions: 26, attendance: 84, joined: 'Aug 2025', avatar: 'D', grad: 'linear-gradient(135deg,#10b981,#34d399)' },
  { name: 'Anjali Roy', phone: '+91 21098 76543', plan: 'Elite', status: 'paused', goal: 'Endurance', sessions: 14, attendance: 60, joined: 'Oct 2024', avatar: 'A', grad: 'linear-gradient(135deg,#ef4444,#f97316)' },
  { name: 'Kiran Sharma', phone: '+91 11098 76543', plan: 'Pro', status: 'active', goal: 'Weight Loss', sessions: 28, attendance: 88, joined: 'Jan 2026', avatar: 'K', grad: 'linear-gradient(135deg,#8b5cf6,#ec4899)' },
];

function renderMembers() {
  membersLoaded = true;
  const grid = document.getElementById('members-grid');
  if (!grid) return;
  grid.innerHTML = memberData.map(m => `
    <div class="member-card">
      <div class="member-card-header">
        <div class="member-avatar" style="background:${m.grad}">${m.avatar}</div>
        <div class="member-card-info">
          <h4>${m.name}</h4>
          <span>${m.phone}</span>
        </div>
        <span class="member-status-badge ${m.status}">${m.status}</span>
      </div>
      <div class="member-card-meta">
        <div class="member-meta-item"><span>Plan</span><strong>${m.plan}</strong></div>
        <div class="member-meta-item"><span>Goal</span><strong>${m.goal}</strong></div>
        <div class="member-meta-item"><span>Sessions</span><strong>${m.sessions}</strong></div>
        <div class="member-meta-item"><span>Since</span><strong>${m.joined}</strong></div>
      </div>
      <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span style="font-size:0.72rem;color:var(--text3)">Attendance</span>
          <span style="font-size:0.72rem;font-weight:700;color:var(--text)">${m.attendance}%</span>
        </div>
        <div class="member-attendance-bar">
          <div class="member-attendance-fill" style="width:${m.attendance}%"></div>
        </div>
      </div>
      <div class="member-card-footer">
        <button class="member-action-btn">📋 Profile</button>
        <button class="member-action-btn">📅 Book</button>
        <button class="member-action-btn primary">💬 Message</button>
      </div>
    </div>
  `).join('');

  // Filter tabs
  document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const f = tab.dataset.filter;
      const cards = grid.querySelectorAll('.member-card');
      cards.forEach((card, i) => {
        const m = memberData[i];
        if (!m) return;
        card.style.display = (f === 'all' || m.status === f) ? '' : 'none';
      });
    });
  });

  // Search
  document.getElementById('member-search').addEventListener('input', e => {
    const q = e.target.value.toLowerCase();
    grid.querySelectorAll('.member-card').forEach((card, i) => {
      const m = memberData[i];
      if (!m) return;
      card.style.display = m.name.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

// Add Member Modal
document.getElementById('add-member-btn').addEventListener('click', () => {
  document.getElementById('add-member-modal').classList.add('open');
});
document.getElementById('close-member-modal').addEventListener('click', () => {
  document.getElementById('add-member-modal').classList.remove('open');
});
document.getElementById('add-member-modal').addEventListener('click', e => {
  if (e.target === e.currentTarget) e.currentTarget.classList.remove('open');
});
document.getElementById('save-member-btn').addEventListener('click', () => {
  const name = document.getElementById('m-name').value.trim();
  if (!name) { alert('Please enter member name'); return; }
  const plan = document.getElementById('m-plan').value;
  const goal = document.getElementById('m-goal').value;
  const letter = name[0].toUpperCase();
  const grads = ['linear-gradient(135deg,#3b82f6,#06b6d4)', 'linear-gradient(135deg,#8b5cf6,#ec4899)', 'linear-gradient(135deg,#10b981,#f59e0b)'];
  memberData.unshift({
    name, phone: document.getElementById('m-phone').value || 'N/A',
    plan: plan.split('—')[0].trim(), status: 'active', goal,
    sessions: 0, attendance: 100, joined: 'Just now', avatar: letter,
    grad: grads[Math.floor(Math.random() * grads.length)]
  });
  membersLoaded = false;
  renderMembers();
  document.getElementById('add-member-modal').classList.remove('open');
  document.getElementById('m-name').value = '';
  document.getElementById('m-phone').value = '';
  document.getElementById('m-email').value = '';
});

// ── Attendance ───────────────────────────────────────────────
let attendanceLoaded = false;
const attendanceLogData = [
  { name: 'Rahul Sharma', type: 'in', time: '6:02 AM', grad: 'linear-gradient(135deg,#f59e0b,#ef4444)', letter: 'R' },
  { name: 'Priya Mehta', type: 'in', time: '6:15 AM', grad: 'linear-gradient(135deg,#8b5cf6,#3b82f6)', letter: 'P' },
  { name: 'Dev Khanna', type: 'out', time: '7:45 AM', grad: 'linear-gradient(135deg,#10b981,#34d399)', letter: 'D' },
  { name: 'Arjun Patel', type: 'in', time: '8:00 AM', grad: 'linear-gradient(135deg,#10b981,#06b6d4)', letter: 'A' },
  { name: 'Sneha Kapoor', type: 'in', time: '8:30 AM', grad: 'linear-gradient(135deg,#f97316,#eab308)', letter: 'S' },
  { name: 'Kiran Sharma', type: 'out', time: '9:15 AM', grad: 'linear-gradient(135deg,#8b5cf6,#ec4899)', letter: 'K' },
  { name: 'Anjali Roy', type: 'in', time: '10:00 AM', grad: 'linear-gradient(135deg,#ef4444,#f97316)', letter: 'A' },
];

function renderAttendance() {
  attendanceLoaded = true;
  const log = document.getElementById('attendance-log');
  if (log) {
    log.innerHTML = attendanceLogData.map(item => `
      <div class="att-log-item">
        <div class="att-log-avatar" style="background:${item.grad}">${item.letter}</div>
        <div class="att-log-info">
          <strong>${item.name}</strong>
          <span>${item.type === 'in' ? '✅ Checked In' : '🏃 Checked Out'}</span>
        </div>
        <span class="att-log-time ${item.type === 'out' ? 'out' : ''}">${item.time}</span>
      </div>
    `).join('');
  }

  const hourlyData = [4, 18, 42, 55, 38, 22, 12, 8, 15, 28, 45, 62, 55, 40, 30, 25, 38, 58, 72, 65, 45, 30, 18, 8];
  const hourlyChart = document.getElementById('hourly-chart');
  if (hourlyChart) {
    const maxH = Math.max(...hourlyData);
    hourlyChart.innerHTML = hourlyData.map((v, i) => {
      const h = Math.round((v / maxH) * 90);
      const hour = i === 0 ? '12a' : i < 12 ? `${i}a` : i === 12 ? '12p' : `${i-12}p`;
      const isPeak = (i >= 6 && i <= 8) || (i >= 18 && i <= 20);
      return `
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:2px">
          <div class="h-bar" data-count="${v}"
            style="height:${h}px;background:${isPeak ? 'linear-gradient(to top,#ef4444,#f97316)' : 'linear-gradient(to top,#3b82f6,#06b6d4)'}"></div>
          ${i % 4 === 0 ? `<span style="font-size:0.6rem;color:var(--text3)">${hour}</span>` : '<span></span>'}
        </div>`;
    }).join('');
  }
}

document.getElementById('checkin-btn').addEventListener('click', () => {
  const names = ['Mohan Das', 'Nisha Gupta', 'Suresh Kumar'];
  const n = names[Math.floor(Math.random() * names.length)];
  attendanceLogData.unshift({ name: n, type: 'in', time: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }), grad: 'linear-gradient(135deg,#3b82f6,#06b6d4)', letter: n[0] });
  renderAttendance();
});

// ── Workouts ─────────────────────────────────────────────────
let workoutsLoaded = false;
const workoutPlans = {
  'Weight Loss': [
    { day: 'Monday', type: 'Cardio + Core', color: '#ef4444', exercises: [
      { icon: '🏃', name: 'Treadmill Run', detail: '30 min @ 7 km/h', sets: 'Cardio' },
      { icon: '💪', name: 'Plank', detail: '3 × 60 sec', sets: '3×60s' },
      { icon: '🔥', name: 'Burpees', detail: '4 × 15 reps', sets: '4×15' },
      { icon: '🧘', name: 'Mountain Climbers', detail: '3 × 20 reps', sets: '3×20' },
    ]},
    { day: 'Tuesday', type: 'Upper Body', color: '#3b82f6', exercises: [
      { icon: '💪', name: 'Push-ups', detail: '4 × 20 reps', sets: '4×20' },
      { icon: '🏋️', name: 'Dumbbell Row', detail: '3 × 12 reps', sets: '3×12' },
      { icon: '💪', name: 'Shoulder Press', detail: '3 × 12 reps', sets: '3×12' },
      { icon: '🔥', name: 'Tricep Dips', detail: '3 × 15 reps', sets: '3×15' },
    ]},
    { day: 'Wednesday', type: 'HIIT', color: '#f97316', exercises: [
      { icon: '🔥', name: 'Jump Rope', detail: '5 × 2 min', sets: '5×2m' },
      { icon: '💪', name: 'Box Jumps', detail: '4 × 12 reps', sets: '4×12' },
      { icon: '🏃', name: 'Sprint Intervals', detail: '8 × 30 sec', sets: '8×30s' },
      { icon: '🧘', name: 'Cool-down Stretch', detail: '10 minutes', sets: 'Flex' },
    ]},
    { day: 'Thursday', type: 'Lower Body', color: '#8b5cf6', exercises: [
      { icon: '🏋️', name: 'Squats', detail: '4 × 15 reps', sets: '4×15' },
      { icon: '💪', name: 'Lunges', detail: '3 × 12 each', sets: '3×12' },
      { icon: '🔥', name: 'Leg Press', detail: '4 × 10 reps', sets: '4×10' },
      { icon: '💪', name: 'Calf Raises', detail: '3 × 20 reps', sets: '3×20' },
    ]},
    { day: 'Friday', type: 'Active Recovery', color: '#10b981', exercises: [
      { icon: '🧘', name: 'Yoga Flow', detail: '30 minutes', sets: 'Flow' },
      { icon: '🏊', name: 'Light Swimming', detail: '20 laps', sets: 'Cardio' },
      { icon: '💆', name: 'Foam Rolling', detail: '15 minutes', sets: 'Recovery' },
      { icon: '🧘', name: 'Meditation', detail: '10 minutes', sets: 'Mind' },
    ]},
  ]
};

function renderWorkouts() {
  workoutsLoaded = true;
  const grid = document.getElementById('workout-plan-grid');
  if (!grid) return;
  const goal = document.getElementById('workout-goal-select')?.value || 'Weight Loss';
  const plan = workoutPlans[goal] || workoutPlans['Weight Loss'];
  grid.innerHTML = plan.map(day => `
    <div class="workout-day-card">
      <div class="workout-day-header">
        <div class="day-badge" style="background:${day.color}">${day.day}</div>
        <div class="workout-day-title">${day.type}</div>
      </div>
      <div class="workout-day-body">
        ${day.exercises.map(ex => `
          <div class="workout-exercise-item">
            <div class="ex-icon">${ex.icon}</div>
            <div class="ex-info">
              <strong>${ex.name}</strong>
              <span>${ex.detail}</span>
            </div>
            <span class="ex-sets">${ex.sets}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');
}

document.getElementById('gen-workout-btn').addEventListener('click', () => {
  workoutsLoaded = false;
  renderWorkouts();
});
document.getElementById('workout-goal-select')?.addEventListener('change', () => {
  workoutsLoaded = false;
  renderWorkouts();
});

// ── Body Progress ────────────────────────────────────────────
let progressLoaded = false;
const transformationData = [
  { icon: '🏁', title: 'Started Program', detail: 'Weight: 82 kg, Body fat: 24%', date: 'Jan 2025' },
  { icon: '💪', title: 'First Milestone', detail: 'Lost 3 kg, bench press +10 kg', date: 'Feb 2025' },
  { icon: '🔥', title: 'Breaking Plateau', detail: 'Switched to HIIT + strength combo', date: 'Mar 2025' },
  { icon: '📊', title: 'Mid Assessment', detail: 'Weight: 76 kg, Body fat: 20%', date: 'Apr 2025' },
  { icon: '🏆', title: 'Goal Achieved!', detail: 'Target weight reached — 74.2 kg', date: 'May 2025' },
];

function renderProgress() {
  progressLoaded = true;
  const tl = document.getElementById('transformation-timeline');
  if (!tl) return;
  tl.innerHTML = transformationData.map(item => `
    <div class="tf-item">
      <div class="tf-dot">${item.icon}</div>
      <div class="tf-content">
        <strong>${item.title}</strong>
        <span>${item.detail}</span>
        <div class="tf-date">${item.date}</div>
      </div>
    </div>
  `).join('');
}

document.querySelectorAll('.timeline-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.timeline-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
  });
});

// ── Diet ─────────────────────────────────────────────────────
let dietLoaded = false;
function renderDiet() {
  dietLoaded = true;
  const dietChart = document.getElementById('diet-chart');
  if (!dietChart) return;
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const cals = [2100, 1950, 2200, 1800, 2050, 2300, 1840];
  const maxC = Math.max(...cals);
  dietChart.innerHTML = `
    <div style="display:flex;align-items:flex-end;gap:6px;width:100%;height:80px">
      ${days.map((d, i) => `
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px">
          <div class="diet-bar ${i === 6 ? 'today' : ''}" style="height:${Math.round((cals[i]/maxC)*70)}px"></div>
          <span class="diet-bar-label">${d}</span>
        </div>
      `).join('')}
    </div>
  `;
}

document.getElementById('log-meal-btn').addEventListener('click', () => {
  const meal = prompt('Log a meal (e.g. "Protein shake — 250 kcal")');
  if (!meal) return;
  const list = document.getElementById('meal-log-list');
  const now = new Date();
  const timeStr = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  const div = document.createElement('div');
  div.className = 'meal-entry';
  div.innerHTML = `
    <div class="meal-time">${timeStr}</div>
    <div class="meal-details"><strong>Custom Meal</strong><span>${meal}</span></div>
    <div class="meal-cals">—</div>
  `;
  list.prepend(div);
});

// ── Heatmap ──────────────────────────────────────────────────
let heatmapLoaded = false;
function renderHeatmap() {
  heatmapLoaded = true;
  const container = document.getElementById('annual-heatmap');
  if (!container) return;
  const totalWeeks = 52;
  let html = '';
  for (let w = 0; w < totalWeeks; w++) {
    for (let d = 0; d < 7; d++) {
      const count = Math.floor(Math.random() * 300);
      const level = count === 0 ? 0 : count < 50 ? 1 : count < 100 ? 2 : count < 200 ? 3 : count < 250 ? 4 : 5;
      html += `<div class="hm-cell" data-level="${level}" data-count="${count}"></div>`;
    }
  }
  container.innerHTML = html;

  const equipGrid = document.getElementById('equipment-grid-disp');
  if (!equipGrid) return;
  const equipment = [
    { icon: '🏋️', name: 'Barbell', usage: '94%', width: '94%' },
    { icon: '💪', name: 'Dumbbells', usage: '89%', width: '89%' },
    { icon: '🔄', name: 'Cable Machine', usage: '82%', width: '82%' },
    { icon: '🏃', name: 'Treadmill', usage: '78%', width: '78%' },
    { icon: '🚲', name: 'Spin Bike', usage: '65%', width: '65%' },
    { icon: '🧘', name: 'Yoga Mat', usage: '58%', width: '58%' },
    { icon: '⚖️', name: 'Leg Press', usage: '72%', width: '72%' },
    { icon: '🥊', name: 'Punching Bag', usage: '45%', width: '45%' },
    { icon: '🏊', name: 'Swimming', usage: '38%', width: '38%' },
  ];
  equipGrid.innerHTML = equipment.map(eq => `
    <div class="equipment-item">
      <div class="eq-icon">${eq.icon}</div>
      <div class="eq-name">${eq.name}</div>
      <div class="eq-usage">${eq.usage} usage</div>
      <div class="eq-bar-wrap"><div class="eq-bar" style="width:${eq.width}"></div></div>
    </div>
  `).join('');
}

// ── Trainers ─────────────────────────────────────────────────
let trainersLoaded = false;
const trainerData = [
  { name: 'Aryan Kapoor', specialty: 'Strength & Conditioning', members: 48, rating: 4.9, reviews: 142, exp: '8 yrs', grad: 'linear-gradient(135deg,#3b82f6,#06b6d4)', letter: 'A', tags: ['Powerlifting', 'HIIT', 'CrossFit'] },
  { name: 'Meena Sharma', specialty: 'Yoga & Wellness', members: 62, rating: 4.8, reviews: 198, exp: '10 yrs', grad: 'linear-gradient(135deg,#ec4899,#8b5cf6)', letter: 'M', tags: ['Hatha Yoga', 'Meditation', 'Flexibility'] },
  { name: 'Rohan Verma', specialty: 'Sports Performance', members: 35, rating: 4.7, reviews: 87, exp: '6 yrs', grad: 'linear-gradient(135deg,#f59e0b,#ef4444)', letter: 'R', tags: ['Cardio', 'Agility', 'Nutrition'] },
  { name: 'Pooja Nair', specialty: 'Weight Loss Specialist', members: 74, rating: 4.9, reviews: 223, exp: '9 yrs', grad: 'linear-gradient(135deg,#10b981,#06b6d4)', letter: 'P', tags: ['Fat Loss', 'Diet', 'Pilates'] },
  { name: 'Vikash Rao', specialty: 'Bodybuilding & Bulk', members: 41, rating: 4.6, reviews: 95, exp: '7 yrs', grad: 'linear-gradient(135deg,#8b5cf6,#3b82f6)', letter: 'V', tags: ['Hypertrophy', 'Powerlifting', 'Diet'] },
  { name: 'Sana Mirza', specialty: 'Functional Fitness', members: 53, rating: 4.8, reviews: 167, exp: '5 yrs', grad: 'linear-gradient(135deg,#f97316,#eab308)', letter: 'S', tags: ['Mobility', 'Core', 'Balance'] },
];

function renderTrainers() {
  trainersLoaded = true;
  const grid = document.getElementById('trainers-grid');
  if (!grid) return;
  grid.innerHTML = trainerData.map(t => `
    <div class="trainer-card">
      <div class="trainer-cover" style="background:${t.grad}">
        <div class="trainer-avatar-lg" style="background:${t.grad}">${t.letter}</div>
      </div>
      <div class="trainer-card-body">
        <div class="trainer-name">${t.name}</div>
        <div class="trainer-specialty">${t.specialty}</div>
        <div class="trainer-stats">
          <div class="trainer-stat"><div class="ts-num">${t.members}</div><div class="ts-label">Members</div></div>
          <div class="trainer-stat"><div class="ts-num">${t.exp}</div><div class="ts-label">Experience</div></div>
        </div>
        <div class="trainer-tags">${t.tags.map(tag => `<span class="trainer-tag">${tag}</span>`).join('')}</div>
        <div class="trainer-rating">
          <span class="rating-stars">${'★'.repeat(Math.floor(t.rating))}${t.rating % 1 ? '½' : ''}</span>
          <span class="rating-num">${t.rating}</span>
          <span class="rating-count">(${t.reviews} reviews)</span>
        </div>
        <button class="trainer-book-btn">📅 Book Session</button>
      </div>
    </div>
  `).join('');
}

// ── Schedule ─────────────────────────────────────────────────
let scheduleLoaded = false;
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let selectedDay = new Date().getDate();

const scheduledSessions = [
  { time: '6:00 AM', duration: '60 min', title: 'Morning HIIT', trainer: 'Aryan Kapoor', status: 'confirmed', members: 12 },
  { time: '8:30 AM', duration: '45 min', title: 'Yoga Flow', trainer: 'Meena Sharma', status: 'confirmed', members: 8 },
  { time: '11:00 AM', duration: '60 min', title: 'Strength Circuit', trainer: 'Rohan Verma', status: 'pending', members: 6 },
  { time: '5:00 PM', duration: '90 min', title: 'Spin Class', trainer: 'Sana Mirza', status: 'full', members: 20 },
  { time: '7:00 PM', duration: '60 min', title: 'Boxing Fitness', trainer: 'Vikash Rao', status: 'confirmed', members: 10 },
];

function renderSchedule() {
  scheduleLoaded = true;
  renderCalendar();
  renderSessions();
}

function renderCalendar() {
  const grid = document.getElementById('cal-grid');
  const label = document.getElementById('cal-month-label');
  if (!grid || !label) return;

  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  label.textContent = `${monthNames[currentMonth]} ${currentYear}`;

  const firstDay = new Date(currentYear, currentMonth, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const today = new Date();
  const sessionDays = [3, 7, 10, 14, 17, 21, 24, 27, 30];

  let html = ['Su','Mo','Tu','We','Th','Fr','Sa'].map(d => `<div class="cal-day-header">${d}</div>`).join('');

  for (let i = 0; i < firstDay; i++) {
    const prevDays = new Date(currentYear, currentMonth, 0).getDate() - firstDay + 1 + i;
    html += `<div class="cal-day other-month">${prevDays}</div>`;
  }

  for (let d = 1; d <= daysInMonth; d++) {
    const isToday = d === today.getDate() && currentMonth === today.getMonth() && currentYear === today.getFullYear();
    const isSelected = d === selectedDay && currentMonth === today.getMonth();
    const hasSession = sessionDays.includes(d);
    const classes = ['cal-day', isToday ? 'today' : '', isSelected && !isToday ? 'selected' : '', hasSession ? 'has-session' : ''].filter(Boolean).join(' ');
    html += `<div class="${classes}" data-day="${d}" onclick="selectDay(${d})">${d}</div>`;
  }

  grid.innerHTML = html;
}

window.selectDay = function(day) {
  selectedDay = day;
  document.querySelectorAll('.cal-day').forEach(d => d.classList.remove('selected'));
  const el = document.querySelector(`.cal-day[data-day="${day}"]`);
  if (el && !el.classList.contains('today')) el.classList.add('selected');
  document.getElementById('selected-date-label').textContent = `${day} ${document.getElementById('cal-month-label').textContent}`;
  renderSessions();
};

function renderSessions() {
  const list = document.getElementById('sessions-list');
  if (!list) return;
  list.innerHTML = scheduledSessions.map(s => `
    <div class="session-item">
      <div class="session-time-block">
        <div class="session-time">${s.time}</div>
        <div class="session-duration">${s.duration}</div>
      </div>
      <div class="session-divider"></div>
      <div class="session-info">
        <strong>${s.title}</strong>
        <span>👤 ${s.trainer} · ${s.members} members</span>
      </div>
      <span class="session-badge ${s.status}">${s.status}</span>
    </div>
  `).join('');
}

document.getElementById('cal-prev').addEventListener('click', () => {
  currentMonth--;
  if (currentMonth < 0) { currentMonth = 11; currentYear--; }
  renderCalendar();
});
document.getElementById('cal-next').addEventListener('click', () => {
  currentMonth++;
  if (currentMonth > 11) { currentMonth = 0; currentYear++; }
  renderCalendar();
});
document.getElementById('book-session-btn').addEventListener('click', () => {
  const title = prompt('Session title?');
  if (!title) return;
  scheduledSessions.push({ time: '9:00 AM', duration: '60 min', title, trainer: 'To Be Assigned', status: 'pending', members: 0 });
  renderSessions();
});

// ── Revenue ──────────────────────────────────────────────────
let revenueLoaded = false;
const revenueData = [48200, 52400, 44800, 61200, 57800, 68400, 72100, 65300, 79800, 84200, 88600, 94280];
const months = ['Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May'];

function renderRevenue() {
  revenueLoaded = true;
  const chart = document.getElementById('revenue-chart');
  if (!chart) return;
  const maxR = Math.max(...revenueData);
  chart.innerHTML = revenueData.map((v, i) => `
    <div class="rev-bar-col">
      <div class="rev-bar" style="height:${Math.round((v/maxR)*140)}px" title="₹${v.toLocaleString('en-IN')}"></div>
      <span class="rev-bar-label">${months[i]}</span>
    </div>
  `).join('');

  // Pie chart SVG
  const pie = document.getElementById('revenue-pie');
  if (pie) {
    pie.innerHTML = `
      <svg viewBox="0 0 160 160" class="pie-svg">
        <circle cx="80" cy="80" r="60" fill="none" stroke="#3b82f6" stroke-width="30"
          stroke-dasharray="${2 * Math.PI * 60 * 0.34} ${2 * Math.PI * 60}" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
        <circle cx="80" cy="80" r="60" fill="none" stroke="#10b981" stroke-width="30"
          stroke-dasharray="${2 * Math.PI * 60 * 0.41} ${2 * Math.PI * 60}"
          stroke-dashoffset="${-2 * Math.PI * 60 * 0.34}" transform="rotate(-90 80 80)"/>
        <circle cx="80" cy="80" r="60" fill="none" stroke="#f59e0b" stroke-width="30"
          stroke-dasharray="${2 * Math.PI * 60 * 0.25} ${2 * Math.PI * 60}"
          stroke-dashoffset="${-2 * Math.PI * 60 * 0.75}" transform="rotate(-90 80 80)"/>
        <circle cx="80" cy="80" r="46" fill="white"/>
        <text x="80" y="76" text-anchor="middle" font-size="9" fill="#64748b" font-family="Inter">Revenue</text>
        <text x="80" y="90" text-anchor="middle" font-size="11" fill="#0f172a" font-weight="700" font-family="Inter">₹94K</text>
      </svg>`;
  }

  const txns = [
    { member: 'Rahul Sharma', plan: 'Elite', amount: '₹3,499', date: '26 May 2026', status: 'paid' },
    { member: 'Priya Mehta', plan: 'Pro', amount: '₹1,999', date: '25 May 2026', status: 'paid' },
    { member: 'Arjun Patel', plan: 'Elite', amount: '₹3,499', date: '24 May 2026', status: 'paid' },
    { member: 'Sneha Kapoor', plan: 'Pro', amount: '₹1,999', date: '23 May 2026', status: 'pending' },
    { member: 'Vikram Singh', plan: 'Basic', amount: '₹999', date: '22 May 2026', status: 'paid' },
    { member: 'Riya Bose', plan: 'Pro', amount: '₹1,999', date: '21 May 2026', status: 'failed' },
    { member: 'Dev Khanna', plan: 'Basic', amount: '₹999', date: '20 May 2026', status: 'paid' },
  ];
  const tbody = document.getElementById('transactions-body');
  if (tbody) {
    tbody.innerHTML = txns.map(t => `
      <tr>
        <td><strong>${t.member}</strong></td>
        <td>${t.plan}</td>
        <td><strong>${t.amount}</strong></td>
        <td>${t.date}</td>
        <td><span class="txn-status ${t.status}">${t.status}</span></td>
      </tr>
    `).join('');
  }
}

// ── Reminders ────────────────────────────────────────────────
let remindersLoaded = false;
let remindersList = [
  { icon: '💳', bg: 'rgba(59,130,246,0.1)', title: 'Membership Renewal — Riya Bose', desc: 'Expires in 3 days', time: 'Today, 10:00 AM' },
  { icon: '⚠️', bg: 'rgba(245,158,11,0.1)', title: 'Absence Alert — Anjali Roy', desc: '5 days without check-in', time: 'Today, 2:00 PM' },
  { icon: '🎯', bg: 'rgba(16,185,129,0.1)', title: 'Goal Check-in — Rahul Sharma', desc: 'Monthly body assessment due', time: 'Tomorrow, 9:00 AM' },
];

function renderReminders() {
  remindersLoaded = true;
  const list = document.getElementById('reminders-list');
  if (!list) return;
  list.innerHTML = remindersList.map((r, i) => `
    <div class="reminder-item" id="reminder-${i}">
      <div class="reminder-icon" style="background:${r.bg}">${r.icon}</div>
      <div class="reminder-info">
        <strong>${r.title}</strong>
        <span>${r.desc}</span>
      </div>
      <div class="reminder-time">${r.time}</div>
      <button class="delete-reminder" onclick="deleteReminder(${i})">✕</button>
    </div>
  `).join('');
}

window.deleteReminder = function(i) {
  remindersList.splice(i, 1);
  renderReminders();
};

document.getElementById('create-reminder-btn').addEventListener('click', () => {
  const title = prompt('Reminder title?');
  if (!title) return;
  remindersList.push({ icon: '🔔', bg: 'rgba(139,92,246,0.1)', title, desc: 'Custom reminder', time: 'Today' });
  renderReminders();
});

// ── AI Assistant ─────────────────────────────────────────────
const aiPanel = document.getElementById('ai-assistant-panel');
const aiMessages = document.getElementById('ai-messages');
const aiInput = document.getElementById('ai-input');

document.getElementById('open-ai-btn').addEventListener('click', () => aiPanel.classList.add('open'));
document.getElementById('close-ai-btn').addEventListener('click', () => aiPanel.classList.remove('open'));

const aiResponses = {
  'weight loss': '🔥 For weight loss, I recommend a calorie deficit of 300–500 kcal/day combined with 4–5 cardio sessions per week. Focus on HIIT workouts and track your meals daily. Based on Rahul\'s data, he\'s on track to hit his goal in 6 weeks!',
  'muscle gain': '💪 To build muscle, focus on progressive overload — increase weights by 2.5–5% weekly. Prioritize compound lifts: squats, deadlifts, bench press. Consume 1.6–2.2g of protein per kg of bodyweight. Sleep 8+ hours nightly.',
  'diet': '🥗 A balanced diet for muscle gain includes: 40% carbs, 30% protein, 30% fats. I recommend 5–6 small meals per day. Key foods: chicken, eggs, oats, sweet potatoes, leafy greens, and Greek yogurt.',
  'attendance': '📍 To improve attendance: 1) Send reminder 1 hour before each session, 2) Run a "streak challenge" — reward 30-day attendance streaks, 3) Schedule sessions at consistent times. Your peak hours are 6–8 AM and 6–8 PM.',
  'top performers': '🏆 Your top performers this month:\n1. Rahul Sharma — 98% attendance, 42 sessions\n2. Priya Mehta — 95% attendance, 38 sessions\n3. Arjun Patel — 92% attendance, 35 sessions\nConsider rewarding them with a free month upgrade!',
  'revenue': '💰 This month\'s revenue is ₹94,280, up 18.7%! The Elite plan drives 25% of revenue from only 12% of members. I recommend converting more Pro members to Elite with a trial offer.',
  'default': '🤖 That\'s a great question! I\'m analyzing your gym data... Based on current trends, I suggest focusing on member retention (currently 87%) and promoting your Elite plan. Would you like me to generate a detailed report?'
};

function getAIResponse(msg) {
  const lower = msg.toLowerCase();
  for (const [key, resp] of Object.entries(aiResponses)) {
    if (lower.includes(key)) return resp;
  }
  return aiResponses['default'];
}

function addMessage(text, isUser) {
  const div = document.createElement('div');
  div.className = `ai-message ${isUser ? 'user' : 'bot'}`;
  const now = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  div.innerHTML = `<div class="ai-bubble">${text}</div><div class="ai-msg-time">${now}</div>`;
  aiMessages.appendChild(div);
  aiMessages.scrollTop = aiMessages.scrollHeight;
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'ai-message bot';
  div.id = 'ai-typing';
  div.innerHTML = `<div class="ai-typing"><span></span><span></span><span></span></div>`;
  aiMessages.appendChild(div);
  aiMessages.scrollTop = aiMessages.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById('ai-typing');
  if (t) t.remove();
}

function sendAIMessage(text) {
  if (!text.trim()) return;
  aiPanel.classList.add('open');
  addMessage(text, true);
  aiInput.value = '';
  showTyping();
  setTimeout(() => {
    hideTyping();
    addMessage(getAIResponse(text), false);
  }, 1200 + Math.random() * 600);
}

document.getElementById('ai-send-btn').addEventListener('click', () => sendAIMessage(aiInput.value));
aiInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendAIMessage(aiInput.value); });

document.querySelectorAll('.ai-suggestion-chip').forEach(chip => {
  chip.addEventListener('click', () => sendAIMessage(chip.dataset.msg));
});

// Notification bell
document.getElementById('notif-btn').addEventListener('click', () => {
  aiPanel.classList.add('open');
  addMessage('🔔 You have 3 pending notifications: 2 membership renewals due and 1 trainer session unassigned.', false);
});

// ── Timeline tabs (progress page) ───────────────────────────
document.addEventListener('click', e => {
  if (e.target.classList.contains('timeline-tab')) {
    document.querySelectorAll('.timeline-tab').forEach(t => t.classList.remove('active'));
    e.target.classList.add('active');
  }
});

// ── Log Measurement ──────────────────────────────────────────
document.getElementById('log-measurement-btn')?.addEventListener('click', () => {
  const w = prompt('Enter current weight (kg):');
  if (!w) return;
  const bf = prompt('Enter body fat % (optional):');
  alert(`✅ Measurement logged!\nWeight: ${w} kg${bf ? `\nBody Fat: ${bf}%` : ''}\n\nThe AI will update your progress charts.`);
});

// ── Initial render complete ──────────────────────────────────
console.log('%c🚀 FitSphere AI Platform Loaded', 'color:#3b82f6;font-size:16px;font-weight:bold;');
