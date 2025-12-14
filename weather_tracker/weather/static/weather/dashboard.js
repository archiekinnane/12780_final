document.addEventListener("DOMContentLoaded", () => {

    const canvas = document.getElementById("statusChart");
    const time_canvas = document.getElementById("timeChart");


  // Helper function
  function readJsonScript(id) {
    const el = document.getElementById(id);
    if (!el) {
      console.error(`JSON script tag #${id} not found`);
      return null;
    }
    try {
      return JSON.parse(el.textContent);
    } catch (err) {
      console.error(`Failed to parse JSON from #${id}`, err);
      return null;
    }
  }

  // Read data
  const labels = readJsonScript("status-labels");
  const counts = readJsonScript("status-values");


  if (!labels || !counts) return;
  if (!Array.isArray(labels) || !Array.isArray(counts)) {
    console.error("Expected labels and counts to be arrays.", { labels, counts });
    return;
  }

  // Status breakdown chart
  new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Queries",
          data: counts,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 },
        },
      },
    },
  });


  // Queries over time chart
  const time_labels = readJsonScript("time-labels");
  const time_values = readJsonScript("time-values");

  new Chart(time_canvas, {
    type: "line",
    data: {
      labels: time_labels,
      datasets: [
        {
          label: "Dates",
          data: time_values,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          ticks: { precision: 0 },
        },
      },
    },
  });

});
