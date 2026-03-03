import React, { useMemo } from 'react';
import { Text, Hud, OrthographicCamera } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import { SimulationParams } from '../types';

interface Props {
  params: SimulationParams;
  visible: boolean;
}

export const InSceneHUD: React.FC<Props> = ({ params, visible }) => {
  if (!visible) return null;

  const getStatus = () => {
    if (params.fracture) return "CRITICAL_FRACTURE";
    if (params.distortion > 0.5) return "STRESS_WARNING";
    return "STABLE";
  };

  const statusColor = useMemo(() => {
    if (params.fracture) return "#ef4444"; // Red
    if (params.distortion > 0.5) return "#eab308"; // Yellow
    return "#22c55e"; // Green
  }, [params.fracture, params.distortion]);

  return (
    <Hud renderPriority={1}>
      <OrthographicCamera makeDefault position={[0, 0, 10]} zoom={1} />
      <group position={[0, 0, 0]}>
        {/* Top Right HUD */}
        <group position={[0.8, 0.8, 0]}>
          <Text
            position={[0, 0, 0]}
            fontSize={0.03}
            color="#22c55e"
            anchorX="right"
            anchorY="top"
          >
            SYSTEM_ROOT: 42.0000
          </Text>
          <Text
            position={[0, -0.04, 0]}
            fontSize={0.03}
            color="#22c55e"
            anchorX="right"
            anchorY="top"
          >
            ψ(r) = sin({params.interferenceA.toFixed(2)}·θ) × sin({params.interferenceB.toFixed(2)}·φ)
          </Text>
          <Text
            position={[0, -0.08, 0]}
            fontSize={0.03}
            color="#22c55e"
            anchorX="right"
            anchorY="top"
          >
            SHEAR_ANGLE: 39.4° [LOCKED]
          </Text>
          <Text
            position={[0, -0.12, 0]}
            fontSize={0.03}
            color="#22c55e"
            anchorX="right"
            anchorY="top"
          >
            OVERPACK_DELTA: {params.fracture ? '0.000585' : 'LATENT'}
          </Text>
          <Text
            position={[0, -0.16, 0]}
            fontSize={0.03}
            color={statusColor}
            anchorX="right"
            anchorY="top"
          >
            STATUS: {getStatus()}
          </Text>
          <Text
            position={[0, -0.20, 0]}
            fontSize={0.02}
            color="#22c55e"
            fillOpacity={0.5}
            anchorX="right"
            anchorY="top"
          >
            // RADICAL RESONANCE ARCHIVE //
          </Text>
        </group>
      </group>
    </Hud>
  );
};
