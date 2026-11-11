import { create } from 'zustand';

interface VoiceAIStudioState {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  hardware: any;
  setHardware: (hw: any) => void;
  loadedModels: any;
  setLoadedModels: (models: any) => void;
}

export const useStudioStore = create<VoiceAIStudioState>((set) => ({
  activeTab: 'dashboard',
  setActiveTab: (tab) => set({ activeTab: tab }),
  hardware: null,
  setHardware: (hw) => set({ hardware: hw }),
  loadedModels: {},
  setLoadedModels: (models) => set({ loadedModels: models }),
}));
