'use client';

import React, { useState } from 'react';
import { Text } from '@react-three/drei';
import * as THREE from 'three';

export interface Slot3DData {
  id: string;
  slot_number: string;
  floor: number;
  status: 'available' | 'occupied' | 'reserved' | 'ev';
  current_plate?: string;
  position: [number, number, number];
}

interface ParkingSlot3DProps {
  slot: Slot3DData;
  isSelected: boolean;
  onSelect: (slot: Slot3DData) => void;
}

export function ParkingSlot3D({ slot, isSelected, onSelect }: ParkingSlot3DProps) {
  const [hovered, setHovered] = useState(false);

  // Status-based colors
  let color = '#10B981'; // Available (Emerald Green)
  if (slot.status === 'occupied') color = '#EF4444'; // Occupied (Red)
  if (slot.status === 'reserved') color = '#F59E0B'; // Reserved (Amber)
  if (slot.status === 'ev') color = '#3B82F6'; // EV Charging (Blue)

  if (isSelected) {
    color = '#F43F5E'; // Selection accent (Rose)
  }

  return (
    <group position={slot.position}>
      {/* Slot Base Plate */}
      <mesh
        onClick={(e) => {
          e.stopPropagation();
          onSelect(slot);
        }}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <boxGeometry args={[1.8, 0.12, 3.4]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered || isSelected ? 0.6 : 0.2}
          roughness={0.2}
          metalness={0.1}
        />
      </mesh>

      {/* Slot Number Label */}
      <Text
        position={[0, 0.15, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        fontSize={0.35}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
      >
        {slot.slot_number}
      </Text>

      {/* If Occupied - Stilizatsiyalashgan 3D Mashina Box */}
      {slot.status === 'occupied' && (
        <group position={[0, 0.5, 0]}>
          <mesh>
            <boxGeometry args={[1.4, 0.8, 2.6]} />
            <meshStandardMaterial color="#0F172A" roughness={0.4} metalness={0.8} />
          </mesh>
          {/* Car roof glass effect */}
          <mesh position={[0, 0.35, -0.2]}>
            <boxGeometry args={[1.2, 0.4, 1.4]} />
            <meshStandardMaterial color="#38BDF8" roughness={0.1} transparent opacity={0.6} />
          </mesh>
        </group>
      )}

      {/* If EV Charging - Stilizatsiyalashgan icon/marker */}
      {slot.status === 'ev' && (
        <mesh position={[0, 0.4, 0]}>
          <boxGeometry args={[0.6, 0.6, 0.6]} />
          <meshStandardMaterial color="#60A5FA" emissive="#3B82F6" emissiveIntensity={0.8} />
        </mesh>
      )}
    </group>
  );
}
