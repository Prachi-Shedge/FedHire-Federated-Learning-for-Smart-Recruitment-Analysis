import { useState, useEffect, useRef } from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  LineChart,
  Line,
  CartesianGrid,
} from "recharts";

const API = "http://localhost:8000";

// ── Animated counter hook ─────────────────────────────────
function useCounter(target, duration = 1200) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        setValue(target);
        clearInterval(timer);
      } else setValue(Math.floor(start * 100) / 100);
    }, 16);
    return () => clearInterval(timer);
  }, [target]);
  return value;
}

// ── Hire Probability Gauge ────────────────────────────────
function GaugeMeter({ probability }) {
  const pct = Math.round(probability * 100);
  const angle = -135 + (pct / 100) * 270;
  const color = pct < 40 ? "#ff4d4d" : pct < 70 ? "#ffa500" : "#00e5a0";
  const animated = useCounter(pct);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 8,
      }}
    >
      <svg width="220" height="140" viewBox="0 0 220 140">
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ff4d4d" />
            <stop offset="50%" stopColor="#ffa500" />
            <stop offset="100%" stopColor="#00e5a0" />
          </linearGradient>
        </defs>
        {/* Track */}
        <path
          d="M 20 120 A 90 90 0 1 1 200 120"
          fill="none"
          stroke="#1a2035"
          strokeWidth="16"
          strokeLinecap="round"
        />
        {/* Fill */}
        <path
          d="M 20 120 A 90 90 0 1 1 200 120"
          fill="none"
          stroke="url(#gaugeGrad)"
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray={`${(pct / 100) * 283} 283`}
        />
        {/* Needle */}
        <g transform={`rotate(${angle}, 110, 120)`}>
          <line
            x1="110"
            y1="120"
            x2="110"
            y2="42"
            stroke={color}
            strokeWidth="3"
            strokeLinecap="round"
          />
          <circle cx="110" cy="120" r="8" fill={color} />
        </g>
        <text
          x="110"
          y="108"
          textAnchor="middle"
          fill={color}
          fontSize="28"
          fontWeight="900"
          fontFamily="'DM Mono', monospace"
        >
          {animated}%
        </text>
      </svg>
      <span
        style={{
          color: color,
          fontFamily: "'DM Mono', monospace",
          fontSize: 13,
          letterSpacing: 2,
        }}
      >
        {pct < 40 ? "LOW MATCH" : pct < 70 ? "MODERATE MATCH" : "STRONG MATCH"}
      </span>
    </div>
  );
}

// ── Skill Tag ─────────────────────────────────────────────
function SkillTag({ skill, type }) {
  const colors = {
    found: { bg: "rgba(0,229,160,0.12)", border: "#00e5a0", text: "#00e5a0" },
    missing: { bg: "rgba(255,77,77,0.12)", border: "#ff4d4d", text: "#ff4d4d" },
    trending: {
      bg: "rgba(255,165,0,0.12)",
      border: "#ffa500",
      text: "#ffa500",
    },
  };
  const c = colors[type];
  return (
    <span
      style={{
        background: c.bg,
        border: `1px solid ${c.border}`,
        color: c.text,
        padding: "3px 10px",
        borderRadius: 20,
        fontSize: 12,
        fontFamily: "'DM Mono', monospace",
        letterSpacing: 1,
        display: "inline-block",
        margin: 3,
      }}
    >
      {skill}
    </span>
  );
}

