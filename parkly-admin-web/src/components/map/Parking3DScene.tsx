'use client';

import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import { ParkingSlot3D, Slot3DData } from './ParkingSlot3D';

interface Parking3DSceneProps {
  slots: Slot3DData[];
  selectedFloor: number | null;
  selectedSlot: Slot3DData | null;
  onSelectSlot: (slot: Slot3DData) => void;
}

export default function Parking3DScene({
  slots,
  selectedFloor,
  selectedSlot,
  onSelectSlot,
}: Parking3DSceneProps) {
  // Filter slots by floor if selected
  const filteredSlots = selectedFloor !== null ? slots.filter((s) => s.floor === selectedFloor) : slots;

  return (
    <Canvas
      camera={{ position: [18, 20, 25], fov: 45 }}
      className="w-full h-full bg-slate-950 rounded-3xl"
    >
      <ambientLight intensity={0.8} />
      <directionalLight position={[15, 25, 20]} intensity={1.4} />
      <pointLight position={[-15, -15, -15]} intensity={0.5} />

      <group position={[0, -2, 0]}>
        {/* Render Floors and their slots */}
        {[1, 2, 3, 4].map((floorNum) => {
          if (selectedFloor !== null && selectedFloor !== floorNum) return null;
          const floorY = (floorNum - 1) * 3.5;

          return (
            <group key={floorNum} position={[0, floorY, 0]}>
              {/* Floor Slab Plate */}
              <mesh position={[0, -0.2, 0]}>
                <boxGeometry args={[18, 0.2, 12]} />
                <meshStandardMaterial color="#1E293B" roughness={0.7} metalness={0.2} />
              </mesh>

              {/* Floor Header Label */}
              <Text
                position={[-8, 0.6, -5.2]}
                fontSize={0.5}
                color="#38BDF8"
                anchorX="left"
              >
                {floorNum}-QAVAT ({floorNum === 1 ? 'A-Zona' : floorNum === 2 ? 'B-Zona' : floorNum === 3 ? 'C-Zona' : 'VIP / EV Zone'})
              </Text>

              {/* Slots on this floor */}
              {slots
                .filter((s) => s.floor === floorNum)
                .map((slot) => (
                  <ParkingSlot3D
                    key={slot.id}
                    slot={slot}
                    isSelected={selectedSlot?.id === slot.id}
                    onSelect={onSelectSlot}
                  />
                ))}
            </group>
          );
        })}
      </group>

      <OrbitControls makeDefault enablePan={true} enableZoom={true} enableRotate={true} maxPolarAngle={Math.PI / 2.1} />
    </Canvas>
  );
}
