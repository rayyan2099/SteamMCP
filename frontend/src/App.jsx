import { useState } from "react";

const API_URL =
  import.meta.env.VITE_API_URL || "https://steammcp-s5qu.onrender.com";

const EXAMPLES = [
  "I want a dark difficult metroidvania for Mac",
  "I want a relaxing farming game with building",
  "I want games like Hollow Knight and Dark Souls",
];

async function getRecommendations(query) {
  const response = await fetch(`${API_URL}/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("The server returned an invalid response.");
  }

  if (!response.ok) {
    throw new Error(data.detail || `Request failed with status ${response.status}.`);
  }

  return data.recommendation;
}

function App() {
  const [query, setQuery] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedQuery = query.trim();
    if (!trimmedQuery || loading) return;

    setLoading(true);
    setError("");
    setRecommendation("");

    try {
      const result = await getRecommendations(trimmedQuery);
      setRecommendation(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function useExample(example) {
    setQuery(example);
    setError("");
  }

  return (
    <div className="app-shell">
      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">S</div>
          <div>
            <div className="brand-name">SteamMCP</div>
            <div className="brand-subtitle">AI game discovery</div>
          </div>
        </div>

        <a
          className="docs-link"
          href={`${API_URL}/docs`}
          target="_blank"
          rel="noreferrer"
        >
          API Docs ↗
        </a>
      </header>

      <main className="main-content">
        <section className="hero">
          <div className="eyebrow">Powered by Groq + MCP</div>
          <h1>
            Find your next
            <span> favorite game.</span>
          </h1>
          <p className="hero-copy">
            Describe the experience you want. SteamMCP chooses the right
            recommendation tools, understands your preferences, and returns
            curated Steam picks.
          </p>

          <form className="search-card" onSubmit={handleSubmit}>
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Try: I want a lonely atmospheric game to explore on Mac..."
              rows={4}
              maxLength={1000}
              disabled={loading}
            />

            <div className="search-footer">
              <span className="char-count">{query.length}/1000</span>
              <button
                type="submit"
                className="recommend-button"
                disabled={!query.trim() || loading}
              >
                {loading ? (
                  <>
                    <span className="spinner" />
                    Finding games...
                  </>
                ) : (
                  <>
                    Find games
                    <span className="button-arrow">→</span>
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="examples">
            <div className="examples-label">Try an example</div>
            <div className="example-list">
              {EXAMPLES.map((example) => (
                <button
                  className="example-chip"
                  key={example}
                  onClick={() => useExample(example)}
                  type="button"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </section>

        {error && (
          <section className="status-card error-card">
            <div className="status-icon">!</div>
            <div>
              <div className="status-title">Couldn't get recommendations</div>
              <div className="status-message">{error}</div>
            </div>
          </section>
        )}

        {loading && !recommendation && !error && (
          <section className="status-card loading-card">
            <div className="loading-animation">
              <span />
              <span />
              <span />
            </div>
            <div>
              <div className="status-title">SteamMCP is thinking…</div>
              <div className="status-message">
                Analyzing your request and selecting the best recommendation
                strategy.
              </div>
            </div>
          </section>
        )}

        {recommendation && (
          <section className="results-section">
            <div className="results-heading">
              <div>
                <div className="eyebrow">SteamMCP results</div>
                <h2>Recommendations</h2>
              </div>
              <button
                className="new-search-button"
                type="button"
                onClick={() => {
                  setRecommendation("");
                  setError("");
                }}
              >
                New search
              </button>
            </div>

            <div className="result-card">
              <div className="result-accent" />
              <div className="result-content">
                <pre>{recommendation}</pre>
              </div>
            </div>
          </section>
        )}

        <section className="how-it-works">
          <div className="eyebrow">How it works</div>
          <div className="steps">
            <article className="step">
              <div className="step-number">01</div>
              <h3>Describe what you want</h3>
              <p>
                Mention games, genres, mechanics, mood, platform, or just the
                vibe you're after.
              </p>
            </article>

            <article className="step">
              <div className="step-number">02</div>
              <h3>AI chooses the tools</h3>
              <p>
                The Groq-powered agent decides whether to use search,
                similarity, preference, or other MCP tools.
              </p>
            </article>

            <article className="step">
              <div className="step-number">03</div>
              <h3>Get curated picks</h3>
              <p>
                SteamMCP combines your request with its recommendation
                models and game metadata.
              </p>
            </article>
          </div>
        </section>
      </main>

      <footer className="footer">
        <span>SteamMCP</span>
        <span>AI-powered Steam game discovery</span>
      </footer>
    </div>
  );
}

export default App;
