document.addEventListener("DOMContentLoaded", () => {

    const canvas = document.getElementById("statusChart");


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

  // Make chart
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
});
