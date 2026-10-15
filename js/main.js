/* ==========================================================================
   CEYLON GERMAN PATHWAY - INTERACTIONS
   Vanilla JS, shared by every page. Each block is a no-op when its markup
   is absent, so one file serves all seven pages.
   ========================================================================== */

(function () {
  "use strict";

  var toArray = function (list) {
    return Array.prototype.slice.call(list);
  };

  /* ----------------------------------------------------------------------
     Logo fallback
     If assets/images/CGPLogo.png is missing or fails to load, show the
     typographic lockup instead of a broken-image icon.
     ---------------------------------------------------------------------- */
  toArray(document.querySelectorAll(".logo__img")).forEach(function (img) {
    var useFallback = function () {
      var logo = img.closest(".logo");
      if (logo) logo.classList.add("logo--fallback");
      img.remove();
    };

    img.addEventListener("error", useFallback);

    // Covers the case where the image already failed before this ran.
    if (img.complete && img.naturalWidth === 0) useFallback();
  });

  /* ----------------------------------------------------------------------
     Mobile navigation toggle
     ---------------------------------------------------------------------- */
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  /* ----------------------------------------------------------------------
     Accordions - any [data-accordion]; one panel open at a time within each
     ---------------------------------------------------------------------- */
  toArray(document.querySelectorAll("[data-accordion]")).forEach(function (group) {
    var items = toArray(group.querySelectorAll(".accordion__item"));

    items.forEach(function (item) {
      var trigger = item.querySelector(".accordion__trigger");
      if (!trigger) return;

      trigger.addEventListener("click", function () {
        var wasOpen = item.classList.contains("is-open");

        items.forEach(function (other) {
          other.classList.remove("is-open");
          var t = other.querySelector(".accordion__trigger");
          if (t) t.setAttribute("aria-expanded", "false");
        });

        if (!wasOpen) {
          item.classList.add("is-open");
          trigger.setAttribute("aria-expanded", "true");
        }
      });
    });
  });

  /* ----------------------------------------------------------------------
     Journey rail - arrows, drag-to-scroll, progress bar
     ---------------------------------------------------------------------- */
  var track = document.querySelector("[data-journey-track]");

  if (track) {
    var prevBtn = document.querySelector("[data-journey-prev]");
    var nextBtn = document.querySelector("[data-journey-next]");
    var progressBar = document.querySelector("[data-journey-progress]");

    var stepWidth = function () {
      var step = track.querySelector(".journey-step");
      return step ? step.offsetWidth + 24 : 320;
    };

    var updateRail = function () {
      var max = track.scrollWidth - track.clientWidth;

      if (prevBtn) prevBtn.disabled = track.scrollLeft <= 4;
      if (nextBtn) nextBtn.disabled = track.scrollLeft >= max - 4;

      if (progressBar && max > 0) {
        var width = (track.clientWidth / track.scrollWidth) * 100;
        progressBar.style.width = width + "%";
        progressBar.style.left = (track.scrollLeft / max) * (100 - width) + "%";
      }
    };

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        track.scrollBy({ left: -stepWidth(), behavior: "smooth" });
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        track.scrollBy({ left: stepWidth(), behavior: "smooth" });
      });
    }

    track.addEventListener("scroll", updateRail, { passive: true });
    window.addEventListener("resize", updateRail);
    updateRail();

    var dragging = false;
    var dragStartX = 0;
    var dragStartScroll = 0;

    track.addEventListener("pointerdown", function (e) {
      dragging = true;
      dragStartX = e.clientX;
      dragStartScroll = track.scrollLeft;
      track.classList.add("is-dragging");
    });

    window.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      track.scrollLeft = dragStartScroll - (e.clientX - dragStartX);
    });

    window.addEventListener("pointerup", function () {
      dragging = false;
      track.classList.remove("is-dragging");
    });
  }

  /* ----------------------------------------------------------------------
     Tabs - every [role="tablist"] on the page (WAI-ARIA pattern)
     ---------------------------------------------------------------------- */
  toArray(document.querySelectorAll('[role="tablist"]')).forEach(function (tablist) {
    var tabs = toArray(tablist.querySelectorAll('[role="tab"]'));

    var selectTab = function (tab, focus) {
      tabs.forEach(function (t) {
        var selected = t === tab;
        t.setAttribute("aria-selected", String(selected));
        t.tabIndex = selected ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !selected;
      });
      if (focus !== false) tab.focus();
    };

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () {
        selectTab(tab, false);
      });

      tab.addEventListener("keydown", function (e) {
        var target = null;
        if (e.key === "ArrowRight") target = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") target = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") target = tabs[0];
        if (e.key === "End") target = tabs[tabs.length - 1];
        if (target) {
          e.preventDefault();
          selectTab(target);
        }
      });
    });
  });

  /* ----------------------------------------------------------------------
     Enquiry form - composes a pre-filled email.
     NOTE: this is a static site with no backend. The form opens the
     visitor's mail client with the details filled in. To collect
     submissions server-side, point form.action at a form service instead.
     ---------------------------------------------------------------------- */
  var form = document.querySelector("[data-enquiry-form]");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (!form.reportValidity()) return;

      var data = new FormData(form);
      var lines = [];

      data.forEach(function (value, key) {
        if (String(value).trim() === "") return;
        var field = form.elements[key];
        var label = form.querySelector('label[for="' + key + '"]');
        var name = label ? label.textContent.replace("*", "").trim() : key;
        lines.push(name + ": " + value);
      });

      var subject = "Request for information - " + (data.get("interest") || "CGP");
      var body =
        "Hello CGP,\n\nI would like more information about the pathway.\n\n" +
        lines.join("\n") +
        "\n\nThank you.";

      var status = form.querySelector("[data-form-status]");
      if (status) {
        status.textContent = "Opening your email app…";
      }

      window.location.href =
        "mailto:hello@cgp.lk" +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    });
  }

  /* ----------------------------------------------------------------------
     Nav dropdown - disclosure menu for "About CGP".
     Opens on hover (pointer devices) and on click/Enter, closes on Escape,
     on outside click and when focus leaves the menu. The button carries
     aria-expanded so the state is announced.
     ---------------------------------------------------------------------- */
  var hoverPointer = window.matchMedia("(hover: hover) and (min-width: 62.01rem)");

  toArray(document.querySelectorAll("[data-nav-menu]")).forEach(function (item) {
    var button = item.querySelector(".nav__toggle");
    var submenu = item.querySelector(".nav__submenu");
    if (!button || !submenu) return;

    var setOpen = function (open) {
      item.classList.toggle("is-open", open);
      button.setAttribute("aria-expanded", String(open));
    };

    var close = function () {
      setOpen(false);
    };

    button.addEventListener("click", function () {
      setOpen(!item.classList.contains("is-open"));
    });

    item.addEventListener("mouseenter", function () {
      if (hoverPointer.matches) setOpen(true);
    });

    item.addEventListener("mouseleave", function () {
      if (hoverPointer.matches) close();
    });

    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) close();
    });

    item.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        close();
        button.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (!item.contains(e.target)) close();
    });
  });

  /* ----------------------------------------------------------------------
     Hero banner slider - three rotating banners on the home page.
     Accessible carousel: arrow keys, swipe, dots, and a play/pause control.
     Rotation stops on hover, on focus, when the tab is hidden, after any
     deliberate interaction, and entirely under prefers-reduced-motion.
     ---------------------------------------------------------------------- */
  var slider = document.querySelector("[data-hero-slider]");

  if (slider) {
    var track = slider.querySelector("[data-slider-track]");
    var slides = toArray(slider.querySelectorAll(".hero-slide"));
    var dots = toArray(slider.querySelectorAll("[data-slider-dot]"));
    var prevBtn = slider.querySelector("[data-slider-prev]");
    var nextBtn = slider.querySelector("[data-slider-next]");
    var toggleBtn = slider.querySelector("[data-slider-toggle]");
    var viewport = slider.querySelector(".hero-slider__viewport");

    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
    var interval = parseInt(slider.getAttribute("data-autoplay"), 10) || 7000;
    var index = 0;
    var timer = null;
    var playing = false;

    var stop = function () {
      if (timer) window.clearInterval(timer);
      timer = null;
      playing = false;
      if (toggleBtn) {
        toggleBtn.setAttribute("aria-label", "Play banner rotation");
        toggleBtn.setAttribute("aria-pressed", "false");
        toggleBtn.textContent = "\u25B6";
      }
    };

    var start = function () {
      if (reduced.matches || slides.length < 2 || timer) return;
      timer = window.setInterval(function () {
        show(index + 1);
      }, interval);
      playing = true;
      if (toggleBtn) {
        toggleBtn.setAttribute("aria-label", "Pause banner rotation");
        toggleBtn.setAttribute("aria-pressed", "true");
        toggleBtn.textContent = "\u2016";
      }
    };

    var show = function (next) {
      index = (next + slides.length) % slides.length;
      track.style.transform = "translateX(" + (index * -100) + "%)";

      slides.forEach(function (slide, i) {
        var active = i === index;
        slide.setAttribute("aria-hidden", String(!active));
        toArray(slide.querySelectorAll("a, button")).forEach(function (el) {
          if (active) el.removeAttribute("tabindex");
          else el.setAttribute("tabindex", "-1");
        });
      });

      dots.forEach(function (dot, i) {
        dot.setAttribute("aria-current", String(i === index));
      });
    };

    show(0);

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        stop();
        show(index - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        stop();
        show(index + 1);
      });
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        stop();
        show(i);
      });
    });

    if (toggleBtn) {
      toggleBtn.addEventListener("click", function () {
        if (playing) stop();
        else start();
      });
    }

    slider.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") {
        stop();
        show(index + 1);
      }
      if (e.key === "ArrowLeft") {
        stop();
        show(index - 1);
      }
    });

    slider.addEventListener("mouseenter", stop);
    slider.addEventListener("focusin", stop);

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop();
    });

    // Swipe / drag
    var startX = 0;
    var dragging = false;

    if (viewport) {
      viewport.addEventListener("pointerdown", function (e) {
        if (e.pointerType === "mouse") return;
        dragging = true;
        startX = e.clientX;
      });

      viewport.addEventListener("pointerup", function (e) {
        if (!dragging) return;
        dragging = false;
        var delta = e.clientX - startX;
        if (Math.abs(delta) < 40) return;
        stop();
        show(delta < 0 ? index + 1 : index - 1);
      });

      viewport.addEventListener("pointercancel", function () {
        dragging = false;
      });
    }

    start();
  }

  /* ----------------------------------------------------------------------
     Reveal on scroll - subtle, one-shot, respects reduced motion
     ---------------------------------------------------------------------- */
  var reveals = document.querySelectorAll(".reveal");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  if (reveals.length && "IntersectionObserver" in window && !reduceMotion.matches) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -5% 0px" }
    );

    toArray(reveals).forEach(function (el) {
      observer.observe(el);
    });
  } else {
    toArray(reveals).forEach(function (el) {
      el.classList.add("is-visible");
    });
  }
})();
