/* =========================================================================
     CONFIG
     ========================================================================= */
const DEMO_MODE = false;
const WS_URL = "wss://m/prod/";

  /* =========================================================================
     STATE
     ========================================================================= */
  const state = {
    total: 0,
    flaggedToday: 0,
    latencySamples: [],
    recentTimestamps: [],
    casesById: {},
    fraudHistory: []
  };

  function parseIncomingEvent(raw) {
    try {
        const message = JSON.parse(raw);

        if (message.type !== "transaction") {
            console.log("Ignoring non-transaction message:", message);
            return null;
        }

        const data = message.data || {};
        const features = data.features || {};
        const rag = data.rag || {};

        return {
            id:
                data.transactionId ||
                data.txn_id ||
                data.id ||
                "UNKNOWN",

            timestamp:
                data.timestamp ||
                Date.now(),

            // Flink puts the complete ML vector inside features
            amount:
                Number(data.amount ?? features.amount) || 0,

            status:
                (data.isFraud ?? message.isFraud)
                    ? "flagged"
                    : "cleared",

            latencyMs:
                typeof data.latencyMs === "number"
                    ? data.latencyMs
                    : null,

            findings:
                Array.isArray(rag.findings)
                    ? rag.findings
                    : [],

            citations:
                Array.isArray(rag.citations)
                    ? rag.citations
                    : [],

            recommendation:
                rag.recommendation || null,

            riskAssessment:
                rag.riskAssessment || null
        };

    } catch (err) {
        console.error(
            "parseIncomingEvent: failed to parse message",
            err,
            raw
        );

        return null;
    }
}

  /* =========================================================================
     WEBSOCKET
     ========================================================================= */
  let socket = null;
  let reconnectDelay = 1000;

  function setStatus(mode, text) {
    const dot = document.getElementById("statusDot");
    const label = document.getElementById("statusText");
    dot.className = "status-dot" + (mode === "live" ? "" : " " + mode);
    label.textContent = text;
  }

  function connect() {
    setStatus("reconnecting", "Connecting…");
    socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      reconnectDelay = 1000;
      setStatus("live", "Live");
    };

    socket.onmessage = (event) => {
      const txn = parseIncomingEvent(event.data);
      if (txn) handleTransaction(txn);
    };

    socket.onclose = () => {
      setStatus("offline", "Disconnected — retrying…");
      setTimeout(connect, reconnectDelay);
      reconnectDelay = Math.min(reconnectDelay * 1.6, 15000);
    };

    socket.onerror = () => {
      socket.close();
    };
  }

  /* =========================================================================
     RENDERING
     ========================================================================= */
