import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis } from 'recharts';
import { MessageSquare, ThumbsUp, AlertTriangle, TrendingUp, Trash2, MinusCircle, Activity } from 'lucide-react';
import { getDashboardStats, resetData, getModelStats } from '../services/api';

const COLORS = ['#10b981', '#6366f1', '#ef4444'];

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [modelStats, setModelStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const handleReset = async () => {
    if (confirm("Are you sure you want to delete all feedback data? This cannot be undone.")) {
      setLoading(true);
      try {
        await resetData();
        await loadStats();
      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    }
  };

  const loadStats = async () => {
    try {
      const [data, mStats] = await Promise.all([
        getDashboardStats(),
        getModelStats()
      ]);
      setStats(data);
      setModelStats(mStats);
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

  const sentimentData = [
    { name: 'Positive', value: stats?.positive || 0 },
    { name: 'Neutral', value: stats?.neutral || 0 },
    { name: 'Negative', value: stats?.negative || 0 },
  ];

  const totalCalculated = (stats?.positive || 0) + (stats?.neutral || 0) + (stats?.negative || 0);
  const isReconciled = !stats || stats.total_feedback === 0 || stats.total_feedback === totalCalculated;

  if (!isReconciled) {
    return (
      <div className="flex h-full items-center justify-center pt-20">
        <div className="bg-rose-500/10 border border-rose-500/20 p-8 rounded-xl max-w-lg text-center">
          <AlertTriangle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Data Reconciliation Error</h2>
          <p className="text-slate-300">
            Sentiment counts do not match Total Feedback. <br/>
            (Total: {stats.total_feedback} vs Calculated: {totalCalculated})
          </p>
          <button onClick={handleReset} className="mt-6 bg-rose-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-rose-600 transition-colors">
            Reset Database
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard Overview</h1>
          <p className="text-muted-text mt-1">Real-time pulse of your product feedback.</p>
        </div>
        <button 
          onClick={handleReset}
          className="flex items-center space-x-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 px-4 py-2 rounded-lg border border-rose-500/20 transition-all shadow-sm"
        >
          <Trash2 className="w-4 h-4" />
          <span className="font-medium text-sm">Reset Data</span>
        </button>
      </header>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
        {[
          { label: 'Total Feedback', value: stats?.total_feedback, icon: MessageSquare, color: 'text-blue-400', bg: 'bg-blue-400/10' },
          { label: 'Positive Sentiment', value: stats?.positive, icon: ThumbsUp, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
          { label: 'Neutral Sentiment', value: stats?.neutral, icon: MinusCircle, color: 'text-slate-400', bg: 'bg-slate-400/10' },
          { label: 'Negative Sentiment', value: stats?.negative, icon: AlertTriangle, color: 'text-rose-400', bg: 'bg-rose-400/10' },
          { label: 'Trending Issues', value: stats?.trending_issues?.length || 0, icon: TrendingUp, color: 'text-amber-400', bg: 'bg-amber-400/10' },
        ].map((stat, idx) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            key={stat.label} 
            className="glass-panel p-6 flex items-center justify-between"
          >
            <div>
              <p className="text-sm font-medium text-muted-text">{stat.label}</p>
              <h3 className="text-3xl font-bold text-white mt-1">{stat.value || 0}</h3>
            </div>
            <div className={`p-4 rounded-xl ${stat.bg}`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {/* Sentiment Chart */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="glass-panel p-6"
        >
          <h3 className="text-lg font-semibold text-white mb-6">Sentiment Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {sentimentData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ color: '#fff' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-col items-center gap-2 mt-4">
            <div className="flex justify-center gap-6">
              {sentimentData.map((s, idx) => (
                <div key={s.name} className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[idx] }} />
                  <span className="text-sm text-slate-300">
                    {s.name}: {s.value} ({stats?.total_feedback ? Math.round((s.value / stats.total_feedback) * 100) : 0}%)
                  </span>
                </div>
              ))}
            </div>
            <p className="text-xs text-slate-400 italic mt-2">
              Note: Total Feedback = Positive + Neutral + Negative
            </p>
          </div>
        </motion.div>

        {/* Top Complaints */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="glass-panel p-6"
        >
          <h3 className="text-lg font-semibold text-white mb-6">Top Complaints</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.top_complaints || []} layout="vertical" margin={{ left: 40 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                <Tooltip 
                  cursor={{ fill: '#334155', opacity: 0.4 }}
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                />
                <Bar dataKey="value" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={24}>
                  {
                    (stats?.top_complaints || []).map((_: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={index === 0 ? '#ef4444' : '#6366f1'} />
                    ))
                  }
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Model Performance Panel */}
      {modelStats && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="glass-panel p-6 mt-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <Activity className="w-6 h-6 text-indigo-400" />
            <h3 className="text-lg font-semibold text-white">AI Model Performance</h3>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { label: 'Accuracy', value: modelStats.accuracy },
              { label: 'Precision', value: modelStats.precision },
              { label: 'Recall', value: modelStats.recall },
              { label: 'F1 Score', value: modelStats.f1 },
            ].map((metric) => (
              <div key={metric.label} className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
                <p className="text-sm font-medium text-slate-400">{metric.label}</p>
                <div className="flex items-end gap-2 mt-1">
                  <h4 className="text-2xl font-bold text-white">
                    {typeof metric.value === 'number' ? (metric.value * 100).toFixed(1) : metric.value}
                  </h4>
                  {typeof metric.value === 'number' && <span className="text-sm text-slate-400 mb-1">%</span>}
                </div>
              </div>
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-4">
            * These metrics represent the underlying performance of the NLP sentiment classifier evaluated on unseen test data.
          </p>
        </motion.div>
      )}

    </div>
  );
}
