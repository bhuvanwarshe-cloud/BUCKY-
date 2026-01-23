'use client';

import { useState } from 'react';
import { motion } from 'motion/react';
import { Brain, CaretRight, Robot, Sparkle, User } from '@phosphor-icons/react';
import { useUserPreferences } from '@/hooks/useUserPreferences';

interface OnboardingFormProps {
  onComplete: () => void;
}

const BEHAVIORS = [
  { id: 'tactical', label: 'Tactical (JARVIS)', desc: 'Precise, concise, efficient.' },
  { id: 'friendly', label: 'Friendly', desc: 'Warm, casual, conversational.' },
  { id: 'professional', label: 'Professional', desc: 'Formal, polite, business-like.' },
  { id: 'energetic', label: 'Energetic', desc: 'High energy, motivational.' },
  { id: 'minimal', label: 'Minimal', desc: 'Direct answers only. No chit-chat.' },
] as const;

export function OnboardingForm({ onComplete }: OnboardingFormProps) {
  const { preferences, savePreferences } = useUserPreferences();

  const [formData, setFormData] = useState({
    userFirstName: preferences.userFirstName || '',
    userLastName: preferences.userLastName || '',
    assistantName: preferences.assistantName || 'BUCKY',
    assistantBehavior: preferences.assistantBehavior || 'tactical',
  });
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.userFirstName.trim()) {
      setError('First Name is required');
      return;
    }
    if (!formData.assistantName.trim()) {
      setError('Assistant Name is required');
      return;
    }

    savePreferences({
      userFirstName: formData.userFirstName,
      userLastName: formData.userLastName,
      assistantName: formData.assistantName,
      assistantBehavior: formData.assistantBehavior,
    });
    onComplete();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, filter: 'blur(10px)' }}
      transition={{ duration: 0.6, ease: 'circOut' }}
      className="z-10 w-full max-w-md p-6"
    >
      <div className="relative overflow-hidden rounded-2xl border border-cyan-500/20 bg-black/60 p-8 text-white shadow-[0_0_40px_-10px_rgba(6,182,212,0.15)] backdrop-blur-2xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full border border-cyan-500/30 bg-cyan-500/10">
            <Sparkle size={20} weight="fill" className="text-cyan-400" />
          </div>
          <h1 className="mb-2 text-xl font-bold tracking-widest text-cyan-400 uppercase">
            System Configuration
          </h1>
          <div className="mx-auto h-0.5 w-16 rounded-full bg-cyan-500/50"></div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* User Name Grid */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-[10px] font-bold tracking-wider text-cyan-200/50 uppercase">
                <User size={12} weight="bold" /> First Name *
              </label>
              <input
                type="text"
                placeholder="Tony"
                value={formData.userFirstName}
                onChange={(e) => setFormData({ ...formData, userFirstName: e.target.value })}
                className="w-full rounded-md border border-cyan-500/20 bg-cyan-950/20 px-3 py-2 text-sm text-cyan-100 placeholder-cyan-900/50 transition-all focus:border-cyan-400 focus:bg-cyan-950/40 focus:ring-1 focus:ring-cyan-400 focus:outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="pl-1 text-[10px] font-bold tracking-wider text-cyan-200/50 uppercase">
                Last Name
              </label>
              <input
                type="text"
                placeholder="Stark"
                value={formData.userLastName}
                onChange={(e) => setFormData({ ...formData, userLastName: e.target.value })}
                className="w-full rounded-md border border-cyan-500/20 bg-cyan-950/20 px-3 py-2 text-sm text-cyan-100 placeholder-cyan-900/50 transition-all focus:border-cyan-400 focus:bg-cyan-950/40 focus:ring-1 focus:ring-cyan-400 focus:outline-none"
              />
            </div>
          </div>

          {/* Assistant Name */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-[10px] font-bold tracking-wider text-cyan-200/50 uppercase">
              <Robot size={12} weight="bold" /> Assistant Designation *
            </label>
            <input
              type="text"
              value={formData.assistantName}
              onChange={(e) => setFormData({ ...formData, assistantName: e.target.value })}
              className="w-full rounded-md border border-cyan-500/20 bg-cyan-950/20 px-3 py-2 text-sm text-cyan-100 placeholder-cyan-900/50 transition-all focus:border-cyan-400 focus:bg-cyan-950/40 focus:ring-1 focus:ring-cyan-400 focus:outline-none"
            />
          </div>

          {/* Behavior Selection */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-[10px] font-bold tracking-wider text-cyan-200/50 uppercase">
              <Brain size={12} weight="bold" /> Personality Matrix *
            </label>
            <div className="relative">
              <select
                value={formData.assistantBehavior}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    assistantBehavior: e.target.value as
                      | 'tactical'
                      | 'friendly'
                      | 'professional'
                      | 'energetic'
                      | 'minimal',
                  })
                }
                className="w-full appearance-none rounded-md border border-cyan-500/20 bg-cyan-950/20 px-3 py-2 text-sm text-cyan-100 transition-all focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 focus:outline-none"
              >
                {BEHAVIORS.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.label}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute top-1/2 right-3 -translate-y-1/2 text-cyan-500">
                <CaretRight className="rotate-90" size={12} />
              </div>
            </div>
            <p className="mt-1 text-[10px] text-cyan-500/60">
              {BEHAVIORS.find((b) => b.id === formData.assistantBehavior)?.desc}
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <p className="animate-pulse text-center font-mono text-xs text-red-400">
              ERROR: {error}
            </p>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            className="group w-full rounded-md bg-cyan-500 py-3 text-xs font-bold tracking-widest text-black uppercase shadow-[0_0_20px_-5px_rgba(34,211,238,0.6)] transition-all hover:bg-cyan-400 active:scale-[0.98]"
          >
            Proceed to Interface
          </button>
        </form>
      </div>
    </motion.div>
  );
}
