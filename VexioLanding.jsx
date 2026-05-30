import { useState, useEffect, useRef, useCallback } from "react";

/* ─────────────────────────────────────────────
   GLOBAL STYLES injected once
───────────────────────────────────────────── */
const GLOBAL_CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  
  :root {
    --bg: #0A0A0A;
    --surface: rgba(255,255,255,0.035);
    --surface-hover: rgba(255,255,255,0.065);
    --border: rgba(255,255,255,0.08);
    --border-glow: rgba(139,92,246,0.35);
    --text: #F0EEF8;
    --text-dim: rgba(240,238,248,0.45);
    --text-muted: rgba(240,238,248,0.25);
    --purple: #8B5CF6;
    --purple-bright: #A78BFA;
    --purple-dim: rgba(139,92,246,0.15);
    --purple-glow: rgba(139,92,246,0.4);
    --font-display: 'Syne', sans-serif;
    --font-body: 'Outfit', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
  }

  ::selection { background: rgba(139,92,246,0.35); color: #fff; }

  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--purple-dim); border-radius: 2px; }

  @keyframes float-a {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-22px) rotate(3deg); }
  }
  @keyframes float-b {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(18px) rotate(-2deg); }
  }
  @keyframes float-c {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-14px) rotate(2deg); }
    66% { transform: translateY(10px) rotate(-1deg); }
  }
  @keyframes pulse-glow {
    0%,100% { box-shadow: 0 0 20px rgba(139,92,246,0.2), 0 0 60px rgba(139,92,246,0.05); }
    50% { box-shadow: 0 0 35px rgba(139,92,246,0.4), 0 0 100px rgba(139,92,246,0.1); }
  }
  @keyframes grid-scroll {
    0% { transform: translateY(0); }
    100% { transform: translateY(60px); }
  }
  @keyframes scanline {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
  }
  @keyframes cursor-blink {
    0%,100% { opacity: 1; }
    50% { opacity: 0; }
  }
  @keyframes progress-fill {
    0% { width: 0%; }
    100% { width: 100%; }
  }
  @keyframes fade-up {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
  }
  @keyframes orbit {
    from { transform: rotate(0deg) translateX(90px) rotate(0deg); }
    to { transform: rotate(360deg) translateX(90px) rotate(-360deg); }
  }
  @keyframes ripple {
    0% { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(2.5); opacity: 0; }
  }

  .glass {
    background: var(--surface);
    backdrop-filter: blur(24px) saturate(1.8);
    -webkit-backdrop-filter: blur(24px) saturate(1.8);
    border: 1px solid var(--border);
  }
  .glass-purple {
    background: rgba(139,92,246,0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(139,92,246,0.2);
  }
  .glow-text {
    text-shadow: 0 0 40px rgba(139,92,246,0.6), 0 0 80px rgba(139,92,246,0.3);
  }
  .shimmer-text {
    background: linear-gradient(90deg, #F0EEF8 0%, #A78BFA 40%, #F0EEF8 60%, #A78BFA 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
  }
  .btn-primary {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 14px 32px;
    background: linear-gradient(135deg, #7C3AED, #6D28D9);
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 12px;
    color: #fff;
    font-family: var(--font-body);
    font-size: 15px;
    font-weight: 500;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: all 0.3s ease;
    overflow: hidden;
  }
  .btn-primary::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }
  .btn-primary:hover::before { opacity: 1; }
  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(139,92,246,0.5), 0 2px 8px rgba(0,0,0,0.4);
  }
  .btn-primary:active { transform: translateY(0px); }

  .section-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--purple-bright);
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.2);
    margin-bottom: 24px;
  }
  .section-label::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--purple);
    box-shadow: 0 0 8px var(--purple);
    animation: pulse-glow 2s ease-in-out infinite;
  }
