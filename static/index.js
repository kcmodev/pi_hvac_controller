const systemStatus = document.querySelector("#system-status");
const lastSpray = document.querySelector("#last-spray");
const sprayButton = document.querySelector("#spray-button");
const message = document.querySelector("#message");

/** Fetches JSON, rejecting with the server's error message on a failed response. */
async function requestJson(url, options) {
  const response = await fetch(url, options);
  const body = await response.json();
  if (!response.ok) {
    const error = new Error(body.error);
    error.status = response.status;
    throw error;
  }
  return body;
}

function showLastSpray({ date, time }) {
  lastSpray.textContent = `${date} at ${time}`;
}

async function loadSystemStatus() {
  try {
    const { status } = await requestJson("/status");
    systemStatus.textContent = status;
  } catch {
    systemStatus.textContent = "Unavailable";
  }
}

async function loadLastSpray() {
  try {
    showLastSpray(await requestJson("/timestamp"));
  } catch (error) {
    lastSpray.textContent = error.status === 404 ? "Never" : "Unavailable";
  }
}

async function spray() {
  sprayButton.disabled = true;
  message.textContent = "Starting the fan, then spraying…";
  try {
    showLastSpray(await requestJson("/spray", { method: "POST" }));
    message.textContent = "Done.";
  } catch (error) {
    message.textContent = error.message || "Could not reach the controller.";
  } finally {
    sprayButton.disabled = false;
  }
}

sprayButton.addEventListener("click", spray);
loadSystemStatus();
loadLastSpray();
