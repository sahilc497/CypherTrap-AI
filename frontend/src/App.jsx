import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, Activity, Terminal, AlertTriangle, Zap, Settings, Database, Users, 
  BarChart3, Clock, ExternalLink, ShieldAlert, Search, Filter, ArrowLeft,
  LayoutDashboard, List, UserCheck, ShieldCheck, Cpu, Globe, Crosshair, 
  Lock, Wifi, Server, RefreshCw, Eye
} from 'lucide-react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  AreaChart, Area, PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [attacks, setAttacks] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [consoleLogs, setConsoleLogs] = useState([]);
  const [summary, setSummary] = useState({
    total_requests: 0,
    active_sessions: 0,
    high_risk_sessions: 0,
    avg_threat_score: 0
  });
  
  const ws = useRef(null);

  useEffect(() => {
    fetchInitialData();
    connectWebSocket();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const fetchInitialData = async () => {
    try {
      const [attacksRes, summaryRes, sessionsRes] = await Promise.all([
        fetch('http://localhost:8000/api/attacks?limit=30').then(res => res.json()),
        fetch('http://localhost:8000/api/summary').then(res => res.json()),
        fetch('http://localhost:8000/api/sessions').then(res => res.json())
      ]);
      setAttacks(attacksRes);
      setSummary(summaryRes);
      setSessions(sessionsRes);
      
      addConsoleLog("INFO", "Forensic database connection established.");
      addConsoleLog("INFO", `Synchronized ${sessionsRes.length} attacker profiles.`);
    } catch (error) {
      addConsoleLog("ERROR", "Failed to reach intelligence backend.");
    }
  };

  const connectWebSocket = () => {
    ws.current = new WebSocket('ws://localhost:8000/ws/attacks');
    
    ws.current.onopen = () => addConsoleLog("SUCCESS", "Real-time threat bridge active.");

    ws.current.onmessage = (event) => {
      const newAttack = JSON.parse(event.data);
      setAttacks(prev => [newAttack, ...prev].slice(0, 50));
      addConsoleLog("CRITICAL", `New threat vector detected from ${newAttack.ip} - Score: ${newAttack.threat_score}%`);
      fetchInitialData();
    };

    ws.current.onclose = () => {
      addConsoleLog("WARNING", "Connection lost. Re-establishing link...");
      setTimeout(connectWebSocket, 3000);
    };
  };

  const addConsoleLog = (type, msg) => {
    const log = { id: Date.now(), type, msg, time: new Date().toLocaleTimeString() };
    setConsoleLogs(prev => [log, ...prev].slice(0, 10));
  };

  const selectSession = (session) => {
    setSelectedSession(session);
    setActiveTab('sessionDetail');
  };

  // World Map Mock - Dots for locations
  const WorldMap = () => (
    <div className="relative w-full h-full bg-[#0a0a0c] rounded-3xl overflow-hidden border border-white/5 flex items-center justify-center">
      <div className="absolute inset-0 opacity-10 pointer-events-none bg-[url('https://upload.wikimedia.org/wikipedia/commons/e/ec/World_map_blank_without_borders.svg')] bg-contain bg-no-repeat bg-center"></div>
      
      {/* Dynamic Threat Nodes */}
      {sessions.map((s, i) => (
        <motion.div
          key={s.id}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="absolute"
          style={{ 
            left: `${((s.longitude || 0) + 180) * (100 / 360)}%`, 
            top: `${(90 - (s.latitude || 0)) * (100 / 180)}%` 
          }}
        >
          <div className={`w-3 h-3 rounded-full ${s.risk_level === 'High' ? 'bg-red-500 shadow-[0_0_10px_#ef4444]' : 'bg-cyan-400 shadow-[0_0_10px_#22d3ee]'} animate-pulse`}></div>
          <div className="absolute top-4 left-0 whitespace-nowrap bg-black/80 backdrop-blur px-2 py-1 rounded text-[8px] font-bold text-white border border-white/10 opacity-0 hover:opacity-100 transition-opacity">
            {s.ip} ({s.city})
          </div>
        </motion.div>
      ))}

      <div className="absolute bottom-6 left-6 flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-cyan-400"></div>
          <span className="text-[10px] font-black uppercase text-gray-500">Normal traffic</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-red-500"></div>
          <span className="text-[10px] font-black uppercase text-gray-500">High Risk</span>
        </div>
      </div>
    </div>
  );

  const renderDashboard = () => {
    const chartData = attacks.slice(0, 15).reverse().map(a => ({
      name: new Date(a.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),
      score: a.threat_score
    }));

    return (
      <div className="space-y-10 pb-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard icon={<Zap className="text-cyan-400" />} label="Interceptions" value={summary.total_requests} trend="+12% today" />
          <StatCard icon={<Users className="text-purple-400" />} label="Active Forensics" value={summary.active_sessions} trend="Stable" />
          <StatCard icon={<ShieldAlert className="text-red-400" />} label="Breach Attempts" value={summary.high_risk_sessions} trend="Critical" />
          <StatCard icon={<Activity className="text-green-400" />} label="Integrity" value="99.8%" trend="Optimal" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          <div className="lg:col-span-3 h-[450px]">
            <WorldMap />
          </div>
          <div className="lg:col-span-2 bg-[#0d0d0f]/60 backdrop-blur-xl border border-white/5 rounded-3xl p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 blur-3xl -mr-32 -mt-32"></div>
            <h3 className="text-sm font-black text-white uppercase tracking-widest mb-8 flex items-center gap-3">
              <BarChart3 size={18} className="text-cyan-400" />
              Intelligence Velocity
            </h3>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" hide />
                  <YAxis hide domain={[0, 100]} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#111114', border: '1px solid #ffffff10', borderRadius: '12px' }}
                    itemStyle={{ color: '#06b6d4' }}
                  />
                  <Area type="monotone" dataKey="score" stroke="#06b6d4" fillOpacity={1} fill="url(#colorScore)" strokeWidth={3} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-6 flex justify-between items-center text-[10px] font-black uppercase text-gray-600">
              <span>Historical Baseline</span>
              <span className="text-cyan-500 flex items-center gap-1">Live <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse"></span></span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 bg-[#0d0d0f]/60 backdrop-blur-xl border border-white/5 rounded-3xl overflow-hidden">
             <div className="p-6 border-b border-white/5 flex items-center justify-between">
                <h3 className="text-xs font-black text-white uppercase tracking-[0.2em]">Latest Reconnaissance</h3>
                <Terminal size={14} className="text-gray-600" />
             </div>
             <div className="max-h-[300px] overflow-y-auto custom-scrollbar">
                {attacks.slice(0, 10).map(attack => (
                  <div key={attack.id} className="px-6 py-4 border-b border-white/5 hover:bg-white/2 transition-colors flex items-center justify-between group">
                    <div className="flex items-center gap-4">
                      <div className={`w-1 h-10 rounded-full ${attack.threat_score > 70 ? 'bg-red-500' : 'bg-cyan-500'}`}></div>
                      <div>
                        <div className="text-xs font-bold text-white mb-0.5">{attack.ip}</div>
                        <div className="text-[10px] font-mono text-gray-600 uppercase tracking-tighter">{attack.attack_type}</div>
                      </div>
                    </div>
                    <div className="text-right">
                       <div className="text-[10px] font-mono text-cyan-400 group-hover:text-cyan-300">SCORE: {attack.threat_score.toFixed(1)}%</div>
                       <div className="text-[9px] text-gray-700">{new Date(attack.timestamp).toLocaleTimeString()}</div>
                    </div>
                  </div>
                ))}
             </div>
          </div>

          <div className="bg-[#0d0d0f]/60 backdrop-blur-xl border border-white/5 rounded-3xl p-8 flex flex-col">
             <h3 className="text-xs font-black text-white uppercase tracking-[0.2em] mb-8 flex items-center gap-2">
                <Server size={16} className="text-purple-400" /> System Health
             </h3>
             <div className="space-y-8 flex-1">
                <HealthBar label="Intelligence Engine (Gemini)" status="Optimal" percentage={98} color="bg-green-500" />
                <HealthBar label="Deception Core (Simulator)" status="Active" percentage={100} color="bg-cyan-500" />
                <HealthBar label="ML Anomaly Monitor" status="Scanning" percentage={85} color="bg-purple-500" />
                <HealthBar label="Forensic Storage (Postgres)" status="Healthy" percentage={92} color="bg-blue-500" />
             </div>
             <div className="mt-10 p-4 bg-white/2 rounded-2xl border border-white/5 flex items-center gap-4">
                <RefreshCw size={14} className="text-cyan-400 animate-spin-slow" />
                <span className="text-[10px] font-bold text-gray-500 uppercase">Self-healing active</span>
             </div>
          </div>
        </div>
      </div>
    );
  };

  const renderFeed = () => (
    <div className="bg-[#0d0d0f]/80 backdrop-blur-2xl border border-white/5 rounded-3xl overflow-hidden shadow-2xl">
      <div className="p-8 border-b border-white/10 flex items-center justify-between bg-white/1">
        <div className="flex items-center gap-4">
          <div className="w-4 h-4 bg-red-500 rounded-full animate-ping absolute"></div>
          <div className="w-4 h-4 bg-red-500 rounded-full relative"></div>
          <h3 className="text-lg font-black text-white uppercase tracking-[0.2em]">Signal Intelligence Stream</h3>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-[10px] font-bold text-gray-500 uppercase flex items-center gap-2">
            <Wifi size={14} /> Bandwidth: 1.2 GB/s
          </span>
          <button className="p-2 bg-white/5 rounded-xl text-white hover:bg-white/10 transition-all"><Filter size={18}/></button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-black/40 text-[9px] font-black text-gray-600 uppercase tracking-[0.3em] border-b border-white/5">
            <tr>
              <th className="px-10 py-6">Identity</th>
              <th className="px-10 py-6">Intelligence Class</th>
              <th className="px-10 py-6">Intercepted Payload</th>
              <th className="px-10 py-6">Threat Intensity</th>
              <th className="px-10 py-6 text-right">Detection Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5 font-mono">
            <AnimatePresence>
              {attacks.map((attack) => (
                <motion.tr 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  key={attack.id} 
                  className="hover:bg-cyan-500/5 transition-all cursor-crosshair group"
                  onClick={() => selectSession(sessions.find(s => s.session_id === attack.session_id))}
                >
                  <td className="px-10 py-6">
                    <div className="flex items-center gap-4">
                       <div className="p-2 bg-white/3 rounded-lg border border-white/5 group-hover:border-cyan-500/30">
                          <Globe size={14} className="text-gray-500 group-hover:text-cyan-400" />
                       </div>
                       <div>
                          <div className="text-sm font-bold text-white tracking-tighter">{attack.ip}</div>
                          <div className="text-[10px] text-gray-600 uppercase">Vector ID: {attack.id.substring(0, 8)}</div>
                       </div>
                    </div>
                  </td>
                  <td className="px-10 py-6">
                    <span className={`px-3 py-1 rounded text-[10px] font-black uppercase tracking-widest ${
                      attack.threat_score > 70 ? 'text-red-400 border border-red-500/20' : 'text-cyan-400 border border-cyan-500/20'
                    }`}>
                      {attack.attack_type}
                    </span>
                  </td>
                  <td className="px-10 py-6">
                    <div className="max-w-md bg-black/40 px-4 py-3 rounded-xl border border-white/5 group-hover:border-cyan-500/10 transition-all">
                       <code className="text-[11px] text-gray-400 group-hover:text-cyan-200 truncate block">
                        {attack.query}
                       </code>
                    </div>
                  </td>
                  <td className="px-10 py-6">
                    <div className="flex items-center gap-3">
                       <div className="w-24 h-1.5 bg-white/5 rounded-full overflow-hidden">
                          <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: `${attack.threat_score}%` }}
                            className={`h-full ${attack.threat_score > 70 ? 'bg-red-500 shadow-[0_0_10px_#ef4444]' : 'bg-cyan-500 shadow-[0_0_10px_#22d3ee]'}`}
                          />
                       </div>
                       <span className="text-xs font-black text-white">{attack.threat_score.toFixed(1)}%</span>
                    </div>
                  </td>
                  <td className="px-10 py-6 text-right">
                    <div className="text-xs text-white/80">{new Date(attack.timestamp).toLocaleTimeString()}</div>
                    <div className="text-[10px] text-gray-700">{new Date(attack.timestamp).toLocaleDateString()}</div>
                  </td>
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderSessions = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <AnimatePresence>
        {sessions.map((session) => (
          <motion.div 
            layout
            key={session.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="group relative bg-[#0d0d0f]/60 backdrop-blur-xl border border-white/5 p-10 rounded-4xl hover:border-cyan-500/40 transition-all cursor-pointer overflow-hidden shadow-2xl"
            onClick={() => selectSession(session)}
          >
            {/* Background Accent */}
            <div className={`absolute top-0 right-0 w-40 h-40 blur-3xl -mr-20 -mt-20 opacity-20 ${session.risk_level === 'High' ? 'bg-red-500' : 'bg-cyan-500'}`}></div>
            
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-10">
                <div className="p-4 bg-white/2 border border-white/5 rounded-2xl group-hover:shadow-[0_0_20px_rgba(6,182,212,0.1)] transition-all">
                  <Globe className={session.risk_level === 'High' ? 'text-red-400' : 'text-cyan-400'} size={24} />
                </div>
                <span className={`px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border ${
                  session.risk_level === 'High' ? 'border-red-500/30 text-red-400 bg-red-500/5' : 'border-cyan-500/30 text-cyan-400 bg-cyan-500/5'
                }`}>
                  {session.risk_level} Risk Level
                </span>
              </div>
              
              <div className="mb-10">
                <p className="text-[10px] font-black text-gray-600 uppercase tracking-widest mb-2">{session.city}, {session.country}</p>
                <h4 className="text-3xl font-black text-white tracking-tighter group-hover:text-cyan-400 transition-colors">{session.ip}</h4>
              </div>

              <div className="grid grid-cols-2 gap-8 pt-8 border-t border-white/5">
                <div>
                  <p className="text-[9px] font-black text-gray-700 uppercase mb-2">Total Intercepts</p>
                  <p className="text-xl font-mono text-white font-black">{session.requests}</p>
                </div>
                <div>
                  <p className="text-[9px] font-black text-gray-700 uppercase mb-2">Behavior Score</p>
                  <p className="text-xl font-mono text-white font-black">{session.score.toFixed(1)}%</p>
                </div>
              </div>

              <div className="mt-10 flex items-center justify-between text-[10px] text-gray-500 font-bold uppercase tracking-widest">
                 <div className="flex items-center gap-2">
                    <Clock size={12} /> Seen {new Date(session.last_seen).toLocaleTimeString()}
                 </div>
                 <div className="flex items-center gap-2 group-hover:text-cyan-400 transition-colors">
                    Forensics <ArrowLeft size={12} className="rotate-180" />
                 </div>
              </div>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );

  const renderSessionDetail = () => {
    if (!selectedSession) return null;
    
    const sessionAttacks = attacks.filter(a => a.session_id === selectedSession.session_id);

    return (
      <div className="space-y-10 pb-20">
        <button 
          onClick={() => setActiveTab('sessions')}
          className="flex items-center gap-3 text-cyan-400 hover:text-cyan-300 transition-colors font-black text-xs uppercase tracking-widest group"
        >
          <div className="p-2 bg-cyan-500/10 rounded-lg group-hover:scale-110 transition-transform"><ArrowLeft size={16} /></div>
          Back to Forensic Intelligence
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          <div className="lg:col-span-1 space-y-8">
            <div className="bg-[#0d0d0f]/80 backdrop-blur-2xl border border-white/5 rounded-4xl p-10 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 blur-3xl"></div>
              
              <div className="w-20 h-20 rounded-3xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-8 shadow-2xl">
                <Users size={40} className="text-cyan-400" />
              </div>
              <h2 className="text-4xl font-black text-white tracking-tighter mb-2">{selectedSession.ip}</h2>
              <p className="text-[9px] font-mono text-gray-600 break-all mb-10 uppercase tracking-widest">{selectedSession.id}</p>
              
              <div className="space-y-4 mb-10">
                <ForensicRow label="Location" value={`${selectedSession.city}, ${selectedSession.country}`} icon={<Globe size={14}/>} />
                <ForensicRow label="Risk Profile" value={selectedSession.risk_level} icon={<ShieldAlert size={14}/>} highlight={selectedSession.risk_level === 'High'} />
                <ForensicRow label="First Detected" value={new Date(selectedSession.last_seen).toLocaleDateString()} icon={<Clock size={14}/>} />
              </div>

              {selectedSession.captured_face_url && (
                <div className="mt-10 group relative">
                   <div className="absolute inset-0 bg-red-500/20 blur-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                   <div className="relative bg-black/40 p-2 rounded-3xl border border-white/10 overflow-hidden">
                      <div className="absolute inset-x-0 top-0 h-1 bg-red-500 shadow-[0_0_20px_#ef4444] animate-scan z-20"></div>
                      <img 
                        src={selectedSession.captured_face_url} 
                        alt="Attacker Face" 
                        className="w-full h-64 object-cover rounded-2xl grayscale group-hover:grayscale-0 transition-all duration-1000 scale-105 group-hover:scale-100" 
                      />
                      <div className="absolute inset-0 bg-linear-to-t from-black via-transparent to-transparent pointer-events-none"></div>
                      <div className="absolute bottom-6 left-6 flex items-center gap-3">
                         <div className="p-2 bg-red-500 rounded-lg shadow-[0_0_15px_#ef4444]"><Eye size={16} className="text-white" /></div>
                         <div>
                            <div className="text-[10px] font-black text-white uppercase tracking-widest">Biometric Match</div>
                            <div className="text-[8px] text-gray-500 uppercase tracking-widest">Identity: ATTACKER_ALPHA</div>
                         </div>
                      </div>
                   </div>
                </div>
              )}

              <div className="mt-10 p-6 bg-white/2 rounded-2xl border border-white/5">
                <p className="text-[9px] font-black text-gray-700 uppercase tracking-[0.2em] mb-4">Device Fingerprint</p>
                <p className="text-[10px] text-gray-500 font-mono leading-relaxed italic">{selectedSession.ua}</p>
              </div>
            </div>
          </div>

          <div className="lg:col-span-2 space-y-10">
            <div className="bg-[#0d0d0f]/60 backdrop-blur-xl border border-white/5 rounded-4xl p-10 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-10 opacity-5 pointer-events-none">
                 <Shield className="w-64 h-64 text-white" />
              </div>
              <h3 className="text-xl font-black text-white mb-10 flex items-center gap-4">
                <div className="p-2 bg-purple-500/20 rounded-xl"><Activity size={24} className="text-purple-400" /></div>
                Tactical Intelligence Timeline
              </h3>
              
              <div className="space-y-10 relative before:absolute before:left-[19px] before:top-2 before:bottom-2 before:w-px before:bg-white/5">
                {sessionAttacks.map((attack) => (
                  <motion.div 
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={attack.id} 
                    className="relative pl-14"
                  >
                    <div className={`absolute left-0 top-1 w-10 h-10 rounded-xl border-4 border-[#0a0a0c] z-10 flex items-center justify-center shadow-2xl ${
                      attack.threat_score > 70 ? 'bg-red-500/20 border-red-500/30' : 'bg-cyan-500/20 border-cyan-500/30'
                    }`}>
                       <div className={`w-2 h-2 rounded-full ${attack.threat_score > 70 ? 'bg-red-500 animate-pulse' : 'bg-cyan-400 animate-pulse'}`}></div>
                    </div>
                    
                    <div className="p-8 bg-white/2 rounded-3xl border border-white/5 hover:border-cyan-500/20 transition-all group relative overflow-hidden">
                      <div className="absolute top-0 right-0 p-8 flex flex-col items-end gap-2">
                         <span className="text-[9px] text-gray-700 font-mono">{new Date(attack.timestamp).toLocaleTimeString()}</span>
                         <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${
                           attack.threat_score > 70 ? 'text-red-400 bg-red-500/10' : 'text-cyan-400 bg-cyan-500/10'
                         }`}>Score: {attack.threat_score.toFixed(1)}%</span>
                      </div>
                      
                      <div className="flex flex-col gap-6">
                        <div>
                          <span className="text-[10px] font-black text-cyan-400 uppercase tracking-[0.2em] mb-3 block">Signal Type: {attack.attack_type}</span>
                          <div className="bg-black/60 p-5 rounded-2xl border border-white/5 group-hover:border-cyan-500/10 transition-all">
                             <code className="text-xs text-gray-300 font-mono leading-relaxed block break-all">
                               {attack.query}
                             </code>
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-8">
                           <IntelMetric icon={<Cpu size={14}/>} label="Target Point" value={attack.endpoint} />
                           <IntelMetric icon={<ShieldCheck size={14}/>} label="Response" value="Simulator_Enriched" />
                           <IntelMetric icon={<Wifi size={14}/>} label="Protocol" value="HTTP/1.1" />
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex h-screen bg-[#070709] text-gray-400 font-sans overflow-hidden selection:bg-cyan-500/30">
      {/* Dynamic Grid Background */}
      <div className="absolute inset-0 bg-size-[40px_40px] bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] mask-[radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
      
      {/* Sidebar */}
      <nav className="w-80 border-r border-white/5 bg-[#0d0d0f]/90 backdrop-blur-3xl z-20 flex flex-col shadow-2xl relative">
        <div className="p-10 flex items-center gap-4 border-b border-white/5">
          <div className="relative">
             <div className="absolute inset-0 bg-cyan-500 blur-xl opacity-20 animate-pulse"></div>
             <div className="p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-2xl relative">
                <ShieldAlert className="text-cyan-400 h-8 w-8" />
             </div>
          </div>
          <div>
             <span className="font-black text-2xl text-white tracking-tighter block leading-none">SOC<span className="text-cyan-400">ENGINE</span></span>
             <span className="text-[9px] font-black text-gray-600 uppercase tracking-widest">v2.0 Advanced Forensic</span>
          </div>
        </div>

        <div className="flex-1 px-6 py-10 space-y-2">
          <SidebarItem icon={<LayoutDashboard size={20}/>} label="Global Overview" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <SidebarItem icon={<Activity size={20}/>} label="Signal Intelligence" active={activeTab === 'feed'} onClick={() => setActiveTab('feed')} />
          <SidebarItem icon={<UserCheck size={20}/>} label="Attacker Profiles" active={activeTab === 'sessions'} onClick={() => setActiveTab('sessions')} />
          <SidebarItem icon={<Database size={20}/>} label="Deception Traps" active={activeTab === 'traps'} onClick={() => setActiveTab('traps')} />
          <SidebarItem icon={<Settings size={20}/>} label="System Engine" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </div>

        {/* Live Terminal Sidebar Section */}
        <div className="p-6 border-t border-white/5 bg-black/40">
           <p className="text-[9px] font-black text-gray-700 uppercase tracking-[0.2em] mb-4 flex items-center justify-between">
              Live Bridge Logs <span className="w-2 h-2 rounded-full bg-green-500"></span>
           </p>
           <div className="space-y-3">
              {consoleLogs.map(log => (
                <div key={log.id} className="text-[10px] font-mono leading-tight flex gap-2">
                   <span className={log.type === 'CRITICAL' ? 'text-red-500' : log.type === 'SUCCESS' ? 'text-green-500' : 'text-gray-500'}>[{log.type}]</span>
                   <span className="text-gray-600 truncate">{log.msg}</span>
                </div>
              ))}
           </div>
        </div>

        <div className="p-8 border-t border-white/5">
          <div className="flex items-center gap-4 p-4 bg-white/2 rounded-3xl border border-white/5">
            <div className="w-12 h-12 rounded-2xl bg-linear-to-tr from-cyan-500 to-purple-500 flex items-center justify-center text-white font-black text-lg shadow-2xl">SC</div>
            <div>
              <div className="text-xs font-black text-white uppercase tracking-tighter">Sahil Chavan</div>
              <div className="text-[8px] text-cyan-400 font-black uppercase tracking-widest">Lead Architect</div>
            </div>
            <Lock size={12} className="ml-auto text-gray-700" />
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto z-10 relative custom-scrollbar">
        <header className="h-24 border-b border-white/5 flex items-center justify-between px-12 bg-[#070709]/60 backdrop-blur-md sticky top-0 z-30">
          <div className="flex items-center gap-8">
            <h1 className="text-sm font-black text-white uppercase tracking-[0.3em] flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></div>
              {activeTab === 'dashboard' ? 'Tactical Command Center' : 
               activeTab === 'feed' ? 'Real-time Threat Stream' : 
               activeTab === 'sessions' ? 'Forensic Intelligence Database' : 
               activeTab === 'sessionDetail' ? 'Deep Forensics Analysis' : 'Configuration'}
            </h1>
            <div className="h-4 w-px bg-white/10"></div>
            <div className="flex gap-4">
               <HeaderStatus icon={<Wifi size={12}/>} label="Bridge" value="ACTIVE" />
               <HeaderStatus icon={<Cpu size={12}/>} label="ML Model" value="LEARNING" />
               <HeaderStatus icon={<Database size={12}/>} label="Deception" value="SYNCED" />
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="relative group">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-700 group-focus-within:text-cyan-500 transition-colors" size={14} />
              <input type="text" placeholder="TRACE IP / UID / VECTOR..." className="bg-white/2 border border-white/5 rounded-2xl py-3 pl-10 pr-6 text-[10px] w-72 focus:outline-none focus:border-cyan-500/30 focus:bg-white/5 transition-all uppercase tracking-widest" />
            </div>
            <button className="bg-white/2 border border-white/10 text-white font-black px-6 py-3 rounded-2xl text-[10px] uppercase tracking-widest hover:bg-white/5 transition-all">
              Security Protocol
            </button>
          </div>
        </header>

        <div className="p-12">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
            >
              {activeTab === 'dashboard' && renderDashboard()}
              {activeTab === 'feed' && renderFeed()}
              {activeTab === 'sessions' && renderSessions()}
              {activeTab === 'sessionDetail' && renderSessionDetail()}
              {activeTab === 'settings' && <div className="text-center py-40 text-[10px] font-black uppercase tracking-[0.5em] text-gray-700">Access Denied: Level 5 Clearance Required</div>}
              {activeTab === 'traps' && <div className="text-center py-40 text-[10px] font-black uppercase tracking-[0.5em] text-gray-700">Deception Array: Initializing Nodes...</div>}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};

const SidebarItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-5 px-6 py-5 rounded-3xl transition-all relative group ${
      active ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-2xl' : 'text-gray-600 hover:text-gray-300 hover:bg-white/2'
    }`}
  >
    <div className={`transition-all duration-500 ${active ? 'scale-110' : 'group-hover:scale-110'}`}>
       {icon}
    </div>
    <span className="font-black text-[11px] uppercase tracking-widest">{label}</span>
    {active && (
      <div className="ml-auto w-1.5 h-1.5 bg-cyan-500 rounded-full shadow-[0_0_10px_#06b6d4]"></div>
    )}
  </button>
);

const StatCard = ({ icon, label, value, trend }) => (
  <div className="bg-[#0d0d0f]/60 backdrop-blur-xl border border-white/5 p-8 rounded-4xl group hover:border-cyan-500/30 transition-all relative overflow-hidden shadow-2xl">
    <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-cyan-500/10 transition-all"></div>
    <div className="flex justify-between items-start mb-8">
       <div className="p-3.5 bg-white/3 border border-white/5 rounded-2xl group-hover:shadow-[0_0_15px_rgba(6,182,212,0.15)] transition-all">
          {icon}
       </div>
       <span className={`text-[10px] font-black px-2 py-0.5 rounded-lg ${trend.includes('+') || trend === 'Optimal' || trend === 'Stable' ? 'text-green-400 bg-green-500/10' : 'text-red-400 bg-red-500/10'}`}>
          {trend}
       </span>
    </div>
    <div className="text-[10px] text-gray-600 font-black uppercase tracking-[0.2em] mb-2">{label}</div>
    <div className="text-4xl font-black text-white tracking-tighter group-hover:text-cyan-50 transition-all">{value}</div>
  </div>
);

const HealthBar = ({ label, status, percentage, color }) => (
  <div className="space-y-3">
    <div className="flex justify-between items-center text-[9px] font-black uppercase tracking-widest">
      <span className="text-gray-500">{label}</span>
      <span className={percentage > 90 ? 'text-green-500' : 'text-cyan-400'}>{status}</span>
    </div>
    <div className="h-1 bg-white/5 rounded-full overflow-hidden">
      <motion.div 
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        className={`h-full ${color} rounded-full`} 
      />
    </div>
  </div>
);

const HeaderStatus = ({ icon, label, value }) => (
  <div className="flex items-center gap-2 px-3 py-1 bg-white/2 border border-white/5 rounded-lg">
     <div className="text-gray-600">{icon}</div>
     <span className="text-[8px] font-black text-gray-500 uppercase tracking-widest">{label}:</span>
     <span className="text-[8px] font-black text-cyan-500 uppercase tracking-widest">{value}</span>
  </div>
);

const ForensicRow = ({ label, value, icon, highlight }) => (
  <div className="flex justify-between items-center p-4 bg-white/2 rounded-2xl border border-white/5 hover:border-white/10 transition-colors">
     <div className="flex items-center gap-3 text-gray-600">
        {icon}
        <span className="text-[10px] font-black uppercase tracking-widest">{label}</span>
     </div>
     <span className={`text-[10px] font-bold ${highlight ? 'text-red-400' : 'text-white'}`}>{value}</span>
  </div>
);

const IntelMetric = ({ icon, label, value }) => (
  <div className="flex flex-col gap-1">
     <div className="flex items-center gap-2 text-gray-700">
        {icon}
        <span className="text-[8px] font-black uppercase tracking-widest">{label}</span>
     </div>
     <span className="text-[10px] font-bold text-gray-400 uppercase">{value}</span>
  </div>
);

export default App;
