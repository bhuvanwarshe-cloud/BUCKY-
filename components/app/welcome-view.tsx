import React, { forwardRef } from 'react';
import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <svg
      width="64"
      height="64"
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="text-fg0 mb-4 size-16"
    />
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = forwardRef<HTMLDivElement, WelcomeViewProps>(
  ({ startButtonText, onStartCall }, ref) => {
    return (
      <div ref={ref} className="flex min-h-screen items-center justify-center overflow-hidden">
        {/* 🔥 Background Video */}
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 h-full w-full object-cover"
        >
          <source src="/BuckyFuture.mp4" type="video/mp4" />
        </video>

        {/* Dark overlay for readability */}
        <div className="absolute inset-0 bg-black/55" />

        {/* Top-left avatar */}
        <div className="fixed top-4 left-4 z-50">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/Gemini_Generated_Image_jqvvutjqvvutjqvv (1).png"
            alt="Bhuvan"
            className="h-13 w-13 rounded-full object-cover"
          />
        </div>

        {/* Foreground Content */}
        <section className="relative z-10 flex flex-col items-center text-center">
          <WelcomeImage />

          <Button
            variant="primary"
            size="lg"
            onClick={() => {
              const sound = new Audio('/buttonClick.mp3');
              sound.volume = 0.8;
              sound.play();
              onStartCall();
            }}
            className="mt-6 w-64 font-mono"
          >
            {startButtonText}
          </Button>
        </section>

        {/* Footer */}
        <div className="z-50·flex·w-full·items-center·justify-center">
          <p className="rounded-md·bg-black/60·px-4·py-2·text-sm·font-bold·tracking-widest·text-white·shadow-[0_4px_20px_rgba(0,0,0,0.9)]·backdrop-blur-sm·md:text-base">
            Created by Bhuvan Warshe
          </p>
        </div>
      </div>
    );
  }
);

WelcomeView.displayName = 'WelcomeView';
