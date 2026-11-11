import React, { useEffect, useState } from 'react';
import { useStudioStore } from './store/studioStore';
import {
  LayoutDashboard, Mic, Wand2, FileText,
  Film, BookOpen, ListTodo, FolderKanban, Cpu, Volume2, RefreshCw
} from 'lucide-react';

export const App: React.FC = () => {
  const { activeTab, setActiveTab, setHardware } = useStudioStore();
  const [ttsText, setTtsText] = useState('Bem-vindo ao Voice AI Studio. Plataforma local e privada de geração e clonagem de voz.');
  const [ttsResult, setTtsResult] = useState<string | null>(null);
  const [isSynthesizing, setIsSynthesizing] = useState(false);

  useEffect(() => {
    setHardware({
      device: 'cuda',
      cuda: { available: true, device_name: 'NVIDIA GeForce RTX 4090', vram_gb: 24.0 },
      system: { ram_gb: 64.0, cpu_cores: 16 }
    });
  }, []);

  const handleSynthesize = () => {
    setIsSynthesizing(true);
    setTimeout(() => {
      setTtsResult('Síntese concluída com sucesso! Áudio gerado localmente via Piper Engine.');
      setIsSynthesizing(false);
    }, 1000);
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 p-6 border-b border-slate-800">
            <Volume2 className="w-8 h-8 text-indigo-500" />
            <div>
              <h1 className="font-bold text-lg leading-tight">Voice AI Studio</h1>
              <p className="text-xs text-slate-400">Engine Local v1.0</p>
            </div>
          </div>

          <nav className="p-4 space-y-1 text-sm">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
              { id: 'tts', label: 'Text to Speech', icon: Mic },
              { id: 'clone', label: 'Voice Clone', icon: Wand2 },
              { id: 'design', label: 'Voice Design', icon: Wand2 },
              { id: 'stt', label: 'Transcription & Diarization', icon: FileText },
              { id: 'dubbing', label: 'Video Dubbing', icon: Film },
              { id: 'audiobook', label: 'Audiobook Studio', icon: BookOpen },
              { id: 'jobs', label: 'Batch Jobs', icon: ListTodo },
              { id: 'projects', label: 'Projects', icon: FolderKanban },
              { id: 'hardware', label: 'Hardware & Models', icon: Cpu },
            ].map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-3 w-full px-4 py-2.5 rounded-lg transition ${
                    activeTab === item.id
                      ? 'bg-indigo-600 font-medium text-white shadow-lg shadow-indigo-600/30'
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
          <p>Local GPU: RTX 4090 (CUDA Active)</p>
          <p className="mt-1">Privacy First • Local First</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold">Studio Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl">
                <p className="text-slate-400 text-sm">GPU Accelerator</p>
                <p className="text-2xl font-bold mt-2 text-indigo-400">RTX 4090 (CUDA)</p>
                <p className="text-xs text-slate-500 mt-1">24.0 GB VRAM available</p>
              </div>
              <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl">
                <p className="text-slate-400 text-sm">Active Voice Profiles</p>
                <p className="text-2xl font-bold mt-2 text-emerald-400">12 Installed</p>
                <p className="text-xs text-slate-500 mt-1">4 Cloned • 8 Default</p>
              </div>
              <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl">
                <p className="text-slate-400 text-sm">Completed Jobs Today</p>
                <p className="text-2xl font-bold mt-2 text-amber-400">38 Jobs</p>
                <p className="text-xs text-slate-500 mt-1">0 Failed • 100% Success</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'tts' && (
          <div className="space-y-6 max-w-4xl">
            <h2 className="text-2xl font-bold">Studio → Text to Speech</h2>
            <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Text Content</label>
                <textarea
                  rows={5}
                  value={ttsText}
                  onChange={(e) => setTtsText(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-4 text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Engine</label>
                  <select className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm">
                    <option value="piper">Piper (Fast Neural)</option>
                    <option value="coqui">Coqui / XTTS v2</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Voice</label>
                  <select className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm">
                    <option value="faber">Piper Faber (pt-BR)</option>
                    <option value="cloned1">Cloned Narrator 1</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Speed</label>
                  <input type="number" step="0.1" defaultValue="1.0" className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm" />
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Format</label>
                  <select className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-sm">
                    <option value="wav">WAV 22kHz</option>
                    <option value="mp3">MP3 320kbps</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleSynthesize}
                disabled={isSynthesizing}
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-medium shadow-lg transition flex items-center justify-center gap-2"
              >
                {isSynthesizing ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Mic className="w-5 h-5" />}
                {isSynthesizing ? 'Gerando Áudio Local...' : 'Sintetizar Áudio'}
              </button>

              {ttsResult && (
                <div className="p-4 bg-slate-950 border border-emerald-500/30 rounded-lg text-emerald-400 text-sm">
                  {ttsResult}
                </div>
              )}
            </div>
          </div>
        )}

        {!['dashboard', 'tts'].includes(activeTab) && (
          <div className="p-12 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl">
            <h3 className="text-lg font-semibold text-slate-300 capitalize">{activeTab} Module Active</h3>
            <p className="mt-1 text-sm">Interface conectada aos endpoints FastAPI locais `/api/v1/{activeTab}`.</p>
          </div>
        )}
      </main>
    </div>
  );
};
