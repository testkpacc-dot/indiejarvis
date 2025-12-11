import { useEffect, useState } from "react";
import axios from "axios";
import type { Experience } from "../types/api";

export default function ExperienceLog() {
  const [items, setItems] = useState<Experience[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const base = import.meta.env.VITE_EXPERIENCE_BASE;

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get(`${base}/experiences`);
        // backend returns { items: [...] }
        setItems(res.data.items || []);
      } catch (err) {
        console.error(err);
        setError("Failed to load experiences");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [base]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Experience Log</h2>

      {loading && <div className="text-sm text-gray-500">Loading…</div>}
      {error && <div className="text-sm text-red-500">{error}</div>}

      {items.map(i => (
        <div key={i.id} className="p-3 border rounded bg-white mb-2">
          <div className="text-sm text-gray-700">ID: {i.id}</div>
          <div className="text-xs text-gray-500">{i.timestamp}</div>
          <div className="text-xs mt-1">Prompt: {i.prompt_id}</div>
        </div>
      ))}
    </div>
  );
}