// ── News Ticker ───────────────────────────────────────────
function NewsTicker() {
  const FALLBACK = [
    "🔥 LangChain v0.3 released — agents now 40% faster",
    "📈 MLOps engineer roles up 67% YoY on LinkedIn",
    "🌐 Microsoft integrates Copilot into Azure DevOps",
    "⚡ PyTorch 2.4 — 2x faster training on consumer GPUs",
    "🚀 Vector databases become standard in GenAI stack",
  ];
  const [headlines, setHeadlines] = useState(FALLBACK);
  const [idx, setIdx] = useState(0);
  const [fade, setFade] = useState(true);

  // Fetch live news from backend, refresh every 10 minutes
  useEffect(() => {
    async function fetchNews() {
      try {
        const res = await fetch(`${API}/news?limit=12`);
        const data = await res.json();
        if (data.news?.length) {
          setHeadlines(data.news.map((n) => `🌐 ${n.title}`));
          setIdx(0);
        }
      } catch {
        // keep fallback silently
      }
    }
    fetchNews();
    const refresh = setInterval(fetchNews, 10 * 60 * 1000);
    return () => clearInterval(refresh);
  }, []);

  // Rotate headline every 4 seconds
  useEffect(() => {
    const t = setInterval(() => {
      setFade(false);
      setTimeout(() => {
        setIdx((i) => (i + 1) % headlines.length);
        setFade(true);
      }, 400);
    }, 4000);
    return () => clearInterval(t);
  }, [headlines]);

  return (
    <div
      style={{
        background: "rgba(255,165,0,0.06)",
        border: "1px solid rgba(255,165,0,0.25)",
        borderRadius: 10,
        padding: "10px 18px",
        marginBottom: 24,
        display: "flex",
        alignItems: "center",
        gap: 12,
      }}
    >
      <span
        style={{
          color: "#ffa500",
          fontFamily: "'DM Mono',monospace",
          fontSize: 11,
          letterSpacing: 2,
          whiteSpace: "nowrap",
        }}
      >
        LIVE IT NEWS
      </span>
      <div
        style={{ width: 1, height: 16, background: "rgba(255,165,0,0.3)" }}
      />
      <span
        style={{
          color: "#c8d0e0",
          fontSize: 13,
          fontFamily: "'Inter',sans-serif",
          transition: "opacity 0.4s",
          opacity: fade ? 1 : 0,
        }}
      >
        {headlines[idx]}
      </span>
    </div>
  );
}

