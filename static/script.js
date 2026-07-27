const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const uploadText = document.getElementById("upload-text");
const extractBtn = document.getElementById("extract-btn");
const paletteOutput = document.getElementById("palette-output");
const loading = document.getElementById("loading");
const errorMsg = document.getElementById("error-msg");
const numColorsSlider = document.getElementById("num-colors");
const numColorsValue = document.getElementById("num-colors-value");
const downloadSection = document.getElementById("download-section");

let selectedFile = null;
let currentPalette = [];

numColorsSlider.addEventListener("input", () => {
  numColorsValue.textContent = numColorsSlider.value;
});

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files.length) {
    handleFile(e.dataTransfer.files[0]);
  }
});

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length) {
    handleFile(e.target.files[0]);
  }
});

function handleFile(file) {
  if (!file.type.startsWith("image/")) return;
  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  preview.style.display = "block";
  uploadText.style.display = "none";
  extractBtn.disabled = false;
  errorMsg.style.display = "none";
}

extractBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  loading.style.display = "block";
  paletteOutput.innerHTML = "";
  errorMsg.style.display = "none";
  downloadSection.style.display = "none";
  extractBtn.disabled = true;
  currentPalette = [];

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("num_colors", numColorsSlider.value);

  try {
    const res = await fetch("/extract", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok || data.error) {
      errorMsg.textContent = data.error || "Unable to extract palette.";
      errorMsg.style.display = "block";
    } else {
      currentPalette = data.palette || [];
      renderPalette(currentPalette);
      if (currentPalette.length) {
        downloadSection.style.display = "block";
      }
    }
  } catch (err) {
    errorMsg.textContent = "Something went wrong. Please try again.";
    errorMsg.style.display = "block";
  } finally {
    loading.style.display = "none";
    extractBtn.disabled = false;
  }
});

function renderPalette(palette) {
  paletteOutput.innerHTML = "";

  if (!palette.length) {
    paletteOutput.innerHTML = "<p class='error'>No colors could be extracted.</p>";
    return;
  }

  palette.forEach((color) => {
    const percentValue = Math.round(color.percentage * 100);

    const swatch = document.createElement("div");
    swatch.className = "swatch";
    swatch.style.backgroundColor = color.hex;
    swatch.innerHTML = `
      <span class="hex">${color.hex}</span>
      <span class="percent">${percentValue}%</span>
    `;

    swatch.addEventListener("click", () => {
      navigator.clipboard.writeText(color.hex).catch(() => {});
      const hex = swatch.querySelector(".hex");
      hex.textContent = "Copied!";
      setTimeout(() => { hex.textContent = color.hex; }, 800);
    });

    paletteOutput.appendChild(swatch);
  });
}

document.querySelectorAll(".download-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    if (!currentPalette.length) return;

    const format = btn.getAttribute("data-format");

    try {
      const res = await fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ palette: currentPalette, format }),
      });

      if (!res.ok) throw new Error("Download failed");

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `palette.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      errorMsg.textContent = "Download failed. Please try again.";
      errorMsg.style.display = "block";
    }
  });
});