`;

/* ─────────────────────────────────────────────
   FLOATING GLASS ORBS – hero background
───────────────────────────────────────────── */
function FloatingOrbs() {
  const orbs = [
    { size: 320, x: "8%", y: "12%", anim: "float-a 8s ease-in-out infinite", opacity: 0.22, delay: "0s" },
    { size: 200, x: "75%", y: "8%", anim: "float-b 11s ease-in-out infinite", opacity: 0.16, delay: "2s" },
    { size: 260, x: "85%", y: "55%", anim: "float-c 9s ease-in-out infinite", opacity: 0.19, delay: "1s" },
    { size: 180, x: "20%", y: "68%", anim: "float-a 12s ease-in-out infinite", opacity: 0.14, delay: "3s" },
    { size: 140, x: "50%", y: "80%", anim: "float-b 7s ease-in-out infinite", opacity: 0.12, delay: "0.5s" },
    { size: 90, x: "62%", y: "30%", anim: "float-c 10s ease-in-out infinite", opacity: 0.18, delay: "1.5s" },
  ];
  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none", overflow: "hidden" }}>
      {orbs.map((o, i) => (
        <div key={i} style={{
          position: "absolute",
          left: o.x, top: o.y,
          width: o.size, height: o.size,
          borderRadius: "50%",
          background: `radial-gradient(circle at 30% 30%, rgba(139,92,246,${o.opacity + 0.05}), rgba(109,40,217,${o.opacity}), transparent 70%)`,
          filter: "blur(1px)",
          animation: o.anim,
          animationDelay: o.delay,
          border: `1px solid rgba(139,92,246,${o.opacity * 0.8})`,
          backdropFilter: "blur(8px)",
          boxShadow: `inset 0 0 60px rgba(139,92,246,${o.opacity * 0.5}), 0 0 40px rgba(139,92,246,${o.opacity * 0.3})`,
        }} />
      ))}
      {/* Grid overlay */}
      <div style={{
        position: "absolute", inset: 0,
        backgroundImage: `
          linear-gradient(rgba(139,92,246,0.05) 1px, transparent 1px),
          linear-gradient(90deg, rgba(139,92,246,0.05) 1px, transparent 1px)
        `,
        backgroundSize: "60px 60px",
        animation: "grid-scroll 8s linear infinite",
        maskImage: "radial-gradient(ellipse 80% 70% at 50% 50%, black 30%, transparent 100%)",
      }} />
    </div>
  );
}

/* ─────────────────────────────────────────────
   SECTION 1 — HERO
───────────────────────────────────────────── */
function Hero({ onViewProjects }) {
  const [visible, setVisible] = useState(false);
  useEffect(() => { setTimeout(() => setVisible(true), 100); }, []);

  return (
    <section style={{
      position: "relative",
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      textAlign: "center",
      padding: "80px 24px",
      overflow: "hidden",
    }}>
      <FloatingOrbs />

      {/* Noise texture */}
      <div style={{
        position: "absolute", inset: 0, pointerEvents: "none",
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E")`,
        backgroundRepeat: "repeat",
        backgroundSize: "200px 200px",
        opacity: 0.6,
      }} />

      <div style={{
        position: "relative", zIndex: 2,
        opacity: visible ? 1 : 0,
        transform: visible ? "none" : "translateY(30px)",
        transition: "all 1s cubic-bezier(0.22, 1, 0.36, 1)",
      }}>
        {/* Badge */}
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 40 }}>
          <div className="section-label">Studio — Est. 2024</div>
        </div>

        {/* Logo */}
        <h1 className="glow-text" style={{
          fontFamily: "var(--font-display)",
          fontSize: "clamp(72px, 16vw, 160px)",
          fontWeight: 800,
          letterSpacing: "-0.04em",
          lineHeight: 0.9,
          marginBottom: 32,
          background: "linear-gradient(160deg, #FFFFFF 0%, #D4C5FF 40%, #8B5CF6 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
        }}>
          VEXIO
        </h1>

        {/* Headline */}
        <h2 style={{
          fontFamily: "var(--font-display)",
          fontSize: "clamp(22px, 4vw, 44px)",
          fontWeight: 600,
          letterSpacing: "-0.02em",
          color: "var(--text)",
          marginBottom: 20,
          maxWidth: 700,
          lineHeight: 1.15,
        }}>
          Websites that don't feel<br />like templates.
        </h2>

        {/* Subheadline */}
        <p style={{
          fontSize: "clamp(15px, 2vw, 18px)",
          color: "var(--text-dim)",
          maxWidth: 520,
          lineHeight: 1.65,
          marginBottom: 48,
          fontWeight: 300,
        }}>
          Custom websites, admin panels and Telegram integrations for businesses that refuse to look ordinary.
        </p>

        {/* CTAs */}
        <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
          <button className="btn-primary" onClick={onViewProjects}>
            View Projects
            <span style={{ fontSize: 18 }}>↗</span>
          </button>
          <button style={{
            padding: "14px 28px",
            background: "transparent",
            border: "1px solid var(--border)",
            borderRadius: 12,
            color: "var(--text-dim)",
            fontSize: 15,
            fontFamily: "var(--font-body)",
            fontWeight: 400,
            cursor: "pointer",
            transition: "all 0.3s",
            backdropFilter: "blur(8px)",
          }}
            onMouseEnter={e => { e.target.style.borderColor = "rgba(139,92,246,0.4)"; e.target.style.color = "var(--text)"; }}
            onMouseLeave={e => { e.target.style.borderColor = "var(--border)"; e.target.style.color = "var(--text-dim)"; }}
          >
            Start a Project
          </button>
        </div>

        {/* Stats row */}
        <div style={{
          display: "flex", gap: 48, marginTop: 72, justifyContent: "center", flexWrap: "wrap",
        }}>
          {[["48+", "Projects"], ["4.9★", "Rating"], ["24h", "Response"]].map(([val, label]) => (
            <div key={label} style={{ textAlign: "center" }}>
              <div style={{ fontFamily: "var(--font-display)", fontSize: 28, fontWeight: 700, color: "var(--purple-bright)" }}>{val}</div>
              <div style={{ fontSize: 12, color: "var(--text-muted)", letterSpacing: "0.1em", textTransform: "uppercase", marginTop: 4 }}>{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div style={{
        position: "absolute", bottom: 32, left: "50%", transform: "translateX(-50%)",
        display: "flex", flexDirection: "column", alignItems: "center", gap: 8,
        opacity: 0.4, animation: "float-b 3s ease-in-out infinite",
      }}>
        <div style={{ fontSize: 11, fontFamily: "var(--font-mono)", letterSpacing: "0.15em", textTransform: "uppercase" }}>scroll</div>
        <div style={{ width: 1, height: 40, background: "linear-gradient(to bottom, var(--border), transparent)" }} />
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   SECTION 2 — PROJECT SHOWCASE
───────────────────────────────────────────── */
const PROJECTS = [
  {
    id: 1, name: "Lunar Commerce", tag: "E-Commerce",
    bg: "linear-gradient(135deg, #0f0514 0%, #1a0533 50%, #0a0a1f 100%)",
    accent: "#9B5CF6",
    mockBg: "#0D0118",
    elements: ["navbar", "hero", "products"],
  },
  {
    id: 2, name: "Meridian SaaS", tag: "Dashboard",
    bg: "linear-gradient(135deg, #020b18 0%, #041830 50%, #010d1f 100%)",
    accent: "#3B82F6",
    mockBg: "#050E1A",
    elements: ["stats", "chart", "table"],
  },
  {
    id: 3, name: "Aura Agency", tag: "Portfolio",
    bg: "linear-gradient(135deg, #0f0a00 0%, #1f1400 50%, #100b00 100%)",
    accent: "#F59E0B",
    mockBg: "#100A00",
    elements: ["header", "grid", "footer"],
  },
  {
    id: 4, name: "Void Studio", tag: "Creative",
    bg: "linear-gradient(135deg, #000a0f 0%, #001a24 50%, #000d14 100%)",
    accent: "#06B6D4",
    mockBg: "#000D14",
    elements: ["logo", "showcase", "contact"],
  },
];

function MockWebsite({ project, isZoomed }) {
  const { accent, mockBg, elements, name } = project;

  const renderElement = (el) => {
    switch (el) {
      case "navbar": return (
        <div key={el} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", borderBottom: `1px solid ${accent}20` }}>
          <div style={{ width: 40, height: 6, borderRadius: 3, background: accent, opacity: 0.8 }} />
          <div style={{ display: "flex", gap: 6 }}>
            {[1, 2, 3].map(i => <div key={i} style={{ width: 20, height: 4, borderRadius: 2, background: "rgba(255,255,255,0.2)" }} />)}
          </div>
        </div>
      );
      case "hero": return (
        <div key={el} style={{ padding: "16px 12px", textAlign: "center" }}>
          <div style={{ width: "60%", height: 8, borderRadius: 4, background: "rgba(255,255,255,0.6)", margin: "0 auto 8px" }} />
          <div style={{ width: "80%", height: 5, borderRadius: 3, background: "rgba(255,255,255,0.2)", margin: "0 auto 4px" }} />
          <div style={{ width: "60%", height: 5, borderRadius: 3, background: "rgba(255,255,255,0.2)", margin: "0 auto 12px" }} />
          <div style={{ display: "inline-block", padding: "5px 14px", borderRadius: 6, background: accent, opacity: 0.9 }}>
            <div style={{ width: 30, height: 4, borderRadius: 2, background: "rgba(255,255,255,0.9)" }} />
          </div>
        </div>
      );
      case "products": return (
        <div key={el} style={{ padding: "8px 12px", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 6 }}>
          {[1, 2, 3].map(i => (
            <div key={i} style={{ borderRadius: 6, padding: 8, background: `${accent}15`, border: `1px solid ${accent}25` }}>
              <div style={{ height: 30, borderRadius: 4, background: `${accent}25`, marginBottom: 5 }} />
              <div style={{ height: 4, borderRadius: 2, background: "rgba(255,255,255,0.3)", marginBottom: 3 }} />
              <div style={{ height: 3, borderRadius: 2, background: "rgba(255,255,255,0.15)" }} />
            </div>
          ))}
        </div>
      );
      case "stats": return (
        <div key={el} style={{ padding: "8px 12px", display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 5 }}>
          {[1, 2, 3, 4].map(i => (
            <div key={i} style={{ padding: 7, borderRadius: 6, background: `${accent}12`, border: `1px solid ${accent}20` }}>
              <div style={{ width: "50%", height: 8, borderRadius: 3, background: accent, opacity: 0.7, marginBottom: 4 }} />
              <div style={{ height: 3, borderRadius: 2, background: "rgba(255,255,255,0.2)" }} />
            </div>
          ))}
        </div>
      );
      case "chart": return (
        <div key={el} style={{ padding: "8px 12px" }}>
          <div style={{ height: 55, borderRadius: 8, background: `${accent}10`, border: `1px solid ${accent}20`, padding: 8, display: "flex", alignItems: "flex-end", gap: 3 }}>
            {[40, 65, 45, 80, 55, 90, 70].map((h, i) => (
              <div key={i} style={{ flex: 1, height: `${h}%`, borderRadius: "2px 2px 0 0", background: `linear-gradient(to top, ${accent}, ${accent}60)` }} />
            ))}
          </div>
        </div>
      );
      case "table": return (
        <div key={el} style={{ padding: "0 12px 8px" }}>
          {[1, 2, 3].map(i => (
            <div key={i} style={{ display: "flex", gap: 6, padding: "5px 0", borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
              <div style={{ width: 16, height: 16, borderRadius: 50, background: `${accent}40` }} />
              <div style={{ flex: 1, height: 5, borderRadius: 2, background: "rgba(255,255,255,0.2)", marginTop: 5 }} />
              <div style={{ width: 20, height: 5, borderRadius: 2, background: `${accent}60`, marginTop: 5 }} />
            </div>
          ))}
        </div>
      );
      default: return (
        <div key={el} style={{ padding: "8px 12px" }}>
          <div style={{ height: 40, borderRadius: 8, background: `${accent}10`, border: `1px solid ${accent}15` }} />
        </div>
      );
    }
  };

  return (
    <div style={{
      width: "100%", height: "100%",
      background: mockBg,
      borderRadius: isZoomed ? 0 : 12,
      overflow: "hidden",
      display: "flex", flexDirection: "column",
      transition: "border-radius 0.5s ease",
    }}>
      {elements.map(renderElement)}
    </div>
  );
}

function ProjectCard({ project, onClick }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onClick={() => onClick(project)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        minWidth: 300,
        height: 220,
        borderRadius: 20,
        overflow: "hidden",
        cursor: "pointer",
        position: "relative",
        transform: hovered ? "scale(1.03) translateY(-4px)" : "scale(1)",
        transition: "transform 0.4s cubic-bezier(0.22, 1, 0.36, 1)",
        boxShadow: hovered
          ? `0 24px 60px rgba(0,0,0,0.6), 0 0 40px ${project.accent}30`
          : "0 8px 32px rgba(0,0,0,0.4)",
        border: `1px solid ${hovered ? project.accent + "50" : "rgba(255,255,255,0.06)"}`,
        background: project.bg,
        flexShrink: 0,
      }}
    >
      <MockWebsite project={project} isZoomed={false} />
      <div style={{
        position: "absolute", inset: 0,
        background: `linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 60%)`,
        display: "flex", flexDirection: "column", justifyContent: "flex-end",
        padding: 18,
        opacity: hovered ? 1 : 0.7,
        transition: "opacity 0.3s",
      }}>
        <div style={{ fontSize: 10, color: project.accent, textTransform: "uppercase", letterSpacing: "0.12em", marginBottom: 4, fontFamily: "var(--font-mono)" }}>
          {project.tag}
        </div>
        <div style={{ fontFamily: "var(--font-display)", fontSize: 18, fontWeight: 700 }}>{project.name}</div>
        {hovered && (
          <div style={{ fontSize: 12, color: "rgba(255,255,255,0.6)", marginTop: 4, fontFamily: "var(--font-mono)", animation: "fade-up 0.3s ease" }}>
            Click to explore →
          </div>
        )}
      </div>
    </div>
  );
}

function ProjectModal({ project, onClose }) {
  const [phase, setPhase] = useState("entering"); // entering | open | exiting

  useEffect(() => {
    setTimeout(() => setPhase("open"), 50);
    const onKey = (e) => { if (e.key === "Escape") handleClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const handleClose = () => {
    setPhase("exiting");
    setTimeout(onClose, 500);
  };

  const scale = phase === "open" ? 1 : phase === "entering" ? 1.3 : 0.9;
  const opacity = phase === "open" ? 1 : 0;

  return (
    <div
      onClick={handleClose}
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: `rgba(0,0,0,${phase === "open" ? 0.9 : 0})`,
        transition: "background 0.5s ease",
        display: "flex", alignItems: "center", justifyContent: "center",
        backdropFilter: `blur(${phase === "open" ? 20 : 0}px)`,
        WebkitBackdropFilter: `blur(${phase === "open" ? 20 : 0}px)`,
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          width: "90vw", maxWidth: 900,
          height: "75vh",
          borderRadius: 24,
          overflow: "hidden",
          transform: `scale(${scale})`,
          opacity,
          transition: "transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.5s ease",
          background: project.bg,
          border: `1px solid ${project.accent}40`,
          boxShadow: `0 0 100px ${project.accent}30, 0 40px 80px rgba(0,0,0,0.8)`,
          position: "relative",
        }}
      >
        {/* Top bar */}
        <div style={{
          position: "absolute", top: 0, left: 0, right: 0,
          padding: "16px 20px",
          display: "flex", justifyContent: "space-between", alignItems: "center",
          background: "rgba(0,0,0,0.4)",
          backdropFilter: "blur(8px)",
          borderBottom: `1px solid ${project.accent}20`,
          zIndex: 2,
        }}>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <div style={{ fontSize: 10, color: project.accent, textTransform: "uppercase", letterSpacing: "0.12em", fontFamily: "var(--font-mono)" }}>{project.tag}</div>
            <div style={{ color: "rgba(255,255,255,0.3)", fontSize: 10 }}>·</div>
            <div style={{ fontSize: 13, fontFamily: "var(--font-display)", fontWeight: 700 }}>{project.name}</div>
          </div>
          <button onClick={handleClose} style={{
            width: 32, height: 32, borderRadius: "50%",
            background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.1)",
            color: "rgba(255,255,255,0.6)", fontSize: 16, cursor: "pointer",
            display: "flex", alignItems: "center", justifyContent: "center",
            transition: "all 0.2s",
          }}>×</button>
        </div>
        <div style={{ paddingTop: 60, height: "100%", overflow: "auto" }}>
          <MockWebsite project={project} isZoomed />
        </div>
        <div style={{ position: "absolute", bottom: 20, right: 20, fontSize: 11, fontFamily: "var(--font-mono)", color: "rgba(255,255,255,0.3)" }}>
          ESC to close
        </div>
      </div>
    </div>
  );
}

function Showcase({ ref: refProp }) {
  const [activeProject, setActiveProject] = useState(null);
  const scrollRef = useRef(null);

  return (
    <section ref={refProp} style={{ padding: "120px 0", position: "relative" }}>
      <div style={{ padding: "0 60px", maxWidth: 1200, margin: "0 auto" }}>
        <div className="section-label">Work</div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: 48 }}>
          <h2 style={{ fontFamily: "var(--font-display)", fontSize: "clamp(32px, 5vw, 56px)", fontWeight: 700, letterSpacing: "-0.03em", lineHeight: 1.05 }}>
            Projects that<br /><span className="shimmer-text">speak louder.</span>
          </h2>
          <p style={{ fontSize: 14, color: "var(--text-dim)", maxWidth: 240, lineHeight: 1.6, textAlign: "right" }}>
            Click any project to explore it up close.
          </p>
        </div>
      </div>

      {/* Horizontal scroll */}
      <div ref={scrollRef} style={{
        display: "flex", gap: 20, padding: "12px 60px",
        overflowX: "auto", scrollbarWidth: "none",
        WebkitOverflowScrolling: "touch",
      }}>
        {PROJECTS.map(p => (
          <ProjectCard key={p.id} project={p} onClick={setActiveProject} />
        ))}
        {/* Ghost card */}
        <div style={{
          minWidth: 300, height: 220, borderRadius: 20, flexShrink: 0,
          border: "1px dashed rgba(139,92,246,0.2)",
          display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
          gap: 12, color: "var(--text-muted)", fontSize: 13,
        }}>
          <div style={{ fontSize: 32 }}>+</div>
          <div>Your project</div>
        </div>
      </div>

      {activeProject && (
        <ProjectModal project={activeProject} onClose={() => setActiveProject(null)} />
      )}
    </section>
  );
}

/* ─────────────────────────────────────────────
   SECTION 3 — INTERACTIVE REQUEST BUILDER
───────────────────────────────────────────── */
const TERMINAL_STEPS = [
  { key: "name", prompt: "What's your project name?", placeholder: "e.g. Lunar Shop", type: "text" },
  { key: "type", prompt: "What type of website do you need?", placeholder: "e.g. E-commerce, Portfolio, SaaS", type: "text" },
  { key: "description", prompt: "Tell us about your project.", placeholder: "Brief overview...", type: "text" },
  { key: "catalog", prompt: "Do you need a product catalog? [yes/no]", placeholder: "yes", type: "yesno" },
  { key: "admin", prompt: "Do you need an admin panel? [yes/no]", placeholder: "yes", type: "yesno" },
  { key: "telegram", prompt: "Telegram bot integration? [yes/no]", placeholder: "no", type: "yesno" },
];

function BlueprintPaper({ answers }) {
  const hasCatalog = answers.catalog?.toLowerCase().startsWith("y");
  const hasAdmin = answers.admin?.toLowerCase().startsWith("y");
  const hasTelegram = answers.telegram?.toLowerCase().startsWith("y");

  return (
    <div style={{
      width: "100%", height: "100%", minHeight: 380,
      background: "#FAFAF8",
      borderRadius: 16,
      padding: 28,
      position: "relative",
      overflow: "hidden",
      boxShadow: "0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.5)",
    }}>
      {/* Paper lines */}
      {Array.from({ length: 20 }).map((_, i) => (
        <div key={i} style={{
          position: "absolute", left: 0, right: 0,
          top: 28 + i * 24,
          height: 1,
          background: "rgba(139,92,246,0.08)",
        }} />
      ))}
      {/* Left margin */}
      <div style={{ position: "absolute", left: 52, top: 0, bottom: 0, width: 1, background: "rgba(255,100,100,0.2)" }} />

      <div style={{ position: "relative", zIndex: 1 }}>
        {/* Title */}
        {answers.name ? (
          <div style={{
            fontFamily: "'Syne', sans-serif", fontSize: 22, fontWeight: 800,
            color: "#1a1a2e", marginBottom: 6,
            animation: "fade-up 0.4s ease",
            paddingLeft: 28,
          }}>{answers.name}</div>
        ) : (
          <div style={{ paddingLeft: 28, fontSize: 13, color: "rgba(0,0,0,0.2)", fontFamily: "var(--font-mono)" }}>
            Project name will appear here...
          </div>
        )}

        {answers.type && (
          <div style={{
            paddingLeft: 28, fontSize: 11, fontFamily: "var(--font-mono)",
            color: "#8B5CF6", textTransform: "uppercase", letterSpacing: "0.1em",
            marginBottom: 16, animation: "fade-up 0.4s ease",
          }}>{answers.type}</div>
        )}

        {answers.description && (
          <div style={{
            paddingLeft: 28, fontSize: 12, color: "#444", lineHeight: 1.6,
            marginBottom: 16, animation: "fade-up 0.4s ease",
          }}>{answers.description}</div>
        )}

        {/* Feature blocks */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10, paddingLeft: 28 }}>
          {hasCatalog && (
            <div style={{
              padding: "10px 14px", borderRadius: 10,
              background: "rgba(139,92,246,0.08)",
              border: "1px solid rgba(139,92,246,0.2)",
              animation: "fade-up 0.4s ease",
            }}>
              <div style={{ fontSize: 11, fontWeight: 600, color: "#6D28D9", marginBottom: 6 }}>🛍 PRODUCT CATALOG</div>
              <div style={{ display: "flex", gap: 6 }}>
                {[1, 2, 3].map(i => (
                  <div key={i} style={{ flex: 1, height: 36, borderRadius: 6, background: "rgba(109,40,217,0.1)", border: "1px solid rgba(109,40,217,0.15)" }} />
                ))}
              </div>
            </div>
          )}

          {hasAdmin && (
            <div style={{
              padding: "10px 14px", borderRadius: 10,
              background: "rgba(59,130,246,0.08)",
              border: "1px solid rgba(59,130,246,0.2)",
              animation: "fade-up 0.4s ease",
            }}>
              <div style={{ fontSize: 11, fontWeight: 600, color: "#1D4ED8", marginBottom: 6 }}>⚙️ ADMIN DASHBOARD</div>
              <div style={{ display: "flex", gap: 4 }}>
                <div style={{ width: 50, background: "rgba(59,130,246,0.15)", borderRadius: 4, height: 28 }} />
                <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 4 }}>
                  {[1, 2].map(i => <div key={i} style={{ height: 10, borderRadius: 3, background: "rgba(59,130,246,0.1)" }} />)}
                </div>
              </div>
            </div>
          )}

          {hasTelegram && (
            <div style={{
              padding: "10px 14px", borderRadius: 10,
              background: "rgba(0,136,204,0.08)",
              border: "1px solid rgba(0,136,204,0.2)",
              animation: "fade-up 0.4s ease",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 18 }}>✈️</span>
                <div>
                  <div style={{ fontSize: 11, fontWeight: 600, color: "#0088CC" }}>TELEGRAM INTEGRATION</div>
                  <div style={{ fontSize: 10, color: "#666" }}>Bot automation · Notifications · Commands</div>
                </div>
              </div>
            </div>
          )}

          {!answers.name && !hasCatalog && !hasAdmin && !hasTelegram && (
            <div style={{ padding: "20px 0", textAlign: "center" }}>
              <div style={{ fontSize: 28, marginBottom: 8 }}>✏️</div>
              <div style={{ fontSize: 12, color: "rgba(0,0,0,0.3)", fontFamily: "var(--font-mono)" }}>
                Answer questions in the terminal<br />to build your blueprint
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Terminal({ onComplete }) {
  const [step, setStep] = useState(0);
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState("");
  const [answers, setAnswers] = useState({});
  const [isComplete, setIsComplete] = useState(false);
  const inputRef = useRef(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, [step]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [history]);

  const handleSubmit = () => {
    if (!input.trim() && step < TERMINAL_STEPS.length) return;
    const currentStep = TERMINAL_STEPS[step];
    const newAnswers = { ...answers, [currentStep.key]: input.trim() };
    setAnswers(newAnswers);
    setHistory(h => [...h,
      { type: "prompt", text: currentStep.prompt },
      { type: "answer", text: input.trim() || "—" },
    ]);
    setInput("");

    if (step < TERMINAL_STEPS.length - 1) {
      setStep(s => s + 1);
    } else {
      setHistory(h => [...h, { type: "system", text: "Blueprint complete. Ready to submit." }]);
      setIsComplete(true);
      onComplete && onComplete(newAnswers);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  const current = TERMINAL_STEPS[step];

  return (
    <div style={{
      background: "#0D0D0D",
      borderRadius: 16,
      overflow: "hidden",
      border: "1px solid rgba(255,255,255,0.08)",
      boxShadow: "0 20px 60px rgba(0,0,0,0.8)",
      height: "100%", minHeight: 380,
      display: "flex", flexDirection: "column",
    }}>
      {/* Title bar */}
      <div style={{
        display: "flex", alignItems: "center", gap: 8,
        padding: "12px 16px",
        background: "rgba(255,255,255,0.03)",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
      }}>
        {["#FF5F57", "#FEBC2E", "#28C840"].map((c, i) => (
          <div key={i} style={{ width: 12, height: 12, borderRadius: "50%", background: c, boxShadow: `0 0 6px ${c}60` }} />
        ))}
        <div style={{ flex: 1, textAlign: "center", fontSize: 11, color: "rgba(255,255,255,0.3)", fontFamily: "var(--font-mono)" }}>
          vexio — project-builder
        </div>
      </div>

      {/* Terminal content */}
      <div ref={scrollRef} style={{
        flex: 1, padding: "20px 20px 0",
        fontFamily: "var(--font-mono)", fontSize: 13, lineHeight: 1.8,
        overflowY: "auto",
      }}>
        {/* Welcome */}
        <div style={{ color: "#8B5CF6", marginBottom: 4 }}>
          <span style={{ color: "rgba(255,255,255,0.3)" }}>$ </span>
          vexio init project
        </div>
        <div style={{ color: "rgba(255,255,255,0.3)", marginBottom: 16, fontSize: 11 }}>
          ✦ Vexio Project Builder v2.4 — Type your answers and press Enter
        </div>

        {history.map((h, i) => (
          <div key={i} style={{
            marginBottom: 4,
            color: h.type === "prompt" ? "rgba(255,255,255,0.55)"
              : h.type === "answer" ? "#A78BFA"
              : "#4ADE80",
            fontSize: h.type === "system" ? 11 : 13,
          }}>
            {h.type === "prompt" && <span style={{ color: "rgba(255,255,255,0.25)" }}>&gt; </span>}
            {h.type === "answer" && <span style={{ color: "rgba(167,139,250,0.5)" }}>✓ </span>}
            {h.text}
          </div>
        ))}

        {/* Current prompt */}
        {!isComplete && (
          <>
            <div style={{ color: "rgba(255,255,255,0.55)", marginTop: 4 }}>
              <span style={{ color: "rgba(255,255,255,0.25)" }}>&gt; </span>
              {current.prompt}
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 4, marginTop: 2 }}>
              <span style={{ color: "var(--purple)" }}>$</span>
              <input
                ref={inputRef}
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKey}
                placeholder={current.placeholder}
                style={{
                  flex: 1, background: "transparent", border: "none", outline: "none",
                  color: "#fff", fontFamily: "var(--font-mono)", fontSize: 13,
                  caretColor: "#8B5CF6",
                }}
              />
              <div style={{
                width: 8, height: 16, background: "#8B5CF6",
                animation: "cursor-blink 1s step-end infinite",
                borderRadius: 1,
              }} />
            </div>
          </>
        )}

        {isComplete && (
          <div style={{ marginTop: 8, padding: "8px 0" }}>
            <span style={{ color: "#4ADE80" }}>✓ </span>
            <span style={{ color: "rgba(255,255,255,0.5)", fontSize: 12 }}>All fields complete. Submit when ready.</span>
          </div>
        )}
      </div>
      <div style={{ height: 20 }} />
    </div>
  );
}

function RequestBuilder({ onSubmit }) {
  const [answers, setAnswers] = useState({});
  const [isTerminalComplete, setIsTerminalComplete] = useState(false);

  return (
    <section style={{ padding: "80px 24px 120px", position: "relative" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          <div className="section-label" style={{ justifyContent: "center" }}>Request Builder</div>
          <h2 style={{ fontFamily: "var(--font-display)", fontSize: "clamp(28px, 4vw, 48px)", fontWeight: 700, letterSpacing: "-0.03em" }}>
            Build your project,<br /><span className="shimmer-text">right here.</span>
          </h2>
        </div>

        <div style={{
          display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, alignItems: "start",
          "@media(maxWidth:768px)": { gridTemplateColumns: "1fr" },
        }}>
          <Terminal onComplete={(a) => { setAnswers(a); setIsTerminalComplete(true); }} />
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <BlueprintPaper answers={answers} />
            {isTerminalComplete && (
              <button
                onClick={() => onSubmit(answers)}
                className="btn-primary"
                style={{ width: "100%", justifyContent: "center", fontSize: 16, padding: "16px 32px" }}
              >
                Submit Project ✦
              </button>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   SECTION 4 — SUBMISSION ANIMATION
───────────────────────────────────────────── */
function SubmissionCard({ answers, onReset }) {
  const [phase, setPhase] = useState("card"); // card | uploading | done
  const [progress, setProgress] = useState(0);
  const projectId = "VX-" + Math.floor(2000 + Math.random() * 999);

  useEffect(() => {
    const t1 = setTimeout(() => setPhase("uploading"), 800);
    const t2 = setTimeout(() => {
      let p = 0;
      const interval = setInterval(() => {
        p += Math.random() * 12 + 3;
        if (p >= 100) { p = 100; clearInterval(interval); setPhase("done"); }
        setProgress(Math.min(p, 100));
      }, 150);
    }, 1200);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);

  return (
    <section style={{
      minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center",
      padding: "80px 24px",
      background: "radial-gradient(ellipse 60% 50% at 50% 50%, rgba(139,92,246,0.08) 0%, transparent 70%)",
    }}>
      <div style={{
        maxWidth: 520, width: "100%",
        animation: "fade-up 0.6s ease",
      }}>
        {/* Project card */}
        <div className="glass-purple" style={{
          borderRadius: 24, padding: 40,
          boxShadow: "0 0 80px rgba(139,92,246,0.2), 0 24px 60px rgba(0,0,0,0.6)",
        }}>
          <div style={{ marginBottom: 32 }}>
            <div style={{ fontSize: 11, fontFamily: "var(--font-mono)", color: "var(--purple)", letterSpacing: "0.15em", marginBottom: 12 }}>
              ◉ PROJECT CREATED
            </div>
            <h3 style={{ fontFamily: "var(--font-display)", fontSize: 32, fontWeight: 800, marginBottom: 8 }}>
              {answers.name || "Your Project"}
            </h3>
            <div style={{ fontSize: 14, color: "var(--text-dim)" }}>{answers.type}</div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
            {[
              ["Status", "Received", "#4ADE80"],
              ["Project ID", projectId, "#A78BFA"],
              ["Response", "Within 24 hours", "#60A5FA"],
            ].map(([k, v, c]) => (
              <div key={k} style={{
                display: "flex", justifyContent: "space-between", alignItems: "center",
                padding: "12px 16px", borderRadius: 12,
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.06)",
              }}>
                <span style={{ fontSize: 13, color: "var(--text-dim)", fontFamily: "var(--font-mono)" }}>{k}</span>
                <span style={{ fontSize: 13, color: c, fontWeight: 500 }}>{v}</span>
              </div>
            ))}
          </div>

          {/* Features summary */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 32 }}>
            {answers.catalog?.toLowerCase().startsWith("y") && (
              <div style={{ padding: "5px 12px", borderRadius: 100, background: "rgba(139,92,246,0.15)", border: "1px solid rgba(139,92,246,0.25)", fontSize: 11, color: "var(--purple-bright)" }}>🛍 Catalog</div>
            )}
            {answers.admin?.toLowerCase().startsWith("y") && (
              <div style={{ padding: "5px 12px", borderRadius: 100, background: "rgba(59,130,246,0.15)", border: "1px solid rgba(59,130,246,0.25)", fontSize: 11, color: "#93C5FD" }}>⚙️ Admin Panel</div>
            )}
            {answers.telegram?.toLowerCase().startsWith("y") && (
              <div style={{ padding: "5px 12px", borderRadius: 100, background: "rgba(0,136,204,0.15)", border: "1px solid rgba(0,136,204,0.25)", fontSize: 11, color: "#7DD3FC" }}>✈️ Telegram</div>
            )}
          </div>

          {/* Progress */}
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>
            {phase === "card" && (
              <div style={{ color: "var(--text-muted)" }}>Preparing upload...</div>
            )}
            {phase === "uploading" && (
              <div>
                <div style={{ color: "var(--text-dim)", marginBottom: 8 }}>Uploading... {Math.floor(progress)}%</div>
                <div style={{ height: 6, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                  <div style={{
                    height: "100%", borderRadius: 3,
                    width: `${progress}%`,
                    background: "linear-gradient(90deg, #6D28D9, #A78BFA)",
                    transition: "width 0.2s ease",
                    boxShadow: "0 0 12px rgba(139,92,246,0.6)",
                  }} />
                </div>
                <div style={{ marginTop: 6, color: "rgba(255,255,255,0.2)" }}>
                  {"█".repeat(Math.floor(progress / 8))}{"░".repeat(12 - Math.floor(progress / 8))}
                </div>
              </div>
            )}
            {phase === "done" && (
              <div style={{ animation: "fade-up 0.5s ease" }}>
                <div style={{ color: "#4ADE80", fontSize: 16, fontWeight: 500, marginBottom: 8 }}>✓ Delivered</div>
                <div style={{ height: 6, borderRadius: 3, background: "rgba(74,222,128,0.2)", overflow: "hidden" }}>
                  <div style={{ height: "100%", width: "100%", borderRadius: 3, background: "linear-gradient(90deg, #16A34A, #4ADE80)", boxShadow: "0 0 12px rgba(74,222,128,0.4)" }} />
                </div>
                <div style={{ marginTop: 8, color: "rgba(255,255,255,0.25)" }}>████████████ 100%</div>
              </div>
            )}
          </div>
        </div>

        {phase === "done" && (
          <div style={{ textAlign: "center", marginTop: 24, animation: "fade-up 0.6s ease 0.3s both" }}>
            <p style={{ fontSize: 14, color: "var(--text-dim)", marginBottom: 20, lineHeight: 1.6 }}>
              We'll review your project brief and reach out within 24 hours.
            </p>
            <button onClick={onReset} style={{
              padding: "12px 28px", borderRadius: 12,
              background: "transparent", border: "1px solid var(--border)",
              color: "var(--text-dim)", fontSize: 14, fontFamily: "var(--font-body)",
              cursor: "pointer", transition: "all 0.3s",
            }}
              onMouseEnter={e => { e.target.style.borderColor = "rgba(139,92,246,0.4)"; e.target.style.color = "var(--text)"; }}
              onMouseLeave={e => { e.target.style.borderColor = "var(--border)"; e.target.style.color = "var(--text-dim)"; }}
            >
              Start a new project
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   NAV
───────────────────────────────────────────── */
function Nav() {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 60);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }, []);

  return (
    <nav style={{
      position: "fixed", top: 0, left: 0, right: 0, zIndex: 100,
      display: "flex", alignItems: "center", justifyContent: "space-between",
      padding: "0 40px",
      height: 64,
      background: scrolled ? "rgba(10,10,10,0.85)" : "transparent",
      backdropFilter: scrolled ? "blur(20px)" : "none",
      borderBottom: scrolled ? "1px solid rgba(255,255,255,0.05)" : "none",
      transition: "all 0.4s ease",
    }}>
      <div style={{ fontFamily: "var(--font-display)", fontSize: 22, fontWeight: 800, letterSpacing: "-0.03em" }}>
        VX<span style={{ color: "var(--purple)" }}>.</span>
      </div>
      <div style={{ display: "flex", gap: 32, alignItems: "center" }}>
        {["Work", "Services", "About"].map(link => (
          <a key={link} href="#" style={{
            fontSize: 14, color: "var(--text-dim)", textDecoration: "none",
            transition: "color 0.2s", fontWeight: 400,
          }}
            onMouseEnter={e => e.target.style.color = "var(--text)"}
            onMouseLeave={e => e.target.style.color = "var(--text-dim)"}
          >{link}</a>
        ))}
        <button className="btn-primary" style={{ padding: "9px 20px", fontSize: 13 }}>
          Contact
        </button>
      </div>
    </nav>
  );
}

/* ─────────────────────────────────────────────
   ROOT
───────────────────────────────────────────── */
export default function VexioLanding() {
  const [submitted, setSubmitted] = useState(false);
  const [submittedAnswers, setSubmittedAnswers] = useState(null);
  const showcaseRef = useRef(null);

  const scrollToShowcase = () => {
    showcaseRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = (answers) => {
    setSubmittedAnswers(answers);
    setSubmitted(true);
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
  };

  const handleReset = () => {
    setSubmitted(false);
    setSubmittedAnswers(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <>
      <style>{GLOBAL_CSS}</style>
      <div style={{ background: "var(--bg)", minHeight: "100vh" }}>
        <Nav />
        <Hero onViewProjects={scrollToShowcase} />

        <div ref={showcaseRef}>
          <Showcase />
        </div>

        {!submitted && <RequestBuilder onSubmit={handleSubmit} />}
        {submitted && <SubmissionCard answers={submittedAnswers} onReset={handleReset} />}

        {/* Footer */}
        <footer style={{
          borderTop: "1px solid var(--border)",
          padding: "40px 60px",
          display: "flex", justifyContent: "space-between", alignItems: "center",
          flexWrap: "wrap", gap: 16,
        }}>
          <div style={{ fontFamily: "var(--font-display)", fontSize: 18, fontWeight: 800 }}>
            VX<span style={{ color: "var(--purple)" }}>.</span>
          </div>
          <div style={{ fontSize: 13, color: "var(--text-muted)" }}>
            © 2024 Vexio Studio. Crafted with obsession.
          </div>
          <div style={{ display: "flex", gap: 24 }}>
            {["Twitter", "Behance", "Telegram"].map(s => (
              <a key={s} href="#" style={{ fontSize: 13, color: "var(--text-muted)", textDecoration: "none", transition: "color 0.2s" }}
                onMouseEnter={e => e.target.style.color = "var(--purple-bright)"}
                onMouseLeave={e => e.target.style.color = "var(--text-muted)"}
              >{s}</a>
            ))}
          </div>
        </footer>
      </div>
    </>
  );
}
