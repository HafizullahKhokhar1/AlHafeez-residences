const towerTrack = document.querySelector("[data-tower-track]");

if (towerTrack) {
  const towerImages = Array.from(towerTrack.querySelectorAll(".tower-image"));
  let frameRequested = false;

  const updateTower = () => {
    const trackBounds = towerTrack.getBoundingClientRect();
    const scrollRange = towerTrack.offsetHeight - window.innerHeight;
    const progress = scrollRange > 0
      ? Math.min(1, Math.max(0, -trackBounds.top / scrollRange))
      : 0;
    const position = progress * (towerImages.length - 1);
    const firstImage = Math.floor(position);
    const crossfade = position - firstImage;

    towerImages.forEach((image, index) => {
      const opacity = index === firstImage
        ? 1 - crossfade
        : index === firstImage + 1
          ? crossfade
          : 0;
      image.style.opacity = String(opacity);
    });
  };

  const scheduleUpdate = () => {
    if (!frameRequested) {
      frameRequested = true;
      requestAnimationFrame(() => {
        frameRequested = false;
        updateTower();
      });
    }
  };

  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate);
  updateTower();
}

document.querySelectorAll("form[data-mailto]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const fields = new FormData(form);
    const message = Array.from(fields.entries())
      .map(([name, value]) => `${name}: ${value}`)
      .join("\n");
    const subject = encodeURIComponent("AlHafeez residence enquiry");
    const body = encodeURIComponent(message);
    window.location.href = `mailto:${form.dataset.mailto}?subject=${subject}&body=${body}`;
  });
});
