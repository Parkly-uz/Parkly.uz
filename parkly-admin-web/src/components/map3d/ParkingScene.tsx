'use client';

import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html } from '@react-three/drei';
import * as THREE from 'three';

interface Slot3DProps {
  position: [number, number, number];
  number: string;
  status: 'available' | 'occupied' | 'reserved';
  onClick: () => void;
}

function SlotBox({ position, number, status, onClick }: Slot3DProps) {
  const [hovered, setHovered] = useState(false);

  let color = '#10B981'; // Available (Emerald)
  if (status === 'occupied') color = '#EF4444'; // Occupied (Red)
  if (status === 'reserved') color = '#F59E0B'; // Reserved (Amber)

  return (
    <group position={position}>
      {/* Slot Base Plate */}
      <mesh
        onClick={(e) => {
          e.stopPropagation();
          onClick();
        }}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <boxGeometry args={[1.8, 0.1, 3.2]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? 0.5 : 0.2}
          roughness={0.3}
        />
      </mesh>

      {/* Slot Number Text */}
      <Text
        position={[0, 0.15, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        fontSize={0.4}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
      >
        {number}
      </Text>
    </group>
  );
}

interface FloorProps {
  floorNumber: number;
  selectedSlot: string | null;
  onSelectSlot: (number: string) => void;
}

function FloorLevel({ floorNumber, selectedSlot, onSelectSlot }: FloorProps) {
  // Generate slots for this floor (e.g. 12 slots arranged in 2 rows)
  const slotsPerRow = 6;
  const slots = [];

  for (let i = 1; i <= 12; i++) {
    const row = i <= slotsPerRow ? 0 : 1;
    const col = i <= slotsPerRow ? i - 1 : i - slotsPerRow - 1;
    const x = (col - slotsPerRow / 2 + 0.5) * 2.2;
    const z = (row - 0.5) * 4.5;
    const y = (floorNumber - 1) * 3; // Vertical stack per floor

    const slotNum = `F${floorNumber}-${i < 10 ? '0' + i : i}`;
    const status: 'available' | 'occupied' | 'reserved' =
      i % 3 === 0 ? 'occupied' : i % 5 === 0 ? 'reserved' : 'available';

    slots.push(
      <SlotBox
        key={slotNum}
        position={[x, y, z]}
        number={slotNum}
        status={status}
        onClick={() => onSelectSlot(slotNum)}
      />
    );
  }

  return (
    <group>
      {/* Floor Slab */}
      <mesh position={[0, (floorNumber - 1) * 3 - 0.2, 0]}>
        <boxGeometry args={[15, 0.2, 11]} />
        <meshStandardMaterial color="#1E293B" roughness={0.8} />
      </mesh>
      {/* Floor Label */}
      <Text
        position={[-6.5, (floorNumber - 1) * 3 + 0.5, -5]}
        fontSize={0.6}
        color="#38BDF8"
      >
        {floorNumber}-QAVAT
      </Text>
      {slots}
    </group>
  );
}

interface ParkingSceneProps {
  activeFloor: number | null;
  selectedSlot: string | null;
  onSelectSlot: (slot: string) => void;
}

export default function ParkingScene({ activeFloor, selectedSlot, onSelectSlot }: ParkingSceneProps) {
  return (
    <Canvas
      camera={{ position: [15, 18, 22], fov: 50 }}
      className="w-full h-full bg-slate-950 rounded-3xl"
    >
      <ambientLight intensity={0.7} />
      <directionalLight position={[10, 20, 15]} intensity={1.2} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} />

      <group position={[0, -3, 0]}>
        {activeFloor === null ? (
          <>
            <FloorLevel floorNumber={1} selectedSlot={selectedSlot} onSelectSlot={onSelectSlot} />
            <FloorLevel floorNumber={2} selectedSlot={selectedSlot} onSelectSlot={onSelectSlot} />
            <FloorLevel floorNumber={3} selectedSlot={selectedSlot} onSelectSlot={onSelectSlot} />
            <FloorLevel floorNumber={4} selectedSlot={selectedSlot} onSelectSlot={onSelectSlot} />
          </>
        ) : (
          <FloorLevel floorNumber={activeFloor} selectedSlot={selectedSlot} onSelectSlot={onSelectSlot} />
        )}
      </group>

      <OrbitControls makeDefault enablePan={true} enableZoom={true} enableRotate={true} />
    </Canvas>
  );
}
