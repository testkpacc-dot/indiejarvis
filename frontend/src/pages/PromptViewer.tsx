import { useEffect, useState } from "react";
import axios from "axios";

export default function PromptViewer() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const base = import.meta.env.VITE_PROMPT_BASE;

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get(`${base}/prompts`);
        // backend returns: { items: [] }
        setItems(res.data.items || []);
      } catch (err) {
        console.error(err);
        setError("Failed to load prompts");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [base]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Prompt Registry</h2>

      {loading && <div>Loading prompts…</div>}
      {error && <div className="text-red-500">{error}</div>}

      {items.map(p => (
        <div key={p.prompt_id} className="p-3 border bg-white rounded mb-2">
          <div className="font-medium">{p.prompt_id}</div>
        </div>
      ))}
    </div>
  );
}
