import { HStack, Status } from '@chakra-ui/react';

import type { DeskDto } from '../../../types';
import { statusLabel, statusPalette } from '../../../utils/deskStatus';

interface DeskRoomStatusStripProps {
  desks: DeskDto[];
}

export default function DeskRoomStatusStrip({ desks }: DeskRoomStatusStripProps) {
  return (
    <HStack gap={1.5} align="center" aria-label="Status per desk">
      {desks.map((desk) => (
        <Status.Root
          key={desk.id}
          colorPalette={statusPalette(desk.status)}
          size="sm"
          title={`${desk.name}: ${statusLabel(desk.status)}`}
        >
          <Status.Indicator />
        </Status.Root>
      ))}
    </HStack>
  );
}
