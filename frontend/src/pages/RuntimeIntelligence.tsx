import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Server, Cpu, DollarSign, Zap } from 'lucide-react';
import { getRoutingLogs } from '../services/api';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

export default function RuntimeIntelligence() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const data = await getRoutingLogs();
      setLogs(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin" />
      </div>
    );
  }

  const totalCost = logs.reduce((sum, log) => sum + log.estimated_cost, 0);
  const avgLatency = logs.length > 0 ? logs.reduce((sum, log) => sum + log.latency_ms, 0) / logs.length : 0;
  const fallbackCount = logs.filter(l => l.status.includes('fallback')).length;

  return (
    <div className="space-y-8">
      <header>
        <div className="flex items-center gap-3 mb-2">
          <Activity className="w-8 h-8 text-cyan-400" />
          <h1 className="text-3xl font-bold text-white">cascadeflow Runtime Intelligence</h1>
        </div>
        <p className="text-muted-text">
          Live audit trail of model routing, budget enforcement, and fallback mechanics.
        </p>
      </header>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-panel p-6 bg-gradient-to-br from-cyan-900/20 to-transparent">
          <div className="flex items-center gap-2 text-cyan-400 mb-2">
            <DollarSign className="w-5 h-5" />
            <h4 className="font-semibold">Total Cost</h4>
          </div>
          <span className="text-3xl font-bold text-white">${totalCost.toFixed(5)}</span>
        </div>
        <div className="glass-panel p-6 bg-gradient-to-br from-indigo-900/20 to-transparent">
          <div className="flex items-center gap-2 text-indigo-400 mb-2">
            <Zap className="w-5 h-5" />
            <h4 className="font-semibold">Avg Latency</h4>
          </div>
          <span className="text-3xl font-bold text-white">{avgLatency.toFixed(0)} ms</span>
        </div>
        <div className="glass-panel p-6 bg-gradient-to-br from-purple-900/20 to-transparent">
          <div className="flex items-center gap-2 text-purple-400 mb-2">
            <Cpu className="w-5 h-5" />
            <h4 className="font-semibold">Requests</h4>
          </div>
          <span className="text-3xl font-bold text-white">{logs.length}</span>
        </div>
        <div className="glass-panel p-6 bg-gradient-to-br from-rose-900/20 to-transparent">
          <div className="flex items-center gap-2 text-rose-400 mb-2">
            <Server className="w-5 h-5" />
            <h4 className="font-semibold">Fallbacks Executed</h4>
          </div>
          <span className="text-3xl font-bold text-white">{fallbackCount}</span>
        </div>
      </div>

      {/* Audit Trail Table */}
      <div className="glass-panel overflow-hidden">
        <div className="p-6 border-b border-dark-border bg-slate-800/50">
          <h3 className="text-lg font-semibold text-white">Routing Audit Trail</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs uppercase text-slate-400 bg-slate-900/50">
              <tr>
                <th className="px-6 py-4">Timestamp</th>
                <th className="px-6 py-4">Task Type</th>
                <th className="px-6 py-4">Model Selected</th>
                <th className="px-6 py-4">Reasoning</th>
                <th className="px-6 py-4">Latency</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, idx) => (
                <motion.tr 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  key={log.id} 
                  className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-slate-300">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-slate-700 text-slate-200 rounded text-xs border border-slate-600">
                      {log.prompt_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-medium text-cyan-400">
                    {log.model_selected}
                  </td>
                  <td className="px-6 py-4 text-slate-400 max-w-xs truncate" title={log.reason}>
                    {log.reason}
                  </td>
                  <td className="px-6 py-4 text-slate-300">
                    {log.latency_ms.toFixed(0)}ms
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 rounded text-xs border",
                      log.status === 'success' ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                      "bg-amber-500/10 text-amber-400 border-amber-500/20"
                    )}>
                      {log.status}
                    </span>
                  </td>
                </motion.tr>
              ))}
              {logs.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                    No routing logs generated yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
