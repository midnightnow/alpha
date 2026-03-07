import React, { useMemo } from 'react';
import * as THREE from 'three';
import { Text, Float } from '@react-three/drei';
import planisphereData from '../data/planisphere.json';

const SectorWedge = ({ sector, index, rotation }: { sector: any, index: number, rotation: number }) => {
    const innerRadius = 8;
    const outerRadius = 15;
    const thickness = 0.2;
    const startAngle = (index * 45) * (Math.PI / 180);
    const endAngle = ((index + 1) * 45) * (Math.PI / 180);

    const shape = useMemo(() => {
        const s = new THREE.Shape();
        s.moveTo(Math.cos(startAngle) * innerRadius, Math.sin(startAngle) * innerRadius);
        s.absarc(0, 0, outerRadius, startAngle, endAngle, false);
        s.lineTo(Math.cos(endAngle) * innerRadius, Math.sin(endAngle) * innerRadius);
        s.absarc(0, 0, innerRadius, endAngle, startAngle, true);
        return s;
    }, [index]);

    return (
        <group rotation={[-Math.PI / 2, 0, rotation]}>
            <mesh position={[0, 0, -5]}>
                <extrudeGeometry args={[shape, { depth: thickness, bevelEnabled: false }]} />
                <meshStandardMaterial
                    color={sector.color}
                    transparent
                    opacity={0.15}
                    emissive={sector.color}
                    emissiveIntensity={0.2}
                    side={THREE.DoubleSide}
                />
            </mesh>

            {/* Sector Label */}
            <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
                <Text
                    position={[
                        Math.cos((startAngle + endAngle) / 2) * (outerRadius + 2),
                        Math.sin((startAngle + endAngle) / 2) * (outerRadius + 2),
                        -4.8
                    ]}
                    fontSize={0.6}
                    color="white"
                    font="https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfMZhrib2Bg-4.ttf"
                    anchorX="center"
                    anchorY="middle"
                    rotation={[0, 0, (startAngle + endAngle) / 2 - Math.PI / 2]}
                >
                    {sector.name}
                </Text>
            </Float>

            {/* Star Markers */}
            {sector.stars.map((star: any, i: number) => {
                const angle = startAngle + (i + 1) * (Math.PI / 180 * 10); // Simple spread
                const dist = innerRadius + (outerRadius - innerRadius) * (0.3 + i * 0.2);
                return (
                    <group key={star.name} position={[Math.cos(angle) * dist, Math.sin(angle) * dist, -4.7]}>
                        <mesh>
                            <sphereGeometry args={[0.08, 8, 8]} />
                            <meshBasicMaterial color="#ffffff" />
                        </mesh>
                        <Text
                            position={[0, -0.3, 0]}
                            fontSize={0.25}
                            color="#aaaaaa"
                            anchorX="center"
                            anchorY="top"
                        >
                            {star.name}
                        </Text>
                    </group>
                );
            })}
        </group>
    );
};

export const PlanisphereOverlay = ({ rotation }: { rotation: number }) => {
    return (
        <group>
            {planisphereData.sectors.map((sector, i) => (
                <SectorWedge key={sector.id} sector={sector} index={i} rotation={rotation} />
            ))}

            {/* Central Axis */}
            <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -5, 0]}>
                <ringGeometry args={[0, 8, 32]} />
                <meshStandardMaterial color="#222222" transparent opacity={0.1} />
            </mesh>

            <Text
                position={[0, -4.9, 0]}
                rotation={[-Math.PI / 2, 0, 0]}
                fontSize={1}
                color="#333333"
                opacity={0.5}
            >
                AN
            </Text>
        </group>
    );
};
