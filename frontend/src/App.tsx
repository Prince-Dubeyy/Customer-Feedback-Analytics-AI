import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, UploadCloud, Brain, Activity, FileText, Menu, X } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import MemoryTimeline from './pages/MemoryTimeline';
import RuntimeIntelligence from './pages/RuntimeIntelligence';
import Reports from './pages/Reports';

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

function Sidebar({ isOpen, setIsOpen }: { isOpen: boolean, setIsOpen: (val: boolean) => void }) {
  const location = useLocation();
  
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Upload Feedback', path: '/upload', icon: UploadCloud },
    { name: 'Hindsight Memory', path: '/memory', icon: Brain },
    { name: 'cascadeflow Runtime', path: '/runtime', icon: Activity },
    { name: 'Executive Reports', path: '/reports', icon: FileText },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm" 
          onClick={() => setIsOpen(false)}
        />
      )}
      
      {/* Sidebar */}
      <div className={cn(
        "w-64 bg-dark-surface border-r border-dark-border flex flex-col h-screen fixed left-0 top-0 z-50 transition-transform duration-300 ease-in-out",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}>
        <div className="p-6 flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent tracking-tight">
              ProductPulse AI
            </h1>
            <p className="text-xs text-muted-text mt-1">Memory-Powered Intelligence</p>
          </div>
          <button 
            onClick={() => setIsOpen(false)} 
            className="md:hidden text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <nav className="flex-1 px-4 space-y-2 mt-4 overflow-y-auto custom-scrollbar">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.name}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={cn(
                  "flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200",
                  isActive 
                    ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.1)]" 
                    : "text-muted-text hover:bg-white/5 hover:text-white"
                )}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.name}</span>
              </Link>
            )
          })}
        </nav>
        
        <div className="p-4 m-4 rounded-xl bg-gradient-to-br from-indigo-900/50 to-cyan-900/50 border border-indigo-500/20 shrink-0">
          <div className="flex items-center space-x-2 text-indigo-300 mb-2">
            <Activity className="w-4 h-4 animate-pulse" />
            <span className="text-xs font-semibold uppercase tracking-wider">System Status</span>
          </div>
          <p className="text-sm text-slate-300">All AI modules online.</p>
        </div>
      </div>
    </>
  );
}

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <Router>
      <div className="flex min-h-screen bg-dark-bg text-light-text font-sans selection:bg-indigo-500/30">
        <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />
        
        <main className="flex-1 md:ml-64 min-h-screen flex flex-col relative w-full overflow-x-hidden">
          {/* Mobile Header */}
          <div className="md:hidden p-4 flex items-center bg-dark-surface border-b border-dark-border z-30 sticky top-0 shadow-lg">
            <button 
              onClick={() => setIsSidebarOpen(true)} 
              className="text-slate-400 hover:text-white mr-4 transition-colors"
            >
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-lg font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent tracking-tight truncate">
              ProductPulse AI
            </h1>
          </div>

          <div className="p-4 md:p-8 flex-1 overflow-y-auto custom-scrollbar relative">
            <div className="absolute top-0 left-0 w-full h-96 bg-indigo-600/10 rounded-full blur-[120px] -z-10 pointer-events-none mix-blend-screen opacity-50 translate-y-[-50%]" />
            <div className="max-w-7xl mx-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/upload" element={<Upload />} />
                <Route path="/memory" element={<MemoryTimeline />} />
                <Route path="/runtime" element={<RuntimeIntelligence />} />
                <Route path="/reports" element={<Reports />} />
              </Routes>
            </div>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App;
