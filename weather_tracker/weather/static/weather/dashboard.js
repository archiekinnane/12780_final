document.addEventListener("DOMContentLoaded", () => {

    const canvas = document.getElementById("statusChart");
    const time_canvas = document.getElementById("timeChart");
    const deltaChart = document.getElementById("deltaChart");
    const selectedMetricLabel = readJsonScript("selected-metric-label") || "Metric";
    console.log("canvases:", { canvas, time_canvas, deltaChart });
    console.log("Chart typeof:", typeof Chart);


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

// Deltas by location 
  const delta_labels = readJsonScript("delta-labels");
  const delta_values = readJsonScript("delta-values");


  new Chart(deltaChart, {
    type: "bar",
    data: {
      labels: delta_labels,
      datasets: [
        {
          label: `Change in ${selectedMetricLabel} by location`,
          data: delta_values,
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