function handleTransaction(txn) {

    state.total += 1;

    state.recentTimestamps.push(Date.now());

    if (typeof txn.latencyMs === "number") {
        state.latencySamples.push(txn.latencyMs);
    }

    if (txn.status === "flagged") {

        state.flaggedToday += 1;

        // Keep permanent fraud history for this browser session
        state.casesById[txn.id] = txn;
        state.fraudHistory.push(txn);

        // Add it to the fraud tab
        renderFraudRow(txn);
    }

    // Live feed remains bounded
    renderRow(txn);

    updateKPIs();
}

  function renderRow(txn) {
    const feed = document.getElementById("feed");
    const emptyState = document.getElementById("feedEmptyState");
    if (emptyState) emptyState.remove();

    const row = document.createElement("div");
    row.className = "txn-row" + (txn.status === "flagged" ? " flagged" : "");

    const time = new Date(txn.timestamp || Date.now());
    const timeLabel = time.toLocaleTimeString([], { hour12: false });

    row.innerHTML = `
      <span class="txn-id">${escapeHtml(txn.id)}</span>
      <span class="txn-time">${timeLabel}</span>
      <span class="txn-amount">₹${formatAmount(txn.amount)}</span>
      <span class="badge ${txn.status === "flagged" ? "flagged" : "cleared"}">${txn.status}</span>
    `;

    if (txn.status === "flagged") {
      row.addEventListener("click", () => renderCaseFile(txn));
    }

    feed.insertBefore(row, feed.firstChild);

    // keep the feed from growing forever
    while (feed.children.length > 60) {
      feed.removeChild(feed.lastChild);
    }
  }

  function renderFraudRow(txn) {

    const feed = document.getElementById("fraudFeed");
    const emptyState = document.getElementById("fraudEmptyState");

    if (emptyState) {
        emptyState.remove();
    }

    const row = document.createElement("div");

    row.className = "txn-row flagged";

    const time = new Date(txn.timestamp || Date.now());

    const timeLabel = time.toLocaleTimeString([], {
        hour12: false
    });

    row.innerHTML = `
        <span class="txn-id">
            ${escapeHtml(txn.id)}
        </span>

        <span class="txn-time">
            ${timeLabel}
        </span>

        <span class="txn-amount">
            ₹${formatAmount(txn.amount)}
        </span>

        <span class="badge flagged">
            flagged
        </span>
    `;

    row.addEventListener("click", () => {
        renderFraudCaseFile(txn);
    });

    // Newest fraud transaction at the top
    feed.insertBefore(row, feed.firstChild);
}

  function renderFraudCaseFile(txn) {

    const panel = document.getElementById("fraudCasePanel");

    panel.classList.remove("empty");

    const findings = (txn.findings || [])
        .map(f => `<li>${escapeHtml(f)}</li>`)
        .join("");

    const citations = (txn.citations || [])
        .map(c => `<li>${escapeHtml(c)}</li>`)
        .join("");

    panel.innerHTML = `
        <div class="case-header">

            <div>

                <span class="case-tag">
                    FLAGGED
                </span>

                <div class="case-id">
                    ${escapeHtml(txn.id)}
                </div>

            </div>

            <div class="case-amount">
                ₹${formatAmount(txn.amount)}
            </div>

        </div>


        <div class="case-section-title">
            Agent Findings
        </div>

        <ol class="findings-list">
            ${
                findings ||
                "<li>No findings provided.</li>"
            }
        </ol>


        <div class="case-section-title">
            Compliance References
        </div>

        <ul class="citations">
            ${
                citations ||
                "<li>No citations attached.</li>"
            }
        </ul>
    `;
}

  function renderCaseFile(txn) {
    const panel = document.getElementById("casePanel");
    panel.classList.remove("empty");

    const findings = (txn.findings || []).map(f => `<li>${escapeHtml(f)}</li>`).join("");
    const citations = (txn.citations || []).map(c => `<li>${escapeHtml(c)}</li>`).join("");

    panel.innerHTML = `
      <div class="case-header">
        <div>
          <span class="case-tag">FLAGGED</span>
          <div class="case-id">${escapeHtml(txn.id)}</div>
        </div>
        <div class="case-amount">₹${formatAmount(txn.amount)}</div>
      </div>

      <div class="case-section-title">Agent Findings</div>
      <ol class="findings-list">${findings || "<li>No findings provided.</li>"}</ol>

      <div class="case-section-title">Compliance References</div>
      <ul class="citations">${citations || "<li>No citations attached.</li>"}</ul>
    `;
  }

  function updateKPIs() {
    document.getElementById("kpiTotal").textContent = state.total.toLocaleString();
    document.getElementById("kpiFlagged").textContent = state.flaggedToday.toLocaleString();

    const now = Date.now();
    state.recentTimestamps = state.recentTimestamps.filter(t => now - t <= 10000);
    const rate = state.recentTimestamps.length / 10;
    document.getElementById("kpiRate").textContent = rate.toFixed(1);

    if (state.latencySamples.length) {
      const avg = state.latencySamples.reduce((a, b) => a + b, 0) / state.latencySamples.length;
      document.getElementById("kpiLatency").textContent = Math.round(avg) + " ms";
      if (state.latencySamples.length > 200) state.latencySamples.shift();
    }
  }

  function formatAmount(n) {
    if (typeof n !== "number") return "—";
    return n.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str == null ? "" : String(str);
    return div.innerHTML;
  }
  
  /* =========================================================================
     THEME TOGGLE
     ========================================================================= */
  const themeToggle = document.getElementById("themeToggle");
  themeToggle.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.documentElement.removeAttribute("data-theme");
      themeToggle.textContent = "🌙 Dark";
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      themeToggle.textContent = "☀️ Light";
    }
  });

  /* =========================================================================
   TABS
   ========================================================================= */

const liveTab = document.getElementById("liveTab");
const fraudTab = document.getElementById("fraudTab");

const liveView = document.getElementById("liveView");
const fraudView = document.getElementById("fraudView");


liveTab.addEventListener("click", () => {

    liveTab.classList.add("active");
    fraudTab.classList.remove("active");

    liveView.style.display = "grid";
    fraudView.style.display = "none";
});


fraudTab.addEventListener("click", () => {

    fraudTab.classList.add("active");
    liveTab.classList.remove("active");

    liveView.style.display = "none";
    fraudView.style.display = "grid";
});

  /* =========================================================================
     BOOT
     ========================================================================= */
    connect();
