(() => {
  "use strict";

  const root = document.documentElement;
  const nav = document.querySelector("#site-nav");
  const navToggle = document.querySelector("#nav-toggle");
  const navLinks = [...document.querySelectorAll(".nav-link[href^='#']")];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  root.classList.add("js-ready");

  function closeMenu() {
    if (!nav || !navToggle) return;
    nav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("nav-open");
  }

  function updateNavAppearance() {
    if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 18);
    const marker = window.scrollY + (nav?.offsetHeight || 0) + 140;
    let activeSectionId = navLinks[0]?.getAttribute("href")?.slice(1);
    navLinks.forEach((link) => {
      const section = document.querySelector(link.getAttribute("href"));
      if (section && section.offsetTop <= marker) activeSectionId = section.id;
    });
    navLinks.forEach((link) => {
      const isActive = link.getAttribute("href") === `#${activeSectionId}`;
      link.classList.toggle("is-active", isActive);
      if (isActive) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const willOpen = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", willOpen);
      navToggle.setAttribute("aria-expanded", String(willOpen));
      document.body.classList.toggle("nav-open", willOpen);
    });

    navLinks.forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });
    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) closeMenu();
    });
  }

  updateNavAppearance();
  window.addEventListener("scroll", updateNavAppearance, { passive: true });

  const featureTabs = [...document.querySelectorAll("[data-feature-target]")];
  const featurePanels = [...document.querySelectorAll("[data-feature-panel]")];
  const supportsHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  function activateFeature(featureName) {
    featureTabs.forEach((tab) => {
      const isActive = tab.dataset.featureTarget === featureName;
      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-selected", String(isActive));
      tab.tabIndex = isActive ? 0 : -1;
    });

    featurePanels.forEach((panel) => {
      const isActive = panel.dataset.featurePanel === featureName;
      panel.hidden = !isActive;
      panel.classList.toggle("is-active", isActive);
      panel.classList.toggle("is-entering", isActive);
    });
  }

  featureTabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activateFeature(tab.dataset.featureTarget));
    tab.addEventListener("focus", () => activateFeature(tab.dataset.featureTarget));
    if (supportsHover) {
      tab.addEventListener("pointerenter", () => activateFeature(tab.dataset.featureTarget));
    }
    tab.addEventListener("keydown", (event) => {
      if (!["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)) return;
      event.preventDefault();
      const direction = event.key === "ArrowDown" || event.key === "ArrowRight" ? 1 : -1;
      const nextTab = featureTabs[(index + direction + featureTabs.length) % featureTabs.length];
      nextTab.focus();
    });
  });

  const constructionPipeline = document.querySelector("[data-construction-pipeline]");
  const pipelineSteps = constructionPipeline
    ? [...constructionPipeline.querySelectorAll("[data-pipeline-step]")]
    : [];
  const pipelineStatus = constructionPipeline?.querySelector("[data-pipeline-status]");
  const pipelineControl = constructionPipeline?.querySelector("[data-pipeline-control]");
  let pipelineIndex = -1;
  let pipelineTimer = null;
  let pipelinePlaying = false;
  let pipelineStarted = false;
  let pipelineObserver = null;

  function updatePipelineControl() {
    if (!pipelineControl) return;
    const icon = pipelineControl.querySelector("i");
    const label = pipelineControl.querySelector("span");
    const isComplete = pipelineIndex === pipelineSteps.length - 1;
    if (icon) icon.className = pipelinePlaying ? "fas fa-pause" : isComplete ? "fas fa-rotate-right" : "fas fa-play";
    if (label) label.textContent = pipelinePlaying ? "Pause" : isComplete ? "Replay" : pipelineIndex >= 0 ? "Resume" : "Play flow";
    pipelineControl.setAttribute(
      "aria-label",
      pipelinePlaying
        ? "Pause construction workflow animation"
        : isComplete
          ? "Replay construction workflow animation"
          : "Play construction workflow animation",
    );
  }

  function showPipelineStep(index) {
    if (!constructionPipeline || !pipelineSteps[index]) return;
    pipelineIndex = index;
    constructionPipeline.classList.remove("is-complete");
    constructionPipeline.style.setProperty(
      "--pipeline-progress-value",
      `${((index + 1) / pipelineSteps.length) * 100}%`,
    );

    pipelineSteps.forEach((step, stepIndex) => {
      const isActive = stepIndex === index;
      step.classList.toggle("is-active", isActive);
      step.classList.toggle("is-complete", stepIndex < index);
      if (isActive) step.setAttribute("aria-current", "step");
      else step.removeAttribute("aria-current");
    });

    constructionPipeline.querySelectorAll(".pipeline-module").forEach((module) => {
      module.classList.toggle("has-active-step", Boolean(module.querySelector(".pipeline-step.is-active")));
    });

    if (pipelineStatus) {
      pipelineStatus.textContent = `Step ${index + 1} of ${pipelineSteps.length} · ${pipelineSteps[index].dataset.stepLabel}`;
    }
    updatePipelineControl();
  }

  function finishPipeline() {
    pipelinePlaying = false;
    pipelineTimer = null;
    constructionPipeline?.classList.add("is-complete");
    if (pipelineStatus) pipelineStatus.textContent = "Complete · LOOP trajectory construction finished";
    updatePipelineControl();
  }

  function advancePipeline() {
    if (!pipelinePlaying) return;
    const nextIndex = pipelineIndex + 1;
    if (nextIndex >= pipelineSteps.length) {
      finishPipeline();
      return;
    }
    showPipelineStep(nextIndex);
    pipelineTimer = window.setTimeout(advancePipeline, nextIndex === 5 ? 1800 : 1450);
  }

  function playPipeline(restart = false) {
    if (!constructionPipeline || !pipelineSteps.length) return;
    window.clearTimeout(pipelineTimer);
    if (restart || pipelineIndex === pipelineSteps.length - 1) {
      pipelineIndex = -1;
      pipelineSteps.forEach((step) => step.classList.remove("is-active", "is-complete"));
      constructionPipeline.style.setProperty("--pipeline-progress-value", "0%");
      constructionPipeline.classList.remove("is-complete");
    }
    pipelinePlaying = true;
    updatePipelineControl();
    advancePipeline();
  }

  function pausePipeline() {
    pipelinePlaying = false;
    window.clearTimeout(pipelineTimer);
    pipelineTimer = null;
    updatePipelineControl();
  }

  pipelineControl?.addEventListener("click", () => {
    if (pipelinePlaying) pausePipeline();
    else playPipeline(pipelineIndex === pipelineSteps.length - 1);
  });

  pipelineSteps.forEach((step, index) => {
    step.addEventListener("click", () => {
      pausePipeline();
      showPipelineStep(index);
    });
  });

  function startPipelineOnView() {
    if (pipelineStarted) return;
    pipelineStarted = true;
    playPipeline(true);
    pipelineObserver?.disconnect();
    window.removeEventListener("scroll", checkPipelineVisibility);
  }

  function checkPipelineVisibility() {
    if (!constructionPipeline || pipelineStarted) return;
    const bounds = constructionPipeline.getBoundingClientRect();
    if (bounds.top < window.innerHeight * 0.84 && bounds.bottom > window.innerHeight * 0.16) {
      startPipelineOnView();
    }
  }

  if (constructionPipeline && pipelineSteps.length) {
    constructionPipeline.dataset.pipelineReady = "true";
    if (reduceMotion || !("IntersectionObserver" in window)) {
      showPipelineStep(0);
    } else {
      pipelineObserver = new IntersectionObserver(
        (entries) => {
          if (entries.some((entry) => entry.isIntersecting)) startPipelineOnView();
        },
        { threshold: 0.16 },
      );
      pipelineObserver.observe(constructionPipeline);
      window.addEventListener("scroll", checkPipelineVisibility, { passive: true });
      window.addEventListener("load", checkPipelineVisibility, { once: true });
      window.requestAnimationFrame(checkPipelineVisibility);
    }
  }

  const resultsTabs = [...document.querySelectorAll("[data-results-target]")];
  const resultsPanels = [...document.querySelectorAll("[data-results-panel]")];

  function activateResultsPanel(panelName) {
    resultsTabs.forEach((tab) => {
      const isActive = tab.dataset.resultsTarget === panelName;
      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-selected", String(isActive));
      tab.tabIndex = isActive ? 0 : -1;
    });

    resultsPanels.forEach((panel) => {
      panel.hidden = panel.dataset.resultsPanel !== panelName;
    });
  }

  resultsTabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activateResultsPanel(tab.dataset.resultsTarget));
    tab.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      let nextIndex = index;
      if (event.key === "ArrowLeft") nextIndex = (index - 1 + resultsTabs.length) % resultsTabs.length;
      if (event.key === "ArrowRight") nextIndex = (index + 1) % resultsTabs.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = resultsTabs.length - 1;
      const nextTab = resultsTabs[nextIndex];
      activateResultsPanel(nextTab.dataset.resultsTarget);
      nextTab.focus();
    });
  });

  const revealElements = [...document.querySelectorAll(".reveal")];
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealElements.forEach((element) => element.classList.add("is-visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -6%", threshold: 0.01 },
    );
    revealElements.forEach((element) => {
      const bounds = element.getBoundingClientRect();
      if (bounds.top < window.innerHeight * 0.94 && bounds.bottom > 0) {
        element.classList.add("is-visible");
      } else {
        revealObserver.observe(element);
      }
    });
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.append(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
  }

  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    button.addEventListener("click", async () => {
      const target = document.querySelector(button.dataset.copyTarget);
      if (!target) return;
      const originalLabel = button.querySelector("span")?.textContent || "Copy";
      try {
        await copyText(target.textContent.trim());
        button.classList.add("is-copied");
        const label = button.querySelector("span");
        if (label) label.textContent = "Copied";
        const icon = button.querySelector("i");
        if (icon) icon.className = "fas fa-check";
        window.setTimeout(() => {
          button.classList.remove("is-copied");
          if (label) label.textContent = originalLabel;
          if (icon) icon.className = "far fa-copy";
        }, 1800);
      } catch (error) {
        console.error("Unable to copy text:", error);
      }
    });
  });

  const lightbox = document.querySelector("#image-lightbox");
  const lightboxImage = lightbox?.querySelector("img");
  const lightboxClose = lightbox?.querySelector(".lightbox-close");
  let lastFocusedElement = null;

  function openLightbox(image) {
    if (!lightbox || !lightboxImage) return;
    lastFocusedElement = document.activeElement;
    lightboxImage.src = image.src;
    lightboxImage.alt = image.alt;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("nav-open");
    lightboxClose?.focus();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("nav-open");
    if (lightboxImage) lightboxImage.removeAttribute("src");
    if (lastFocusedElement instanceof HTMLElement) lastFocusedElement.focus();
  }

  document.querySelectorAll("img[data-zoom]").forEach((image) => {
    image.classList.add("zoomable");
    image.tabIndex = 0;
    image.setAttribute("role", "button");
    image.setAttribute("aria-label", `${image.alt}. Open larger view.`);
    image.addEventListener("click", () => openLightbox(image));
    image.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openLightbox(image);
      }
    });
  });

  lightboxClose?.addEventListener("click", closeLightbox);
  lightbox?.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && lightbox?.classList.contains("is-open")) closeLightbox();
  });
})();
