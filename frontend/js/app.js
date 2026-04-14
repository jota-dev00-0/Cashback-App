const API_URL = "https://cashback-app-xqja.onrender.com/api/v1";

async function submitCashback() {
  const clientType    = document.getElementById("client_type").value;
  const purchaseValue = parseFloat(document.getElementById("purchase_value").value);

  const errorEl = document.getElementById("error-msg");
  errorEl.style.display = "none";

  if (!purchaseValue || purchaseValue <= 0) {
    errorEl.textContent = "Informe um valor de compra válido.";
    errorEl.style.display = "block";
    return;
  }

  const btn = document.getElementById("submit-btn");
  btn.disabled    = true;
  btn.textContent = "Calculando...";

  try {
    const res = await fetch(`${API_URL}/cashback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client_type: clientType, purchase_value: purchaseValue }),
    });

    if (!res.ok) throw new Error();

    const data = await res.json();

    // Detalhe: base sempre aparece; bônus VIP só se houver
    let detail = `Base: R$ ${data.cashback_base.toFixed(2)}`;
    if (data.cashback_bonus > 0) {
      detail += ` + Bônus VIP: R$ ${data.cashback_bonus.toFixed(2)}`;
    }

    document.getElementById("result-pct").textContent  = detail;
    document.getElementById("result-value").textContent = `R$ ${data.cashback_total.toFixed(2)}`;
    document.getElementById("result-box").classList.add("visible");

    loadHistory();
  } catch {
    errorEl.textContent = "Não foi possível conectar à API. Tente novamente.";
    errorEl.style.display = "block";
  } finally {
    btn.disabled    = false;
    btn.textContent = "Calcular";
  }
}

async function loadHistory() {
  const container = document.getElementById("history-container");

  try {
    const res = await fetch(`${API_URL}/cashback/history`);
    if (!res.ok) throw new Error();

    const logs = await res.json();

    if (logs.length === 0) {
      container.innerHTML = '<p class="history-empty">Nenhuma consulta ainda.</p>';
      return;
    }

    container.innerHTML = logs.map(log => `
      <div class="history-row">
        <span class="badge">${log.client_type}</span>
        <span class="purchase">R$ ${parseFloat(log.purchase_value).toFixed(2)}</span>
        <span class="cashback-val">+ R$ ${parseFloat(log.cashback_total).toFixed(2)}</span>
      </div>
    `).join("");
  } catch {
    container.innerHTML = '<p class="history-empty">Erro ao carregar histórico.</p>';
  }
}

loadHistory();