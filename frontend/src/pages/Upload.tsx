import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2, Info } from 'lucide-react';
import { uploadFeedback } from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setText(''); // Clear text if file is selected
    }
  };

  const handleUpload = async () => {
    if (!file && !text.trim()) {
      setError('Please provide a file or paste text feedback.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await uploadFeedback(file || undefined, text || undefined);
      navigate('/'); // Redirect to dashboard after processing
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload and process feedback.');
      setLoading(false); // Only set to false on error, success redirects away
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <header>
        <h1 className="text-3xl font-bold text-white">Ingest Feedback</h1>
        <p className="text-muted-text mt-2">Upload CSV batches or paste raw text. The cascadeflow engine will route analysis automatically.</p>
      </header>

      <AnimatePresence>
        {!loading && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, height: 0, overflow: 'hidden' }}
            className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-5 flex items-start gap-4"
          >
            <div className="bg-amber-500/20 p-2 rounded-lg shrink-0 mt-1">
              <Info className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <h3 className="text-amber-400 font-semibold mb-1 flex items-center gap-2">
                ⚠️ Demo Environment Notice
              </h3>
              <div className="text-amber-400/80 text-sm space-y-2">
                <p>This project is hosted using free cloud infrastructure for demonstration purposes.</p>
                <p>If the backend has been inactive, the first request may take up to <strong>30–60 seconds</strong> while the server initializes.</p>
                <p>Please wait momentarily after uploading your file. Once active, all subsequent requests will respond normally. Thank you for your patience.</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* File Upload */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel p-8 flex flex-col items-center justify-center text-center border-dashed border-2 border-slate-600 hover:border-indigo-500 transition-colors cursor-pointer relative"
        >
          <input 
            type="file" 
            accept=".csv,.txt"
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" 
            disabled={loading}
          />
          <div className="bg-indigo-500/10 p-4 rounded-full mb-4">
            <UploadCloud className="w-8 h-8 text-indigo-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">Upload CSV or TXT</h3>
          <p className="text-sm text-slate-400 mb-4">Drag & drop or click to browse</p>
          
          {file && (
            <div className="flex items-center gap-2 text-emerald-400 bg-emerald-400/10 px-4 py-2 rounded-full text-sm">
              <CheckCircle2 className="w-4 h-4" />
              <span>{file.name} ready</span>
            </div>
          )}
        </motion.div>

        {/* Manual Text */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel p-6 flex flex-col min-h-[300px]"
        >
          <div className="flex items-center gap-3 mb-4">
            <FileText className="w-5 h-5 text-cyan-400" />
            <h3 className="text-lg font-semibold text-white">Paste Raw Text</h3>
          </div>
          <textarea 
            value={text}
            onChange={(e) => { setText(e.target.value); setFile(null); }}
            placeholder="Paste multiple customer reviews or feedback here (one per line)..."
            className="flex-1 bg-dark-bg/50 border border-dark-border rounded-lg p-4 text-sm text-light-text focus:outline-none focus:ring-2 focus:ring-cyan-500/50 resize-none"
            disabled={loading}
          />
        </motion.div>
      </div>

      {error && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-rose-500/10 border border-rose-500/30 text-rose-400 p-4 rounded-lg flex items-center gap-3"
        >
          <AlertCircle className="w-5 h-5" />
          <p>{error}</p>
        </motion.div>
      )}

      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="flex flex-col items-end gap-4"
      >
        <button 
          onClick={handleUpload}
          disabled={loading || (!file && !text)}
          className="bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-400 hover:to-cyan-400 text-white font-semibold py-3 px-8 rounded-xl shadow-lg shadow-indigo-500/20 transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group w-full md:w-auto justify-center"
        >
          {loading && (
            <motion.div 
              className="absolute inset-0 bg-white/20"
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
            />
          )}
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing feedback...</span>
            </>
          ) : (
            'Analyze Feedback'
          )}
        </button>
        
        <AnimatePresence>
          {loading && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="text-indigo-300 text-sm flex flex-col items-end text-right mr-2"
            >
              <span className="flex items-center gap-2">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
                </span>
                If this is the first request, the backend may be waking up.
              </span>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
