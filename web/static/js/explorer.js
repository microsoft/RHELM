(() => {
  "use strict";

  const TYPE_META = {
    attachment: { color: "#f3a93b", label: "Attachment" },
    mixed: { color: "#8b5cf6", label: "Mixed" },
    fact: { color: "#4f7cff", label: "Fact" },
    hallucination: { color: "#ef6a75", label: "Hallucination" },
    aggregation: { color: "#20b486", label: "Aggregation" },
    temporal: { color: "#26a6c7", label: "Temporal" },
    misleading: { color: "#e16d34", label: "Misleading" },
  };

  const numberFormatter = new Intl.NumberFormat("en-US");
  const explorer = document.querySelector("#dataset-explorer");

  if (!explorer) return;

  const elements = {
    loading: explorer.querySelector("#explorer-loading"),
    error: explorer.querySelector("#explorer-error"),
    content: explorer.querySelector("#explorer-content"),
    distribution: explorer.querySelector("#question-distribution"),
    donut: explorer.querySelector("#source-donut"),
    sourceTotal: explorer.querySelector("#source-total"),
    sourceLegend: explorer.querySelector("#source-legend"),
    characteristics: explorer.querySelector("#characteristic-cloud"),
    personaSelect: explorer.querySelector("#sample-persona"),
    typeSelect: explorer.querySelector("#sample-type"),
    randomButton: explorer.querySelector("#sample-random"),
    previousButton: explorer.querySelector("#sample-previous"),
    nextButton: explorer.querySelector("#sample-next"),
    revealButton: explorer.querySelector("#sample-reveal"),
    card: explorer.querySelector("#sample-card"),
    sampleType: explorer.querySelector("#sample-card-type"),
    samplePersona: explorer.querySelector("#sample-card-persona"),
    sampleDate: explorer.querySelector("#sample-card-date"),
    question: explorer.querySelector("#sample-question"),
    answer: explorer.querySelector("#sample-answer"),
    evidence: explorer.querySelector("#sample-evidence"),
    challengeList: explorer.querySelector("#sample-characteristics"),
    counter: explorer.querySelector("#sample-counter"),
    progress: explorer.querySelector("#sample-progress-fill"),
    empty: explorer.querySelector("#sample-empty"),
    sampleContent: explorer.querySelector("#sample-content"),
  };

  const state = {
    data: null,
    filteredSamples: [],
    sampleIndex: 0,
  };

  function typeMeta(type) {
    return TYPE_META[type] || { color: "#64748b", label: type };
  }

  function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function switchTab(tabName) {
    explorer.querySelectorAll("[data-explorer-tab]").forEach((button) => {
      const isActive = button.dataset.explorerTab === tabName;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-selected", String(isActive));
      button.tabIndex = isActive ? 0 : -1;
    });

    explorer.querySelectorAll("[data-explorer-panel]").forEach((panel) => {
      const isActive = panel.dataset.explorerPanel === tabName;
      panel.hidden = !isActive;
      panel.classList.toggle("is-entering", isActive);
    });
  }

  function renderSummary(summary) {
    Object.entries(summary).forEach(([key, value]) => {
      const target = explorer.querySelector(`[data-summary="${key}"]`);
      if (target) target.textContent = numberFormatter.format(value);
    });
  }

  function renderDistribution(questionTypes) {
    elements.distribution.replaceChildren();
    const maximum = Math.max(...questionTypes.map((item) => item.count));

    questionTypes.forEach((item) => {
      const meta = typeMeta(item.type);
      const row = createElement("button", "distribution-row");
      row.type = "button";
      row.style.setProperty("--type-color", meta.color);
      row.setAttribute(
        "aria-label",
        `Explore ${numberFormatter.format(item.count)} ${meta.label} questions`,
      );

      const label = createElement("span", "distribution-label");
      label.append(createElement("span", "distribution-dot"));
      label.append(createElement("span", "", meta.label));

      const track = createElement("span", "distribution-track");
      const fill = createElement("span", "distribution-fill");
      track.append(fill);

      row.append(label, track, createElement("span", "distribution-count", item.count));
      row.addEventListener("click", () => {
        elements.typeSelect.value = item.type;
        applySampleFilters();
        switchTab("samples");
        elements.question.focus({ preventScroll: true });
      });
      elements.distribution.append(row);

      requestAnimationFrame(() => {
        fill.style.width = `${(item.count / maximum) * 100}%`;
      });
    });
  }

  function renderSources(sources) {
    const sourceConfig = [
      { key: "conversations", label: "Conversations", color: "#4f7cff" },
      { key: "emails", label: "Emails", color: "#20b486" },
      { key: "attachments", label: "Attachments", color: "#f3a93b" },
    ];
    const total = sourceConfig.reduce((sum, source) => sum + sources[source.key], 0);
    const conversationEnd = (sources.conversations / total) * 100;
    const emailEnd = conversationEnd + (sources.emails / total) * 100;

    elements.donut.style.setProperty("--conversation-end", `${conversationEnd}%`);
    elements.donut.style.setProperty("--email-end", `${emailEnd}%`);
    elements.sourceTotal.textContent = numberFormatter.format(total);
    elements.sourceLegend.replaceChildren();

    sourceConfig.forEach((source) => {
      const item = createElement("div", "source-legend-item");
      const swatch = createElement("span", "source-legend-swatch");
      swatch.style.setProperty("--source-color", source.color);
      item.append(
        swatch,
        createElement("span", "source-legend-label", source.label),
        createElement(
          "span",
          "source-legend-value",
          numberFormatter.format(sources[source.key]),
        ),
      );
      elements.sourceLegend.append(item);
    });
  }

  function renderCharacteristics(characteristics) {
    elements.characteristics.replaceChildren();
    characteristics.slice(0, 10).forEach((characteristic) => {
      const chip = createElement("div", "characteristic-chip", characteristic.name);
      chip.append(createElement("span", "", numberFormatter.format(characteristic.count)));
      elements.characteristics.append(chip);
    });
  }

  function populateFilters(data) {
    data.personas.forEach((persona) => {
      const option = createElement("option", "", persona.name);
      option.value = persona.name;
      elements.personaSelect.append(option);
    });

    data.questionTypes.forEach((questionType) => {
      const meta = typeMeta(questionType.type);
      const option = createElement(
        "option",
        "",
        `${meta.label} (${numberFormatter.format(questionType.count)})`,
      );
      option.value = questionType.type;
      elements.typeSelect.append(option);
    });
  }

  function applySampleFilters() {
    const persona = elements.personaSelect.value;
    const type = elements.typeSelect.value;
    state.filteredSamples = state.data.samples.filter(
      (sample) =>
        (persona === "all" || sample.persona === persona) &&
        (type === "all" || sample.type === type),
    );
    state.sampleIndex = 0;
    renderSample();
  }

  function renderChips(container, values, emptyLabel) {
    container.replaceChildren();
    if (!values.length) {
      container.append(createElement("span", "detail-chip", emptyLabel));
      return;
    }
    values.forEach((value) => {
      container.append(createElement("span", "detail-chip", value));
    });
  }

  function renderSample() {
    const total = state.filteredSamples.length;
    const hasSamples = total > 0;
    elements.empty.hidden = hasSamples;
    elements.sampleContent.hidden = !hasSamples;
    elements.previousButton.disabled = total <= 1;
    elements.nextButton.disabled = total <= 1;
    elements.randomButton.disabled = total <= 1;

    if (!hasSamples) {
      elements.counter.textContent = "No samples";
      elements.progress.style.width = "0";
      return;
    }

    const sample = state.filteredSamples[state.sampleIndex];
    const meta = typeMeta(sample.type);
    elements.card.style.setProperty("--sample-color", meta.color);
    elements.sampleType.textContent = meta.label;
    elements.samplePersona.textContent = sample.persona;
    elements.sampleDate.textContent = sample.questionDate;
    elements.question.textContent = sample.question;
    elements.answer.textContent = sample.answer;
    elements.answer.hidden = true;
    elements.revealButton.hidden = false;
    elements.revealButton.setAttribute("aria-expanded", "false");
    elements.revealButton.querySelector("span:last-child").textContent = "Reveal answer";
    renderChips(elements.evidence, sample.evidence, "No evidence reference");
    renderChips(elements.challengeList, sample.characteristics, "General retrieval");
    elements.counter.textContent = `${state.sampleIndex + 1} of ${total} samples`;
    elements.progress.style.width = `${((state.sampleIndex + 1) / total) * 100}%`;
  }

  function moveSample(direction) {
    const total = state.filteredSamples.length;
    if (total <= 1) return;
    state.sampleIndex = (state.sampleIndex + direction + total) % total;
    renderSample();
  }

  function showRandomSample() {
    const total = state.filteredSamples.length;
    if (total <= 1) return;
    let nextIndex = state.sampleIndex;
    while (nextIndex === state.sampleIndex) {
      nextIndex = Math.floor(Math.random() * total);
    }
    state.sampleIndex = nextIndex;
    renderSample();
  }

  function bindInteractions() {
    explorer.querySelectorAll("[data-explorer-tab]").forEach((button) => {
      button.addEventListener("click", () => switchTab(button.dataset.explorerTab));
      button.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        const tabs = [...explorer.querySelectorAll("[data-explorer-tab]")];
        const direction = event.key === "ArrowRight" ? 1 : -1;
        const nextIndex = (tabs.indexOf(button) + direction + tabs.length) % tabs.length;
        tabs[nextIndex].focus();
        tabs[nextIndex].click();
      });
    });

    elements.personaSelect.addEventListener("change", applySampleFilters);
    elements.typeSelect.addEventListener("change", applySampleFilters);
    elements.previousButton.addEventListener("click", () => moveSample(-1));
    elements.nextButton.addEventListener("click", () => moveSample(1));
    elements.randomButton.addEventListener("click", showRandomSample);
    elements.revealButton.addEventListener("click", () => {
      const willReveal = elements.answer.hidden;
      elements.answer.hidden = !willReveal;
      elements.revealButton.setAttribute("aria-expanded", String(willReveal));
      elements.revealButton.querySelector("span:last-child").textContent = willReveal
        ? "Hide answer"
        : "Reveal answer";
    });
  }

  async function initialize() {
    bindInteractions();
    try {
      const response = await fetch("static/data/explorer-data.json");
      if (!response.ok) throw new Error(`Data request failed (${response.status})`);
      const data = await response.json();
      state.data = data;
      renderSummary(data.summary);
      renderDistribution(data.questionTypes);
      renderSources(data.sources);
      renderCharacteristics(data.characteristics);
      populateFilters(data);
      applySampleFilters();
      elements.loading.hidden = true;
      elements.content.hidden = false;
    } catch (error) {
      console.error("Unable to initialize the RHELM dataset explorer:", error);
      elements.loading.hidden = true;
      elements.error.hidden = false;
    }
  }

  initialize();
})();
