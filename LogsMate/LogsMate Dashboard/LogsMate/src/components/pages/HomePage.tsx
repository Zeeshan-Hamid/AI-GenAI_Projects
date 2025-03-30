import React from 'react';
import { HeroSection } from '../Home/HeroSection';
import { FeaturesSection } from '../Home/FeaturesSection';
import { HowItWorksSection } from '../Home/HowItWorksSection';

export const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen">
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
    </div>
  );
};