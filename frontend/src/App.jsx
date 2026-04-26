import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Activity, 
  Terminal, 
  AlertTriangle, 
  Zap, 
  Settings, 
  Database, 
  Users, 
  BarChart3,
  Clock,
  ExternalLink,
  ShieldAlert
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  AreaChart, 
  Area 
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

// Mock Data
const MOCK_ATTACKS = [
  { id: '1', ip: '192.168.1.105', path: '/login', method: 'POST', status: 200, time: '2 mins ago', score: 85, type: 'Brute Force' },
  { id: '2', ip: '45.12.98.22', path: '/db', method: 'POST', status: 200, time: '5 mins ago', score: 92, type: 'SQL Injection' },
  { id: '3', ip: '103.4.5.11', path: '/config', method: 'GET', status: 200, time: '12 mins ago', score: 45, type: 'Reconnaissance' },
  { id: '4', ip: '88.22.1.99', path: '/admin', method: 'GET', status: 403, time: '15 mins ago', score: 60, type: 'Auth Bypass' },
  { id: '5', ip: '210.55.44.3', path: '/login', method: 'POST', status: 200, time: '20 mins ago', score: 88, type: 'Brute Force' },
];

const CHART_DATA = [
  { name: '00:00', attacks: 12, threat: 40 },
  { name: '04:00', attacks: 18, threat: 55 },
  { name: '08:00', attacks: 45, threat: 80 },
  { name: '12:00', attacks: 30, threat: 65 },
  { name: '16:00', attacks: 60, threat: 90 },
  { name: '20:00', attacks: 40, threat: 75 },
  { name: '23:59', attacks: 25, threat: 50 },
];

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [attacks, setAttacks] = useState([]);
  const [summary, setSummary] = useState({
    total_requests: 0,
    threat_events: 0,
    avg_threat_score: 0,
    trap_hits: 0
  });

  const fetchData = async () => {
    try {
      const [attacksRes, summaryRes] = await Promise.all([
        fetch('http://localhost:8000/api/attacks').then(res => res.json()),
        fetch('http://localhost:8000/api/summary').then(res => res.json())
      ]);
      setAttacks(attacksRes);
      setSummary(summaryRes);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Polling every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen bg-cyber-bg text-gray-300 font-sans">
      <div className="absolute inset-0 bg-grid pointer-events-none opacity-20"></div>
      
      {/* Sidebar */}
      <nav className="w-64 border-r border-cyber-border bg-cyber-card/50 backdrop-blur-xl z-10 flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="p-2 bg-cyber-primary/20 rounded-lg">
            <ShieldAlert className="text-cyber-primary h-6 w-6" />
          </div>
          <span className="font-bold text-xl text-white tracking-tight">CypherTrap <span className="text-cyber-primary">AI</span></span>
        </div>

        <div className="flex-1 px-4 py-6 space-y-2">
          <SidebarItem icon={<BarChart3 size={20}/>} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <SidebarItem icon={<Activity size={20}/>} label="Live Feed" active={activeTab === 'feed'} onClick={() => setActiveTab('feed')} />
          <SidebarItem icon={<Users size={20}/>} label="Attacker Profiles" active={activeTab === 'attackers'} onClick={() => setActiveTab('attackers')} />
          <SidebarItem icon={<Database size={20}/>} label="Database Traps" active={activeTab === 'traps'} onClick={() => setActiveTab('traps')} />
          <SidebarItem icon={<Terminal size={20}/>} label="Raw Logs" active={activeTab === 'logs'} onClick={() => setActiveTab('logs')} />
        </div>

        <div className="p-4 border-t border-cyber-border">
          <SidebarItem icon={<Settings size={20}/>} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto z-10 relative">
        {/* Header */}
        <header className="h-20 border-b border-cyber-border flex items-center justify-between px-8 bg-cyber-card/30 backdrop-blur-md sticky top-0">
          <div>
            <h1 className="text-2xl">Security Overview</h1>
            <p className="text-sm text-gray-500">System Status: <span className="text-cyber-success">Online & Monitoring</span></p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-cyber-bg border border-cyber-border rounded-full text-sm">
              <div className="w-2 h-2 rounded-full bg-cyber-success animate-pulse"></div>
              Live Monitoring
            </div>
            <button className="cyber-button">Generate Report</button>
          </div>
        </header>

        <div className="p-8 space-y-8">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard icon={<Zap className="text-cyber-primary" />} label="Total Requests" value={summary.total_requests} change="+12%" />
            <StatCard icon={<AlertTriangle className="text-cyber-danger" />} label="Threat Events" value={summary.threat_events} change="+5%" />
            <StatCard icon={<Activity className="text-cyber-secondary" />} label="Avg. Threat Score" value={summary.avg_threat_score} change="-2%" />
            <StatCard icon={<Database className="text-cyber-success" />} label="Trap Hits" value={summary.trap_hits} change="+24%" />
          </div>


          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="glass-card p-6">
              <h3 className="mb-6 flex items-center gap-2">
                <Activity size={18} className="text-cyber-primary" />
                Attack Frequency (24h)
              </h3>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={CHART_DATA}>
                    <defs>
                      <linearGradient id="colorAttacks" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#00f2ff" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#00f2ff" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
                    <XAxis dataKey="name" stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0d1117', border: '1px solid #30363d', borderRadius: '8px' }}
                      itemStyle={{ color: '#00f2ff' }}
                    />
                    <Area type="monotone" dataKey="attacks" stroke="#00f2ff" fillOpacity={1} fill="url(#colorAttacks)" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="glass-card p-6">
              <h3 className="mb-6 flex items-center gap-2">
                <Shield size={18} className="text-cyber-secondary" />
                Threat Level Distribution
              </h3>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={CHART_DATA}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
                    <XAxis dataKey="name" stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0d1117', border: '1px solid #30363d', borderRadius: '8px' }}
                    />
                    <Line type="monotone" dataKey="threat" stroke="#7000ff" strokeWidth={3} dot={{ fill: '#7000ff', strokeWidth: 2 }} activeDot={{ r: 8 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Recent Attacks Table */}
          <div className="glass-card">
            <div className="p-6 border-b border-cyber-border flex justify-between items-center">
              <h3 className="flex items-center gap-2">
                <Terminal size={18} className="text-cyber-warning" />
                Live Deception Feed
              </h3>
              <button className="text-cyber-primary text-sm hover:underline flex items-center gap-1">
                View All Logs <ExternalLink size={14} />
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="bg-cyber-bg/50 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    <th className="px-6 py-4">Attacker IP</th>
                    <th className="px-6 py-4">Endpoint</th>
                    <th className="px-6 py-4">Method</th>
                    <th className="px-6 py-4">Type</th>
                    <th className="px-6 py-4">Threat Score</th>
                    <th className="px-6 py-4">Time</th>
                    <th className="px-6 py-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-cyber-border">
                  {attacks.map((attack) => (
                    <tr key={attack.id} className="hover:bg-white/2 transition-colors group">
                      <td className="px-6 py-4 font-mono text-white text-sm">{attack.ip}</td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 bg-cyber-bg border border-cyber-border rounded text-xs text-cyber-primary">
                          {attack.path}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-xs font-bold text-gray-400">{attack.method}</td>
                      <td className="px-6 py-4 text-sm">{attack.type}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-1.5 bg-cyber-bg rounded-full overflow-hidden">
                            <div 
                              className={`h-full rounded-full ${
                                attack.score > 80 ? 'bg-cyber-danger' : 
                                attack.score > 50 ? 'bg-cyber-warning' : 'bg-cyber-success'
                              }`} 
                              style={{ width: `${attack.score}%` }}
                            />
                          </div>
                          <span className={`text-xs font-bold ${
                            attack.score > 80 ? 'text-cyber-danger' : 
                            attack.score > 50 ? 'text-cyber-warning' : 'text-cyber-success'
                          }`}>
                            {attack.score}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-xs text-gray-500 flex items-center gap-1">
                        <Clock size={12} /> {attack.time}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button className="p-2 hover:bg-cyber-primary/10 rounded-lg text-gray-400 hover:text-cyber-primary transition-colors">
                          <Activity size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

const SidebarItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
      active 
        ? 'bg-cyber-primary/10 text-cyber-primary border border-cyber-primary/20 shadow-cyber-glow' 
        : 'text-gray-500 hover:text-gray-300 hover:bg-white/5'
    }`}
  >
    {icon}
    <span className="font-medium text-sm">{label}</span>
    {active && (
      <motion.div 
        layoutId="active-pill" 
        className="ml-auto w-1 h-4 bg-cyber-primary rounded-full"
      />
    )}
  </button>
);

const StatCard = ({ icon, label, value, change }) => (
  <div className="glass-card p-6 group hover:border-cyber-primary/30 transition-all duration-500">
    <div className="flex justify-between items-start mb-4">
      <div className="p-2 bg-cyber-bg border border-cyber-border rounded-lg group-hover:shadow-cyber-glow transition-all">
        {icon}
      </div>
      <span className={`text-xs font-bold ${change.startsWith('+') ? 'text-cyber-success' : 'text-cyber-danger'}`}>
        {change}
      </span>
    </div>
    <div className="text-sm text-gray-500 font-medium mb-1">{label}</div>
    <div className="text-2xl font-bold text-white tracking-tight">{value}</div>
  </div>
);

export default App;
