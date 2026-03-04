import React from 'react';
import { SoftCreature } from './components/SoftCreature';
import { PivotValidator } from './components/PivotValidator';

function App() {
  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      {/* 93-Point Icosahedral Phase Matrix (WebGL) */}
      <SoftCreature />
      
      {/* Live Server Physics Dashboard */}
      <PivotValidator />
    </div>
  );
}

export default App;