// ── Live News Card (Trends Tab) ───────────────────────────
function LiveNewsCard() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetchedAt, setFetchedAt] = useState(null);

  useEffect(() => {
    async function fetchNews() {
      setLoading(true);
      try {
        const res = await fetch(`${API}/news?limit=10`);
        const data = await res.json();
        if (data.news?.length) {
          setArticles(data.news);
          setFetchedAt(data.fetched_at);
        }
      } catch {
        setArticles([]);
      } finally {
        setLoading(false);
      }
    }
    fetchNews();
    const refresh = setInterval(fetchNews, 10 * 60 * 1000);
    return () => clearInterval(refresh);
  }, []);

  const ICONS = ["🤖", "📈", "⚡", "🔬", "💼", "🚀", "🌐", "🏆", "🔥", "📊"];

  return (
    <div
      style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: 16,
        padding: 24,
        marginBottom: 20,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 16,
        }}
      >
        <div
          style={{
            fontSize: 12,
            fontFamily: "'DM Mono',monospace",
            letterSpacing: 2,
            color: "#5a6478",
            textTransform: "uppercase",
          }}
        >
          🌐 LIVE IT & TECH NEWS
        </div>
        {fetchedAt && (
          <div
            style={{
              fontSize: 10,
              color: "#3a4a60",
              fontFamily: "'DM Mono',monospace",
            }}
          >
            UPDATED {new Date(fetchedAt).toLocaleTimeString()}
          </div>
        )}
      </div>

      {loading ? (
        <div
          style={{
            textAlign: "center",
            padding: "24px 0",
            color: "#3a4a60",
            fontFamily: "'DM Mono',monospace",
            fontSize: 12,
            letterSpacing: 2,
          }}
        >
          ⏳ FETCHING LIVE NEWS...
        </div>
      ) : articles.length === 0 ? (
        <div
          style={{
            textAlign: "center",
            padding: "24px 0",
            color: "#3a4a60",
            fontFamily: "'DM Mono',monospace",
            fontSize: 12,
          }}
        >
          ⚠️ Could not load news — backend may be offline
        </div>
      ) : (
        articles.map((article, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              gap: 14,
              alignItems: "flex-start",
              padding: "12px 0",
              borderBottom: "1px solid rgba(255,255,255,0.04)",
            }}
          >
            <span style={{ fontSize: 20 }}>{ICONS[i % ICONS.length]}</span>
            <div style={{ flex: 1 }}>
              <a
                href={article.link}
                target="_blank"
                rel="noreferrer"
                style={{
                  fontSize: 13,
                  color: "#c8d0e0",
                  lineHeight: 1.5,
                  textDecoration: "none",
                  cursor: "pointer",
                }}
                onMouseEnter={(e) => (e.target.style.color = "#6fb3ff")}
                onMouseLeave={(e) => (e.target.style.color = "#c8d0e0")}
              >
                {article.title}
              </a>
              <div
                style={{
                  fontSize: 11,
                  color: "#3a4a60",
                  fontFamily: "'DM Mono',monospace",
                  marginTop: 4,
                }}
              >
                {article.source}
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────
export default function Dashboard() {
  const [resumeText, setResumeText] = useState("");
  const [targetRole, setTargetRole] = useState("Data Scientist");
  const [result, setResult] = useState(null);
  const [flData, setFlData] = useState([]);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("analyze");
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    fetch(`${API}/fl-progress`)
      .then((r) => r.json())
      .then((d) => {
        if (d.rounds)
          setFlData(
            d.rounds.map((r) => ({
              round: `R${r.round}`,
              accuracy: Math.round(r.avg_accuracy * 100),
            })),
          );
      })
      .catch(() => {});
    fetch(`${API}/trends`)
      .then((r) => r.json())
      .then((d) => {
        if (d.trending_skills)
          setTrends(
            d.trending_skills.map((s, i) => ({ skill: s, demand: 95 - i * 8 })),
          );
      })
      .catch(() => {});
    fetch(`${API}/roles`)
      .then((r) => r.json())
      .then((d) => {
        if (d.roles) setRoles(d.roles);
      })
      .catch(() => {});
  }, []);

  async function analyze() {
    if (!resumeText.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_text: resumeText,
          target_role: targetRole,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
      setActiveTab("results");
    } catch (e) {
      setError(
        "Cannot connect to API. Make sure backend is running at localhost:8000",
      );
    } finally {
      setLoading(false);
    }
  }

  // Build radar data from result
  const radarData = result
    ? [
        {
          skill: "AI/ML",
          score: result.skills_by_category.ai_ml?.length * 20 || 0,
        },
        {
          skill: "Data Eng",
          score: result.skills_by_category.data_engineering?.length * 20 || 0,
        },
        {
          skill: "Cloud",
          score: result.skills_by_category.cloud_devops?.length * 20 || 0,
        },
        {
          skill: "Languages",
          score:
            result.skills_by_category.programming_languages?.length * 20 || 0,
        },
        {
          skill: "Frameworks",
          score:
            result.skills_by_category.frameworks_libraries?.length * 20 || 0,
        },
        {
          skill: "Soft Skills",
          score: result.skills_by_category.soft_skills?.length * 20 || 0,
        },
      ]
    : [];

  const styles = {
    app: {
      minHeight: "100vh",
      background: "#0a0f1e",
      fontFamily: "'Inter', sans-serif",
      color: "#c8d0e0",
      backgroundImage:
        "radial-gradient(ellipse at 20% 20%, rgba(0,100,255,0.06) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(0,229,160,0.04) 0%, transparent 50%)",
    },
    header: {
      borderBottom: "1px solid rgba(255,255,255,0.06)",
      padding: "18px 40px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      background: "rgba(10,15,30,0.95)",
      backdropFilter: "blur(20px)",
      position: "sticky",
      top: 0,
      zIndex: 100,
    },
    logo: { display: "flex", alignItems: "center", gap: 12 },
    logoIcon: {
      width: 36,
      height: 36,
      borderRadius: 10,
      background: "linear-gradient(135deg,#0064ff,#00e5a0)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 18,
    },
    logoText: {
      fontFamily: "'DM Mono',monospace",
      fontSize: 15,
      fontWeight: 700,
      color: "#fff",
      letterSpacing: 1,
    },
    badge: {
      background: "rgba(0,229,160,0.1)",
      border: "1px solid rgba(0,229,160,0.3)",
      color: "#00e5a0",
      padding: "4px 12px",
      borderRadius: 20,
      fontSize: 11,
      fontFamily: "'DM Mono',monospace",
      letterSpacing: 1,
    },
    main: { maxWidth: 1200, margin: "0 auto", padding: "32px 40px" },
    tabs: {
      display: "flex",
      gap: 4,
      marginBottom: 28,
      background: "rgba(255,255,255,0.03)",
      borderRadius: 12,
      padding: 4,
      width: "fit-content",
    },
    tab: (active) => ({
      padding: "8px 20px",
      borderRadius: 9,
      fontSize: 13,
      cursor: "pointer",
      border: "none",
      fontFamily: "'DM Mono',monospace",
      letterSpacing: 1,
      transition: "all 0.2s",
      background: active ? "rgba(0,100,255,0.25)" : "transparent",
      color: active ? "#6fb3ff" : "#5a6478",
      borderBottom: active ? "1px solid #0064ff" : "1px solid transparent",
    }),
    card: {
      background: "rgba(255,255,255,0.03)",
      border: "1px solid rgba(255,255,255,0.07)",
      borderRadius: 16,
      padding: 24,
      marginBottom: 20,
    },
    cardTitle: {
      fontSize: 12,
      fontFamily: "'DM Mono',monospace",
      letterSpacing: 2,
      color: "#5a6478",
      marginBottom: 16,
      textTransform: "uppercase",
    },
    grid2: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 },
    grid3: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 20 },
    textarea: {
      width: "100%",
      minHeight: 160,
      background: "rgba(0,0,0,0.3)",
      border: "1px solid rgba(255,255,255,0.1)",
      borderRadius: 12,
      padding: 16,
      color: "#c8d0e0",
      fontSize: 14,
      fontFamily: "'Inter',sans-serif",
      resize: "vertical",
      outline: "none",
      boxSizing: "border-box",
      lineHeight: 1.7,
    },
    select: {
      background: "rgba(0,0,0,0.4)",
      border: "1px solid rgba(255,255,255,0.1)",
      borderRadius: 10,
      padding: "10px 16px",
      color: "#c8d0e0",
      fontSize: 13,
      fontFamily: "'DM Mono',monospace",
      outline: "none",
      cursor: "pointer",
      width: "100%",
    },
    btn: {
      background: "linear-gradient(135deg,#0064ff,#0040cc)",
      color: "#fff",
      border: "none",
      borderRadius: 12,
      padding: "12px 32px",
      fontSize: 14,
      fontFamily: "'DM Mono',monospace",
      letterSpacing: 1,
      cursor: "pointer",
      transition: "all 0.2s",
      fontWeight: 600,
    },
    statCard: (color) => ({
      background: `rgba(${color},0.06)`,
      border: `1px solid rgba(${color},0.2)`,
      borderRadius: 14,
      padding: "18px 20px",
    }),
    statNum: (color) => ({
      fontSize: 32,
      fontWeight: 900,
      fontFamily: "'DM Mono',monospace",
      color: `rgb(${color})`,
    }),
    statLabel: {
      fontSize: 11,
      color: "#5a6478",
      letterSpacing: 2,
      fontFamily: "'DM Mono',monospace",
      marginTop: 4,
    },
    recItem: {
      background: "rgba(0,100,255,0.06)",
      border: "1px solid rgba(0,100,255,0.15)",
      borderRadius: 10,
      padding: "10px 16px",
      marginBottom: 8,
      fontSize: 13,
      color: "#9bb0d0",
      lineHeight: 1.6,
    },
  };

  return (
    <div style={styles.app}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>🎓</div>
          <div>
            <div style={styles.logoText}>SKILLSYNC FL</div>
            <div
              style={{
                fontSize: 10,
                color: "#3a4a60",
                fontFamily: "'DM Mono',monospace",
                letterSpacing: 1,
              }}
            >
              FEDERATED SKILL ANALYZER
            </div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span style={styles.badge}>● FL ACTIVE</span>
          <span
            style={{
              fontSize: 11,
              color: "#3a4a60",
              fontFamily: "'DM Mono',monospace",
            }}
          >
            81 SKILLS TRACKED
          </span>
        </div>
      </header>

      <main style={styles.main}>
        <NewsTicker />

        {/* Tabs */}
        <div style={styles.tabs}>
          {["analyze", "results", "fl-progress", "trends"].map((t) => (
            <button
              key={t}
              style={styles.tab(activeTab === t)}
              onClick={() => setActiveTab(t)}
            >
              {t === "analyze"
                ? "📝 ANALYZE"
                : t === "results"
                  ? "📊 RESULTS"
                  : t === "fl-progress"
                    ? "🔄 FL PROGRESS"
                    : "🔥 TRENDS"}
            </button>
          ))}
        </div>

        {/* ── ANALYZE TAB ── */}
        {activeTab === "analyze" && (
          <div>
            <div style={{ marginBottom: 12 }}>
              <div style={styles.cardTitle}>TARGET ROLE</div>
              <select
                style={styles.select}
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
              >
                {(roles.length
                  ? roles
                  : [
                      "Data Scientist",
                      "ML Engineer",
                      "Full Stack Developer",
                      "Data Engineer",
                      "GenAI Engineer",
                    ]
                ).map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </div>
            <div style={{ marginBottom: 16 }}>
              <div style={styles.cardTitle}>
                PASTE YOUR RESUME / SKILLS SUMMARY
              </div>
              <textarea
                style={styles.textarea}
                placeholder="Paste your resume text or skills summary here...&#10;&#10;Example: I am a final year student with experience in Python, machine learning, PyTorch, SQL and Docker..."
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
              />
            </div>
            {error && (
              <div
                style={{
                  color: "#ff4d4d",
                  fontSize: 13,
                  marginBottom: 12,
                  padding: "10px 16px",
                  background: "rgba(255,77,77,0.08)",
                  borderRadius: 10,
                  border: "1px solid rgba(255,77,77,0.2)",
                }}
              >
                ⚠️ {error}
              </div>
            )}
            <button style={styles.btn} onClick={analyze} disabled={loading}>
              {loading ? "⏳ ANALYZING..." : "⚡ ANALYZE SKILLS"}
            </button>
            <div style={{ marginTop: 32 }}>
              <div style={styles.cardTitle}>HOW IT WORKS</div>
              <div style={styles.grid3}>
                {[
                  [
                    "🔒",
                    "Privacy First",
                    "Your resume never leaves your device — only model weights are shared via Federated Learning",
                  ],
                  [
                    "🏢",
                    "5 Company Nodes",
                    "TCS, Infosys, Wipro, Startup & MNC trained our model on their hiring patterns",
                  ],
                  [
                    "🎯",
                    "Personalized",
                    "Get role-specific gaps, trending skill alerts & hire probability score",
                  ],
                ].map(([icon, title, desc]) => (
                  <div key={title} style={styles.card}>
                    <div style={{ fontSize: 28, marginBottom: 10 }}>{icon}</div>
                    <div
                      style={{
                        fontWeight: 700,
                        color: "#fff",
                        marginBottom: 6,
                        fontSize: 14,
                      }}
                    >
                      {title}
                    </div>
                    <div
                      style={{
                        fontSize: 12,
                        color: "#5a6478",
                        lineHeight: 1.7,
                      }}
                    >
                      {desc}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── RESULTS TAB ── */}
        {activeTab === "results" && result && (
          <div>
            {/* Stats Row */}
            <div style={styles.grid3}>
              <div style={styles.statCard("0,229,160")}>
                <div style={styles.statNum("0,229,160")}>
                  {result.extracted_skills.length}
                </div>
                <div style={styles.statLabel}>SKILLS DETECTED</div>
              </div>
              <div style={styles.statCard("255,77,77")}>
                <div style={styles.statNum("255,77,77")}>
                  {result.missing_skills.length}
                </div>
                <div style={styles.statLabel}>SKILLS MISSING</div>
              </div>
              <div style={styles.statCard("0,100,255")}>
                <div style={styles.statNum("0,100,255")}>
                  {result.match_percentage}%
                </div>
                <div style={styles.statLabel}>ROLE MATCH</div>
              </div>
            </div>

            <div style={styles.grid2}>
              {/* Gauge */}
              <div style={styles.card}>
                <div style={styles.cardTitle}>HIRE PROBABILITY (FL MODEL)</div>
                <GaugeMeter probability={result.hire_probability} />
                <div
                  style={{
                    fontSize: 11,
                    color: "#3a4a60",
                    textAlign: "center",
                    marginTop: 8,
                    fontFamily: "'DM Mono',monospace",
                  }}
                >
                  PREDICTED BY FEDERATED GLOBAL MODEL
                </div>
              </div>

              {/* Radar */}
              <div style={styles.card}>
                <div style={styles.cardTitle}>SKILL CATEGORY COVERAGE</div>
                <ResponsiveContainer width="100%" height={220}>
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="rgba(255,255,255,0.08)" />
                    <PolarAngleAxis
                      dataKey="skill"
                      tick={{
                        fill: "#5a6478",
                        fontSize: 11,
                        fontFamily: "'DM Mono',monospace",
                      }}
                    />
                    <Radar
                      dataKey="score"
                      stroke="#0064ff"
                      fill="rgba(0,100,255,0.2)"
                      strokeWidth={2}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Skills */}
            <div style={styles.card}>
              <div style={styles.cardTitle}>SKILLS FOUND ✅</div>
              <div>
                {result.extracted_skills.map((s) => (
                  <SkillTag key={s} skill={s} type="found" />
                ))}
              </div>
            </div>

            <div style={styles.grid2}>
              <div style={styles.card}>
                <div style={styles.cardTitle}>MISSING FOR ROLE ❌</div>
                <div>
                  {result.missing_skills.length ? (
                    result.missing_skills.map((s) => (
                      <SkillTag key={s} skill={s} type="missing" />
                    ))
                  ) : (
                    <span style={{ color: "#00e5a0", fontSize: 13 }}>
                      ✅ You have all required skills!
                    </span>
                  )}
                </div>
              </div>
              <div style={styles.card}>
                <div style={styles.cardTitle}>TRENDING NOW 🔥</div>
                <div>
                  {result.trending_skills.map((s) => (
                    <SkillTag key={s} skill={s} type="trending" />
                  ))}
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div style={styles.card}>
              <div style={styles.cardTitle}>PERSONALIZED RECOMMENDATIONS</div>
              {result.recommendations.map((r, i) => (
                <div key={i} style={styles.recItem}>
                  → {r}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "results" && !result && (
          <div
            style={{ textAlign: "center", padding: "60px 0", color: "#3a4a60" }}
          >
            <div style={{ fontSize: 48, marginBottom: 16 }}>📊</div>
            <div
              style={{ fontFamily: "'DM Mono',monospace", letterSpacing: 2 }}
            >
              NO ANALYSIS YET — GO TO ANALYZE TAB
            </div>
          </div>
        )}

        {/* ── FL PROGRESS TAB ── */}
        {activeTab === "fl-progress" && (
          <div>
            <div style={styles.grid2}>
              <div style={styles.statCard("0,100,255")}>
                <div style={styles.statNum("0,100,255")}>{flData.length}</div>
                <div style={styles.statLabel}>FL ROUNDS COMPLETED</div>
              </div>
              <div style={styles.statCard("0,229,160")}>
                <div style={styles.statNum("0,229,160")}>
                  {flData.length ? flData[flData.length - 1].accuracy : 0}%
                </div>
                <div style={styles.statLabel}>FINAL GLOBAL ACCURACY</div>
              </div>
            </div>
            <div style={styles.card}>
              <div style={styles.cardTitle}>
                GLOBAL MODEL ACCURACY PER FL ROUND
              </div>
              {flData.length ? (
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={flData}>
                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="rgba(255,255,255,0.05)"
                    />
                    <XAxis
                      dataKey="round"
                      tick={{ fill: "#5a6478", fontSize: 11 }}
                    />
                    <YAxis
                      domain={[0, 100]}
                      tick={{ fill: "#5a6478", fontSize: 11 }}
                      tickFormatter={(v) => `${v}%`}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "#0d1526",
                        border: "1px solid rgba(0,100,255,0.3)",
                        borderRadius: 8,
                      }}
                      labelStyle={{ color: "#6fb3ff" }}
                      formatter={(v) => [`${v}%`, "Accuracy"]}
                    />
                    <Line
                      type="monotone"
                      dataKey="accuracy"
                      stroke="#0064ff"
                      strokeWidth={3}
                      dot={{ fill: "#00e5a0", strokeWidth: 2, r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div
                  style={{
                    textAlign: "center",
                    padding: "40px 0",
                    color: "#3a4a60",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "'DM Mono',monospace",
                      letterSpacing: 2,
                      fontSize: 13,
                    }}
                  >
                    RUN FL TRAINING FIRST
                  </div>
                  <div style={{ fontSize: 12, marginTop: 8 }}>
                    cd fl_server && python server.py
                  </div>
                </div>
              )}
            </div>
            <div style={styles.card}>
              <div style={styles.cardTitle}>HOW FL WORKS IN THIS PROJECT</div>
              <div
                style={{
                  display: "flex",
                  gap: 0,
                  alignItems: "center",
                  flexWrap: "wrap",
                }}
              >
                {[
                  "TCS Node",
                  "Product Node",
                  "Consulting Node",
                  "Startup Node",
                  "MNC Node",
                ].map((n, i) => (
                  <div
                    key={n}
                    style={{ display: "flex", alignItems: "center" }}
                  >
                    <div
                      style={{
                        background: "rgba(0,100,255,0.1)",
                        border: "1px solid rgba(0,100,255,0.25)",
                        borderRadius: 8,
                        padding: "8px 14px",
                        fontSize: 12,
                        fontFamily: "'DM Mono',monospace",
                        color: "#6fb3ff",
                      }}
                    >
                      {n}
                    </div>
                    {i < 4 && (
                      <div
                        style={{
                          color: "#3a4a60",
                          padding: "0 6px",
                          fontSize: 18,
                        }}
                      >
                        →
                      </div>
                    )}
                  </div>
                ))}
                <div
                  style={{ color: "#3a4a60", padding: "0 6px", fontSize: 18 }}
                >
                  →
                </div>
                <div
                  style={{
                    background: "rgba(0,229,160,0.1)",
                    border: "1px solid rgba(0,229,160,0.3)",
                    borderRadius: 8,
                    padding: "8px 14px",
                    fontSize: 12,
                    fontFamily: "'DM Mono',monospace",
                    color: "#00e5a0",
                  }}
                >
                  FL SERVER (FedAvg)
                </div>
                <div
                  style={{ color: "#3a4a60", padding: "0 6px", fontSize: 18 }}
                >
                  →
                </div>
                <div
                  style={{
                    background: "rgba(255,165,0,0.1)",
                    border: "1px solid rgba(255,165,0,0.3)",
                    borderRadius: 8,
                    padding: "8px 14px",
                    fontSize: 12,
                    fontFamily: "'DM Mono',monospace",
                    color: "#ffa500",
                  }}
                >
                  GLOBAL MODEL
                </div>
              </div>
              <div
                style={{
                  fontSize: 12,
                  color: "#3a4a60",
                  marginTop: 12,
                  fontFamily: "'DM Mono',monospace",
                }}
              >
                ✅ ZERO raw employee data shared between nodes — only model
                weights (≈50KB per round)
              </div>
            </div>
          </div>
        )}

        {/* ── TRENDS TAB ── */}
        {activeTab === "trends" && (
          <div>
            <div style={styles.card}>
              <div style={styles.cardTitle}>
                TOP TRENDING SKILLS — INDUSTRY DEMAND INDEX
              </div>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={trends} layout="vertical" margin={{ left: 20 }}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(255,255,255,0.04)"
                    horizontal={false}
                  />
                  <XAxis
                    type="number"
                    domain={[0, 100]}
                    tick={{ fill: "#5a6478", fontSize: 11 }}
                    tickFormatter={(v) => `${v}%`}
                  />
                  <YAxis
                    type="category"
                    dataKey="skill"
                    width={120}
                    tick={{
                      fill: "#9bb0d0",
                      fontSize: 12,
                      fontFamily: "'DM Mono',monospace",
                    }}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "#0d1526",
                      border: "1px solid rgba(0,229,160,0.3)",
                      borderRadius: 8,
                    }}
                    formatter={(v) => [`${v}%`, "Demand"]}
                  />
                  <Bar
                    dataKey="demand"
                    fill="url(#barGrad)"
                    radius={[0, 6, 6, 0]}
                  >
                    <defs>
                      <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#0064ff" />
                        <stop offset="100%" stopColor="#00e5a0" />
                      </linearGradient>
                    </defs>
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div style={styles.grid2}>
              {[
                {
                  title: "🚀 FASTEST GROWING",
                  skills: ["LangChain", "LLM Ops", "Vector DB", "Prompt Eng"],
                  color: "0,229,160",
                },
                {
                  title: "⚠️ DECLINING DEMAND",
                  skills: [
                    "Hadoop",
                    "Basic Tableau",
                    "Manual Testing",
                    "Legacy Java",
                  ],
                  color: "255,77,77",
                },
              ].map(({ title, skills, color }) => (
                <div key={title} style={styles.card}>
                  <div style={styles.cardTitle}>{title}</div>
                  {skills.map((s) => (
                    <div
                      key={s}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        padding: "8px 0",
                        borderBottom: "1px solid rgba(255,255,255,0.04)",
                      }}
                    >
                      <span style={{ fontSize: 13, color: "#9bb0d0" }}>
                        {s}
                      </span>
                      <span
                        style={{
                          fontSize: 11,
                          fontFamily: "'DM Mono',monospace",
                          color: `rgb(${color})`,
                        }}
                      >
                        {color === "0,229,160" ? "↑ RISING" : "↓ FALLING"}
                      </span>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            <LiveNewsCard />
          </div>
        )}
      </main>
    </div>
  );
}
