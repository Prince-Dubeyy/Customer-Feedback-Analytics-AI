import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Clock, ChevronRight, Trash2 } from 'lucide-react';
import { getMemories, resetData } from '../services/api';

export default function MemoryTimeline() {
  const [memories, setMemories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMemories();
  }, []);

  const handleReset = async () => {
    if (confirm("Are you sure you want to delete all hindsight memory? This cannot be undone.")) {
      setLoading(true);
      try {
        await resetData();
        await loadMemories();
      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    }
  };

  const loadMemories = async () => {
    try {
      const data = await getMemories();
      setMemories(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <header className="flex justify-between items-end">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Brain className="w-8 h-8 text-indigo-400" />
            <h1 className="text-3xl font-bold text-white">Hindsight Memory</h1>
          </div>
          <p className="text-muted-text">
            Watch as the AI agent <strong>Retains</strong> insights over time, <strong>Recalls</strong> past feedback, and <strong>Reflects</strong> on trends.
          </p>
        </div>
        <button 
          onClick={handleReset}
          className="flex items-center space-x-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 px-4 py-2 rounded-lg border border-rose-500/20 transition-all shadow-sm"
        >
          <Trash2 className="w-4 h-4" />
          <span className="font-medium text-sm">Reset Data</span>
        </button>
      </header>

      {memories.length === 0 ? (
        <div className="glass-panel p-12 text-center">
          <Brain className="w-12 h-12 text-slate-500 mx-auto mb-4 opacity-50" />
          <h3 className="text-xl font-medium text-slate-300">No memories formed yet.</h3>
          <p className="text-slate-500 mt-2">Upload feedback to start building the Hindsight timeline.</p>
        </div>
      ) : (
        <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-indigo-500/30 before:to-transparent">
          {memories.map((memory, index) => (
            <motion.div 
              key={memory.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active"
            >
              <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-dark-bg bg-indigo-500/20 text-indigo-400 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_10px_rgba(99,102,241,0.2)] z-10">
                <Clock className="w-4 h-4" />
              </div>
              
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-panel p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold uppercase text-indigo-400 tracking-wider">
                    Batch #{memory.batch_id}
                  </span>
                  <span className="text-xs text-slate-500">
                    {new Date(memory.created_at).toLocaleString()}
                  </span>
                </div>
                
                <p className="text-sm text-slate-300 leading-relaxed mb-4">
                  "{memory.summary}"
                </p>
                
                <div className="space-y-3 pt-4 border-t border-slate-700/50">
                  <div>
                    <span className="text-xs text-slate-500 uppercase font-semibold">Top Complaints</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {memory.top_complaints.map((c: string) => (
                        <span key={c} className="px-2 py-1 bg-rose-500/10 text-rose-400 text-xs rounded border border-rose-500/20">
                          {c}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <span className="text-xs text-slate-500 uppercase font-semibold">Top Requests</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {memory.top_requests.map((r: string) => (
                        <span key={r} className="px-2 py-1 bg-emerald-500/10 text-emerald-400 text-xs rounded border border-emerald-500/20">
                          {r}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
