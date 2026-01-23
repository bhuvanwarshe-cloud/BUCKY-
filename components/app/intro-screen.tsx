'use client';

import { motion } from 'motion/react';
import { ArrowRight, Cpu, GlobeHemisphereWest } from '@phosphor-icons/react';

interface IntroScreenProps {
    onGetStarted: () => void;
}

export function IntroScreen({ onGetStarted }: IntroScreenProps) {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.8, ease: 'easeInOut' }}
            className="relative z-10 flex min-h-screen flex-col items-center justify-center p-6 text-center text-white"
        >
            {/* Hero Content */}
            <div className="relative">
                <div className="absolute -inset-1 rounded-full bg-cyan-500/20 blur-xl"></div>
                <Cpu
                    weight="duotone"
                    className="relative mb-6 h-24 w-24 animate-pulse text-cyan-400"
                />
            </div>

            <h1 className="mb-2 bg-gradient-to-r from-cyan-400 to-blue-600 bg-clip-text text-5xl font-bold tracking-tighter text-transparent drop-shadow-[0_0_15px_rgba(34,211,238,0.5)]">
                BUCKY
            </h1>

            <p className="mb-8 max-w-md font-mono text-lg tracking-wide text-cyan-100/70">
                ADVANCED TACTICAL AI ASSISTANT
            </p>

            {/* Feature Grid (Mini) */}
            <div className="mb-12 grid grid-cols-2 gap-4 text-xs font-bold tracking-widest text-cyan-300/50 uppercase">
                <div className="flex items-center gap-2">
                    <GlobeHemisphereWest /> Real-time Voice
                </div>
                <div className="flex items-center gap-2">
                    <Cpu /> Neural Processing
                </div>
            </div>

            {/* CTA Button */}
            <button
                onClick={onGetStarted}
                className="group relative flex items-center gap-3 rounded-full border border-cyan-500/50 bg-cyan-950/30 px-8 py-4 text-sm font-bold tracking-widest text-cyan-400 uppercase backdrop-blur-md transition-all hover:border-cyan-400 hover:bg-cyan-500/20 hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.4)]"
            >
                Initialize System
                <ArrowRight className="transition-transform group-hover:translate-x-1" />
            </button>

            {/* Footer System Status */}
            <div className="absolute bottom-6 flex gap-8 font-mono text-[10px] text-cyan-500/30">
                <span>SYS.STATUS: ONLINE</span>
                <span>VER: 2.5.0-ALPHA</span>
                <span>SECURE.CONN: TRUE</span>
            </div>
        </motion.div>
    );
}
