import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, TrendingUp, AlertTriangle, Lightbulb } from 'lucide-react';
import { getReport } from '../services/api';

export default function Reports() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReport();
  }, []);

  const loadReport = async () => {
    try {
      const data = await getReport();
      setReport(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12 print:max-w-full print:bg-white print:text-black">
      <header className="flex justify-between items-end print:hidden">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-8 h-8 text-indigo-400" />
            <h1 className="text-3xl font-bold text-white">Executive Report</h1>
          </div>
          <p className="text-muted-text">Strategic recommendations synthesized from historical memory.</p>
        </div>
        
        <button 
          onClick={handleExportPDF}
          disabled={!report || report.report?.includes('Not enough data')}
          className="bg-dark-surface border border-dark-border hover:bg-slate-800 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50"
        >
          <Download className="w-4 h-4" />
          Export PDF
        </button>
      </header>

      {(!report || report.report?.includes('Not enough data')) ? (
        <div className="glass-panel p-12 text-center print:hidden">
          <FileText className="w-12 h-12 text-slate-500 mx-auto mb-4 opacity-50" />
          <h3 className="text-xl font-medium text-slate-300">Insufficient Data</h3>
          <p className="text-slate-500 mt-2">Upload more feedback batches to generate strategic executive reports.</p>
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel p-8 md:p-12 space-y-12 print:shadow-none print:border-none print:text-black print:bg-white"
        >
          {/* Header for PDF */}
          <div className="border-b border-slate-700/50 pb-6 print:border-slate-300">
            <h2 className="text-2xl font-bold text-white print:text-black">ProductPulse AI - Executive Summary</h2>
            <p className="text-slate-400 mt-2 print:text-slate-600">Generated on: {new Date().toLocaleDateString()}</p>
          </div>

          <section>
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-indigo-400 print:text-indigo-600" />
              <h3 className="text-xl font-semibold text-white print:text-black">Latest Insights</h3>
            </div>
            <p className="text-slate-300 leading-relaxed text-lg print:text-slate-800">
              {report.latest_insights}
            </p>
          </section>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <section className="bg-rose-500/5 p-6 rounded-xl border border-rose-500/10 print:border-rose-200 print:bg-rose-50">
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="w-5 h-5 text-rose-400 print:text-rose-600" />
                <h3 className="text-lg font-semibold text-white print:text-black">Key Risks & Complaints</h3>
              </div>
              <ul className="space-y-3">
                {(report.risks || []).map((risk: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-slate-300 print:text-slate-700">
                    <span className="text-rose-400 mt-1">•</span>
                    {risk}
                  </li>
                ))}
              </ul>
            </section>

            <section className="bg-emerald-500/5 p-6 rounded-xl border border-emerald-500/10 print:border-emerald-200 print:bg-emerald-50">
              <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="w-5 h-5 text-emerald-400 print:text-emerald-600" />
                <h3 className="text-lg font-semibold text-white print:text-black">Opportunities & Feature Requests</h3>
              </div>
              <ul className="space-y-3">
                {(report.opportunities || []).map((opp: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-slate-300 print:text-slate-700">
                    <span className="text-emerald-400 mt-1">•</span>
                    {opp}
                  </li>
                ))}
              </ul>
            </section>
          </div>
          
          <section className="pt-8 border-t border-slate-700/50 print:border-slate-300">
             <h3 className="text-lg font-semibold text-white mb-4 print:text-black">Strategic Recommendations</h3>
             <p className="text-slate-400 print:text-slate-600 italic">
               Based on the trajectory identified by Hindsight memory analysis, immediate engineering resources should be allocated to resolve the top recurring complaints to prevent churn, while product teams scope out the highest priority feature requests for the upcoming quarter.
             </p>
          </section>
        </motion.div>
      )}
    </div>
  );
}
